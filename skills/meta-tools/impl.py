def update_experience(skill_name, experience, _context=None):
    """
    Update the experience/lessons learned for a specific skill.
    """
    if not _context:
        return "Error: Context not available."
    
    skill_manager = _context.get('skill_manager')
    if not skill_manager:
        return "Error: SkillManager not found in context."
        
    success, message = skill_manager.update_skill_experience(skill_name, experience)
    if success:
        return f"Successfully recorded experience for '{skill_name}': {experience}"
    else:
        return f"Failed to record experience: {message}"
