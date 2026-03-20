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

# ==========================================
# ENHANCED SAVE FILE INTERACTION
# ==========================================

def browse_saves_directory(directory, show_modified=True):
    """
    Scans directory for .sav files and returns list with metadata.
    
    Args:
        directory (str): Path to scan
        show_modified (bool): Include _MOD_*.sav files
        
    Returns:
        list[dict]: Files with keys: 'path', 'name', 'size', 'modified'
    """
    import os
    import glob
    from datetime import datetime
    
    if not os.path.exists(directory):
        log_error(f"Directory not found: {directory}")
        return []
    
    files = []
    pattern = os.path.join(directory, "*.sav")
    
    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        
        # Skip modified files if show_modified is False
        if not show_modified and "_MOD_" in filename:
            continue
        
        try:
            stat = os.stat(filepath)
            size_mb = stat.st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            
            files.append({
                'path': filepath,
                'name': filename,
                'size': f"{size_mb:.1f} MB",
                'modified': modified,
                'is_modified': "_MOD_" in filename
            })
        except (OSError, PermissionError):
            continue
    
    # Sort by modification date (newest first)
    files.sort(key=lambda x: os.path.getmtime(x['path']), reverse=True)
    return files

def select_file_interactive(file_list, allow_arrows=True):
    """
    Interactive file selection with optional arrow key navigation.
    
    Args:
        file_list (list[dict]): Files from browse_saves_directory()
        allow_arrows (bool): Enable arrow key navigation
        
    Returns:
        str: Selected file path, or None if cancelled
    """
    if not file_list:
        log_error("No save files found in directory")
        return None
    
    # Try to import readchar for arrow navigation
    arrow_nav = False
    if allow_arrows:
        try:
            import readchar
            arrow_nav = True
        except ImportError:
            log_warning("Arrow navigation disabled (install 'readchar' package)")
            arrow_nav = False
    
    current_selection = 0
    
    while True:
        clear_screen()
        print_header("Available Save Files")
        
        # Display file list
        for i, file_info in enumerate(file_list):
            prefix = "→" if i == current_selection else " "
            modified_tag = f" {Colors.WARNING}[MOD]{Colors.ENDC}" if file_info['is_modified'] else ""
            
            print(f" {prefix} [{i+1}] {file_info['name']} ({file_info['size']}, Modified: {file_info['modified']}){modified_tag}")
        
        print(f"\n{Colors.BOLD}Navigation:{Colors.ENDC}")
        if arrow_nav:
            print(f" • {Colors.BLUE}↑/↓{Colors.ENDC} arrows to move")
            print(f" • {Colors.GREEN}Enter{Colors.ENDC} to select")
            print(f" • {Colors.FAIL}Esc{Colors.ENDC} to cancel")
        else:
            print(f" • Enter number (1-{len(file_list)})")
            print(f" • Enter {Colors.FAIL}0{Colors.ENDC} to cancel")
        
        if arrow_nav:
            try:
                key = readchar.readkey()
                
                if key == readchar.key.UP:
                    current_selection = max(0, current_selection - 1)
                    continue
                elif key == readchar.key.DOWN:
                    current_selection = min(len(file_list) - 1, current_selection + 1)
                    continue
                elif key == readchar.key.ENTER or key == '\r' or key == '\n':
                    return file_list[current_selection]['path']
                elif key == readchar.key.ESC:
                    return None
            except Exception:
                # Fallback to numbered input on any error
                arrow_nav = False
        
        # Numbered input (fallback or primary)
        try:
            choice = input(f"\n{Colors.BOLD}Select file (1-{len(file_list)}): {Colors.ENDC}").strip()
            if not choice:
                continue
            
            choice_num = int(choice)
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(file_list):
                return file_list[choice_num - 1]['path']
            else:
                log_error(f"Please enter a number between 1 and {len(file_list)}")
        except ValueError:
            log_error("Please enter a valid number")
        except KeyboardInterrupt:
            return None

