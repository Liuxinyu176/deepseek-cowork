from core.interaction import ask_user

def ask_user_confirmation(message):
    """
    Ask the user for confirmation.
    
    Args:
        message (str): The message to display.
    """
    result = ask_user(message)
    if result is True:
        return "User confirmed (Yes)."
    elif result is False:
        return "User denied (No)."
    else:
        # User provided text input
        return f"User replied: {result}"
