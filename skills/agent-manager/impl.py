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
        
        # Create Worker
        worker = LLMWorker(messages, config_manager, workspace_dir, parent_agent_id=agent_id)
        
        # Connect signals to a local handler to capture output
        # We use a closure to capture agent_id
        def make_logger(aid):
            return lambda msg: step_signal.emit(f"[{aid}]: {msg}")
            
        worker.step_signal.connect(make_logger(agent_id))
        
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

    # Wait for all workers to finish
    # Since we are in a thread, we can block.
    for worker in workers:
        worker.wait()
        
    step_signal.emit("Manager: All sub-agents finished.")
    
    # Format Output
    output = "## Sub-Agent Results\n\n"
    for agent_id, result in results.items():
        output += f"### {agent_id}\n{result}\n\n"
        
    return output
