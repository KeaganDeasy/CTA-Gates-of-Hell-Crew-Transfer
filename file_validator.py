"""
File validation for GoH Smart Scout.
Pure validation layer - no user interface or printing.
"""
import os
import re
import zipfile

def validate_save_file(sav_path):
    """
    Validate save file structure.
    
    Args:
        sav_path (str): Path to .sav file
        
    Returns:
        tuple: (valid: bool, errors: list[str])
    """
    errors = []
    
    # Check 1: File exists
    if not os.path.exists(sav_path):
        errors.append("File not found")
        return False, errors
    
    # Check 2: Is it a ZIP archive?
    if not zipfile.is_zipfile(sav_path):
        errors.append("File is not a valid .sav archive (must be ZIP format)")
        return False, errors
    
    # Check 3: Contains campaign.scn and is readable
    try:
        with zipfile.ZipFile(sav_path, 'r') as z:
            files = z.namelist()
            scn_file = None
            
            # Find campaign.scn or .scm file
            for name in files:
                if any(x in name.lower() for x in ['campaign.scn', 'campaign.scm']):
                    scn_file = name
                    break
            
            if not scn_file:
                errors.append("No campaign.scn or campaign.scm file found in archive")
                return False, errors
            
            # Check 4: Can we read the scenario file?
            try:
                data = z.read(scn_file)
                if len(data) == 0:
                    errors.append("campaign.scn file is empty")
                    return False, errors
            except Exception as e:
                errors.append(f"Cannot read campaign.scn: {e}")
                return False, errors
                
    except zipfile.BadZipFile:
        errors.append("Corrupted ZIP archive")
        return False, errors
    except PermissionError:
        errors.append("Permission denied accessing save file")
        return False, errors
    except Exception as e:
        errors.append(f"Archive error: {e}")
        return False, errors
    
    return True, []

def validate_campaign_structure(scn_text):
    """
    Validate campaign file has required structure.
    
    Args:
        scn_text (str): Content of campaign.scn file
        
    Returns:
        tuple: (valid: bool, error: str|None)
    """
    # Check for CampaignSquads block
    if not re.search(r'\{\s*CampaignSquads\b', scn_text, re.IGNORECASE):
        return False, "No CampaignSquads block found in save file"
    
    # Check for entity definitions
    if not re.search(r'\{\s*(?:Entity|Human|Vehicle)\s+', scn_text, re.IGNORECASE):
        return False, "No entity definitions found in save file"
    
    return True, None

def detect_encoding(data):
    """
    Detect encoding of binary data.
    
    Args:
        data (bytes): Raw file data
        
    Returns:
        tuple: (encoding: str, text: str)
    """
    if data.startswith(b'\xff\xfe'):
        return 'utf-16-le', data.decode('utf-16-le', errors='ignore')
    elif data.startswith(b'\xfe\xff'):
        return 'utf-16-be', data.decode('utf-16-be', errors='ignore')
    else:
        return 'utf-8', data.decode('utf-8', errors='ignore')

def extract_scn_from_zip(sav_path):
    """
    Extract and decode campaign.scn from save file.
    
    Args:
        sav_path (str): Path to .sav file
        
    Returns:
        tuple: (success: bool, scn_text: str|None, encoding: str|None, error: str|None)
    """
    try:
        with zipfile.ZipFile(sav_path, 'r') as z:
            # Find campaign.scn file
            scn_file = None
            for name in z.namelist():
                if any(x in name.lower() for x in ['campaign.scn', 'campaign.scm']):
                    scn_file = name
                    break
            
            if not scn_file:
                return False, None, None, "No campaign.scn file found in archive"
            
            # Read and decode
            data = z.read(scn_file)
            encoding, text = detect_encoding(data)
            text = text.replace('\x00', '')
            
            return True, text, encoding, None
            
    except zipfile.BadZipFile:
        return False, None, None, "Corrupted ZIP archive"
    except PermissionError:
        return False, None, None, "Permission denied accessing save file"
    except Exception as e:
        return False, None, None, f"Error extracting save: {e}"