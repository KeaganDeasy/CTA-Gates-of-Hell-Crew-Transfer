import os
import sys

# Terminal Colors for Clean ADHD-friendly UI
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    BG_GREEN = '\033[42m\033[30m' # Green Background with Black Text
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Prints a standardized, colored header for each step."""
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}=== {text} ==={Colors.ENDC}\n")

def log_success(message):
    """Prints a success message with a bullet point."""
    print(f" • {Colors.GREEN}{message}{Colors.ENDC}")

def log_warning(message):
    """Prints a warning message with a bullet point."""
    print(f" • {Colors.WARNING}Warning: {message}{Colors.ENDC}")

def log_error(message):
    """Prints an error message with a bullet point."""
    print(f" • {Colors.FAIL}Error: {message}{Colors.ENDC}")

def format_crew_member(index, cid, exp, breed):
    """Formats the current squad members in Step 3 with high visibility."""
    idx_str = f"[{index}]".ljust(6)
    id_str = f"{cid}".ljust(10)
    
    # Highlight veterancy levels
    if exp >= 7.0:
        exp_display = f"{Colors.WARNING}{Colors.BOLD}ACE (Lvl {exp:.0f}){Colors.ENDC}"
    elif exp >= 1.0:
        exp_display = f"{Colors.BLUE}EXP (Lvl {exp:.1f}){Colors.ENDC}"
    else:
        exp_display = f"{Colors.FAIL}ROOKIE (Lvl 0){Colors.ENDC}"

    return f" {idx_str} {id_str} | {breed.ljust(35)} ({exp_display})"

def format_candidate(index, cand):
    """Returns a formatted string for a candidate in the Scout Report."""
    # Aggressive Tag for role matching using background colors
    match_tag = f" {Colors.BG_GREEN}{Colors.BOLD} ROLE MATCH {Colors.ENDC}" if cand['role_match'] else ""
    
    # Blue Tag for current location
    squad_tag = f"{Colors.BLUE}[SQUAD: {cand['squad']}]{Colors.ENDC}"
    
    # Colorize and Label the experience value
    exp_val = cand['exp']
    if exp_val >= 7.0:
        exp_display = f"{Colors.WARNING}{Colors.BOLD}ACE (Lvl {exp_val:.0f}){Colors.ENDC}"
    elif exp_val >= 5.0:
        exp_display = f"{Colors.WARNING}VET (Lvl {exp_val:.0f}){Colors.ENDC}"
    elif exp_val >= 2.0:
        exp_display = f"{Colors.BLUE}EXP (Lvl {exp_val:.1f}){Colors.ENDC}"
    else:
        exp_display = f"Lvl {exp_val:.1f}"
    
    # Build the final string with aligned spacing
    idx_str = f"[{index}]".ljust(6)
    id_str = f"{cand['id']}".ljust(10)
    
    return f" {idx_str} {id_str} | {cand['breed'].ljust(35)} ({exp_display}) {squad_tag}{match_tag}"

def print_manifest(selected_rookies, selected_vets):
    """Prints the high-visibility Transfer Manifest (Review Changes)."""
    print_header("Transfer Manifest (Review Changes)")
    print(f"{Colors.BOLD}Planned Personnel Movements:{Colors.ENDC}\n")
    
    swap_list = []
    for i in range(len(selected_rookies)):
        r_id, r_exp, r_breed = selected_rookies[i]
        v = selected_vets[i]
        swap_list.append((r_id, v['id']))
        
        # Rookie Line (Moving Out)
        print(f" {i+1}. {Colors.FAIL}{Colors.BOLD}OUT:{Colors.ENDC} {r_id} ({r_breed}, Lvl {r_exp:.1f})")
        
        # Transfer Arrow
        print(f"    {Colors.BOLD}  ↑ SWAPPING SEATS WITH ↑{Colors.ENDC}")
        
        # Veteran Line (Moving In)
        print(f"    {Colors.GREEN}{Colors.BOLD} IN:{Colors.ENDC} {v['id']} ({v['breed']}, Lvl {v['exp']:.1f}) [From: {v['squad']}]")
        print("-" * 50)
        
    return swap_list

def get_status_tag(exp):
    """Returns a color-coded status tag based on veterancy level."""
    if exp < 1.0:
        return f"{Colors.GREEN}► ROOKIE (Target){Colors.ENDC}"
    elif exp >= 7.0:
        return f"{Colors.WARNING}★★★ ELITE ACE{Colors.ENDC}"
    elif exp >= 5.0:
        return f"{Colors.WARNING}★★ VETERAN{Colors.ENDC}"
    elif exp >= 2.0:
        return f"{Colors.BLUE}★ SEASONED{Colors.ENDC}"
    return "Standard"

# ==========================================
# INPUT VALIDATION WITH UX
# ==========================================

def get_valid_integer(prompt, min_val, max_val):
    """Prompt user with validation and colored error feedback."""
    while True:
        try:
            val = int(input(f"{Colors.BOLD}{prompt}{Colors.ENDC}").strip())
            if min_val <= val <= max_val:
                return val
            log_error(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            log_error("Please enter a valid number")
        except KeyboardInterrupt:
            sys.exit(0)

def get_valid_indices(prompt, max_index, required_count=None):
    """Get comma-separated indices with validation and error feedback."""
    while True:
        try:
            raw = input(f"{Colors.BOLD}{prompt}{Colors.ENDC}").strip()
            indices = [int(x.strip()) - 1 for x in raw.split(',')]
            
            if all(0 <= idx < max_index for idx in indices):
                if required_count and len(indices) != required_count:
                    log_error(f"You must select exactly {required_count} items")
                    continue
                return indices
            else:
                log_error(f"All numbers must be between 1 and {max_index}")
        except ValueError:
            log_error("Invalid format. Use comma-separated numbers: 1, 2, 3")
        except KeyboardInterrupt:
            sys.exit(0)

def get_yes_no(prompt, default='n'):
    """Get yes/no confirmation with flexible input."""
    valid_yes = ['y', 'yes', 'Y', 'YES']
    valid_no = ['n', 'no', 'N', 'NO']
    
    while True:
        response = input(f"{Colors.BOLD}{prompt}{Colors.ENDC}").strip()
        if not response:
            return default.lower() == 'y'
        if response in valid_yes:
            return True
        if response in valid_no:
            return False
        log_error("Please enter 'y' for yes or 'n' for no")

# ==========================================
# FILE PATH INTERACTION
# ==========================================

def get_save_path_interactive(config):
    """Interactive path selection with recent history display."""
    print_header("Save File Selection")
    
    # Show current/last used path
    if config.get('default_save_path'):
        print(f"{Colors.BOLD}Last used:{Colors.ENDC}")
        print(f"  {Colors.GREEN}{config['default_save_path']}{Colors.ENDC}\n")
    
    # Show recent saves if available
    recent = config.get('recent_saves', [])
    if recent:
        print(f"{Colors.BOLD}Recent files:{Colors.ENDC}")
        for i, path in enumerate(recent[:5], 1):
            print(f"  [{i}] {os.path.basename(path)}")
        print()
    
    # Prompt user
    if config.get('default_save_path'):
        if get_yes_no("Use last path? (y/n): ", default='y'):
            return config['default_save_path']
    
    # Ask for new path
    new_path = input(f"{Colors.BOLD}Enter save file path: {Colors.ENDC}").strip()
    new_path = new_path.replace('"', '').replace("'", "")
    return new_path

def display_validation_errors(errors):
    """Display file validation errors with formatting."""
    print(f"\n{Colors.FAIL}{Colors.BOLD}Save file validation failed:{Colors.ENDC}")
    for err in errors:
        print(f"  {Colors.FAIL}✗{Colors.ENDC} {err}")
    print()

def display_validation_success():
    """Display validation success message."""
    log_success("Save file validated successfully")

# ==========================================
# ENHANCED DISPLAY FUNCTIONS
# ==========================================

def display_squad_list(squads):
    """Display formatted squad list (replaces inline printing)."""
    for i, sq in enumerate(squads):
        print(f" [{i+1}] {sq['name']} (Max Veterancy: {sq['max_exp']:.1f}) - {get_status_tag(sq['max_exp'])}")

def display_crew_members(current_crew):
    """Display formatted crew list using existing format_crew_member."""
    for i, (cid, exp, breed) in enumerate(current_crew):
        print(format_crew_member(i+1, cid, exp, breed))

def display_candidates(candidates):
    """Display formatted candidate list using existing format_candidate."""
    for i, cand in enumerate(candidates):
        print(format_candidate(i+1, cand))
