import json
from PySide6.QtCore import QEventLoop, QObject
from core.agent import LLMWorker

def dispatch_agents(workspace_dir, tasks, _context=None):
    """
    Spawn multiple sub-agents to execute tasks in parallel.
    
    Args:
        workspace_dir (str): The workspace directory.
        tasks (list): A list of task descriptions (strings).
        _context (dict, optional): System context containing signal emitters and config.
    
    Returns:
        str: Aggregated results from all agents.
    """
    if not tasks:
        return "No tasks provided."
    
    if not _context:
        return "Error: System context not provided (cannot access config/signals)."
    
    config_manager = _context.get('config_manager')
    step_signal = _context.get('step_signal')
    agent_state_signal = _context.get('agent_state_signal')
    tool_call_id = _context.get('tool_call_id')
    
    if not config_manager:
        return "Error: ConfigManager not found in context."

    results = {}
    workers = []
    
    # Helper QObject to handle signals in the current thread context if needed
    # But since we are inside a function called by LLMWorker (QThread), 
    # we can create sub-threads (LLMWorkers) and wait for them.
    # Note: QThread.wait() blocks the calling thread (the Manager Agent), which is what we want.
    
    step_signal.emit(f"Manager: Spawning {len(tasks)} sub-agents...")
    
    for i, task in enumerate(tasks):
        agent_id = f"Agent-{i+1}"
        messages = [{"role": "user", "content": task}]
        
        # Report initial status
        if agent_state_signal:
             agent_state_signal.emit({
                 "agent_id": agent_id,
                 "status": "pending",
                 "task": task,
                 "tool_call_id": tool_call_id
             })

        # Create Worker
        worker = LLMWorker(messages, config_manager, workspace_dir, parent_agent_id=agent_id)
        
        # Connect signals to a local handler to capture output
        # We use a closure to capture agent_id
        def make_logger(aid):
            def logger(msg):
                step_signal.emit(f"[{aid}]: {msg}")
                # Also forward to agent_state_signal for the UI Monitor
                if agent_state_signal:
                    agent_state_signal.emit({
                        "agent_id": aid,
                        "status": "log",
                        "log_content": msg,
                        "tool_call_id": tool_call_id
                    })
            return logger
            
        worker.step_signal.connect(make_logger(agent_id))
        
        # Forward agent state signals
        if agent_state_signal:
             # State tracker for this agent to avoid spamming signals
             state_tracker = {"last_status": None}

             def make_state_forwarder(aid):
                def forwarder(state):
                    # Inject tool_call_id if present so UI knows which card to update
                    if tool_call_id:
                        state["tool_call_id"] = tool_call_id
                    agent_state_signal.emit(state)
                return forwarder
             worker.agent_state_signal.connect(make_state_forwarder(agent_id))

             # Forward thinking status (throttled)
             def make_think_forwarder(aid, tracker):
                def forwarder(msg):
                    # Always emit delta for UI update
                    agent_state_signal.emit({
                        "agent_id": aid,
                        "status": "thinking",
                        "reasoning_delta": msg,
                        "tool_call_id": tool_call_id
                    })
                    tracker["last_status"] = "thinking"
                return forwarder
             worker.thinking_signal.connect(make_think_forwarder(agent_id, state_tracker))

             # Forward tool usage status
             def make_tool_forwarder(aid, tracker):
                def forwarder(tool_info):
                    tool_name = tool_info.get("name", "unknown")
                    agent_state_signal.emit({
                        "agent_id": aid,
                        "status": "tool_use",
                        "task": f"Tool: {tool_name}",
                        "tool_call_id": tool_call_id
                    })
                    tracker["last_status"] = "tool_use"
                return forwarder
             worker.tool_call_signal.connect(make_tool_forwarder(agent_id, state_tracker))

        # We need to capture the result. 
        # Since LLMWorker.finished_signal emits a dict, we need a slot.
        # But we can't easily define slots in a function.
        # We'll attach a custom attribute to the worker to store the result?
        # No, signals don't work like that.
        # We can use a container list/dict and a lambda.
        
        def make_finisher(aid, container):
            def finisher(res):
                container[aid] = res.get("content", "No content")
                if "error" in res:
                    container[aid] += f" (Error: {res['error']})"
            return finisher

        worker.finished_signal.connect(make_finisher(agent_id, results))
        
        worker.start()
        workers.append(worker)
        step_signal.emit(f"Manager: Started {agent_id} on task: {task[:30]}...")

    # Wait for all workers to finish using an event loop to allow signal processing
    # This ensures that signals (logs, results) from sub-agents are processed by the current thread.
    loop = QEventLoop()
    active_count = len(workers)
    
    def on_finished(res):
        nonlocal active_count
        active_count -= 1
        if active_count <= 0:
            loop.quit()
            
    for worker in workers:
        worker.finished_signal.connect(on_finished)
        
    if active_count > 0:
        loop.exec()
        
    step_signal.emit("Manager: All sub-agents finished.")
    
    # Format Output
    output = "## Sub-Agent Results\n\n"
    for agent_id, result in results.items():
        output += f"### {agent_id}\n{result}\n\n"
        
    return output
