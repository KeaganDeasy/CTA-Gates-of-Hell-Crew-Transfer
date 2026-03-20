"""
Configuration management for GoH Smart Scout.
Pure data layer - no user interface or printing.
"""
import json
import os

DEFAULT_CONFIG = {
    "version": "1.0",
    "default_save_path": "",
    "save_directory": "",
    "recent_saves": [],
    "max_candidates": 100,
    "enable_arrow_navigation": True,
    "output_filename_pattern": "{original}_MOD_{timestamp}",
    "show_modified_in_browser": True,
    "strict_role_matching": False,
    "auto_backup": False
}

def load_config():
    """
    Load configuration from config.json or return defaults.
    
    Returns:
        dict: Configuration dictionary with all required keys.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    # Create default config if file doesn't exist
    if not os.path.exists(config_path):
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Ensure all default keys are present
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        
        # Validate recent_saves is a list
        if not isinstance(merged.get('recent_saves'), list):
            merged['recent_saves'] = []
        
        return merged
    except (json.JSONDecodeError, IOError, PermissionError):
        # Silently return defaults if config is corrupted or unreadable
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """
    Save configuration to config.json.
    
    Args:
        config (dict): Configuration dictionary to save.
        
    Returns:
        tuple: (success: bool, error: str|None)
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    
    # Ensure config has all required keys
    merged = DEFAULT_CONFIG.copy()
    merged.update(config)
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
        return True, None
    except (IOError, PermissionError) as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"

def update_recent_saves(config, new_path):
    """
    Update recent saves list with new path (FIFO, max 5).
    
    Args:
        config (dict): Configuration dictionary (will be modified in-place).
        new_path (str): New save file path to add.
        
    Returns:
        dict: Modified configuration (same object reference).
    """
    if 'recent_saves' not in config:
        config['recent_saves'] = []
    
    recent = config['recent_saves']
    
    # Remove if already exists (to avoid duplicates)
    if new_path in recent:
        recent.remove(new_path)
    
    # Add to front (most recent first)
    recent.insert(0, new_path)
    
    # Keep only 5 most recent
    config['recent_saves'] = recent[:5]
    
    return config

def validate_config_schema(config):
    """
    Validate that config has correct schema.
    
    Args:
        config (dict): Configuration to validate.
        
    Returns:
        tuple: (valid: bool, errors: list[str])
    """
    errors = []
    
    # Check required keys
    for key in DEFAULT_CONFIG:
        if key not in config:
            errors.append(f"Missing key: {key}")
    
    # Validate types
    if 'max_candidates' in config and not isinstance(config['max_candidates'], (int, float)):
        errors.append("max_candidates must be a number")
    
    if 'recent_saves' in config and not isinstance(config['recent_saves'], list):
        errors.append("recent_saves must be a list")
    
    if 'auto_backup' in config and not isinstance(config['auto_backup'], bool):
        errors.append("auto_backup must be boolean")
    
    return len(errors) == 0, errors