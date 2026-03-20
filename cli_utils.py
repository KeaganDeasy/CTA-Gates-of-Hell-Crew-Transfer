import os

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