def get_output_filename(source_path, default_pattern="{original}_MOD_{timestamp}"):
    """
    Interactive output filename selection with overwrite protection.
    
    Args:
        source_path (str): Original .sav file path
        default_pattern (str): Template for suggested name
        
    Returns:
        str: Full path to output file (validated and confirmed)
    """
    import os
    from datetime import datetime
    
    source_dir = os.path.dirname(source_path)
    source_name = os.path.basename(source_path)
    source_base = os.path.splitext(source_name)[0]
    
    # Generate default name from pattern
    timestamp = datetime.now().strftime("%H%M")
    default_name = default_pattern.replace("{original}", source_base).replace("{timestamp}", timestamp)
    
    # Ensure .sav extension
    if not default_name.lower().endswith('.sav'):
        default_name += '.sav'
    
    while True:
        print_header("Output File Selection")
        print(f"{Colors.BOLD}Source file:{Colors.ENDC} {source_name}")
        print(f"{Colors.BOLD}Directory:{Colors.ENDC} {source_dir}")
        print()
        print(f"{Colors.BOLD}Suggested name:{Colors.ENDC} {Colors.GREEN}{default_name}{Colors.ENDC}")
        print()
        print(f"{Colors.BOLD}Options:{Colors.ENDC}")
        print(f" • Press {Colors.GREEN}ENTER{Colors.ENDC} to use suggested name")
        print(f" • Type custom filename (e.g., 'my_custom_save.sav')")
        print(f" • Type {Colors.FAIL}q{Colors.ENDC} to cancel operation")
        print()
        
        user_input = input(f"{Colors.BOLD}Output filename: {Colors.ENDC}").strip()
        
        if user_input.lower() == 'q':
            return None
        
        if not user_input:
            # Use default
            final_name = default_name
        else:
            # Use user input
            final_name = user_input
            if not final_name.lower().endswith('.sav'):
                final_name += '.sav'
        
        # Validate filename
        invalid_chars = r'\/:*?"<>|'
        if any(char in final_name for char in invalid_chars):
            log_error(f"Filename contains invalid characters: {invalid_chars}")
            input(f"{Colors.BOLD}Press Enter to try again...{Colors.ENDC}")
            continue
        
        # Build full path
        full_path = os.path.join(source_dir, final_name)
        
        # Check if file exists
        if os.path.exists(full_path):
            print(f"\n{Colors.WARNING}{Colors.BOLD}⚠ File already exists!{Colors.ENDC}")
            print(f"  Name: {final_name}")
            print(f"  Path: {full_path}")
            
            try:
                stat = os.stat(full_path)
                size_mb = stat.st_size / (1024 * 1024)
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                print(f"  Size: {size_mb:.1f} MB")
                print(f"  Modified: {modified}")
            except (OSError, PermissionError):
                pass
            
            print()
            if not get_yes_no(f"{Colors.BOLD}Overwrite existing file? (y/n): {Colors.ENDC}", default='n'):
                input(f"{Colors.BOLD}Press Enter to choose different name...{Colors.ENDC}")
                continue
        
        # Return validated path
        return full_path

def get_save_path_interactive(config):
    """Enhanced interactive path selection with directory browsing."""
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
    
    # Show options
    print(f"{Colors.BOLD}Options:{Colors.ENDC}")
    print(f"  [1] Use last path")
    print(f"  [2] Browse save directory")
    print(f"  [3] Enter custom path")
    print(f"  [0] Exit")
    print()
    
    while True:
        try:
            choice = input(f"{Colors.BOLD}Your choice: {Colors.ENDC}").strip()
            
            if choice == '0':
                sys.exit(0)
            elif choice == '1':
                if config.get('default_save_path'):
                    return config['default_save_path']
                else:
                    log_error("No last path available")
                    continue
            elif choice == '2':
                # Browse directory
                save_dir = config.get('save_directory', '')
                if not save_dir or not os.path.exists(save_dir):
                    log_warning("Save directory not configured or not found")
                    save_dir = input(f"{Colors.BOLD}Enter save directory path: {Colors.ENDC}").strip()
                    save_dir = save_dir.replace('"', '').replace("'", "")
                    
                    if not os.path.exists(save_dir):
                        log_error(f"Directory not found: {save_dir}")
                        continue
                    
                    # Update config
                    config['save_directory'] = save_dir
                
                # Browse files
                show_modified = config.get('show_modified_in_browser', True)
                files = browse_saves_directory(save_dir, show_modified)
                
                if not files:
                    log_error(f"No save files found in {save_dir}")
                    continue
                
                allow_arrows = config.get('enable_arrow_navigation', True)
                selected = select_file_interactive(files, allow_arrows)
                
                if selected:
                    return selected
                else:
                    continue
            elif choice == '3':
                # Custom path
                new_path = input(f"{Colors.BOLD}Enter save file path: {Colors.ENDC}").strip()
                new_path = new_path.replace('"', '').replace("'", "")
                return new_path
            else:
                log_error("Please enter 0, 1, 2, or 3")
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            log_error(f"Error: {e}")
            continue
