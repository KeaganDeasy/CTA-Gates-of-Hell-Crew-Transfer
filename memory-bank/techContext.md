# Technical Context

## Technology Stack

### Core Technologies
- **Language**: Python 3.x (standard library focus)
- **File Format**: .sav files (ZIP containers with UTF-16-LE/UTF-8 encoded text files)
- **Encoding**: UTF-16-LE (primary), UTF-8 (fallback)
- **Dependencies**: Standard library only + optional `readchar` for enhanced navigation

### External Dependencies
```python
# Required (standard library)
import os
import sys
import json
import zipfile
import re
import tempfile
from datetime import datetime

# Optional (enhanced UX)
import readchar  # For arrow key navigation (graceful fallback if missing)
```

## Architecture Overview

### Modular Separation
```
GoH Smart Scout/
├── Main Script (orchestration)
├── cli_utils.py (UI layer)
├── config_manager.py (data layer)
└── file_validator.py (validation layer)
```

### Data Flow
1. **Input**: User selects .sav file via CLI
2. **Validation**: File validator checks structure and encoding
3. **Extraction**: Campaign data parsed from ZIP
4. **Processing**: Entity indexing, squad analysis, role matching
5. **Interaction**: User selects squad, crew, replacements via CLI
6. **Modification**: Surgical ID swaps in CampaignSquads block
7. **Output**: New .sav file with modifications

## Core Implementation Details

### 1. Save File Structure
```
.sav File (ZIP Archive)
├── campaign.scn (UTF-16-LE/UTF-8 text)
│   ├── {Entity ...} blocks (unit definitions)
│   ├── {CampaignSquads ...} block (squad assignments)
│   └── Other game state data
├── status.chs (optional modifications tracking)
└── Other game files
```

### 2. Entity Data Model
```python
Entity = {
    "id": "0x12345678",      # Hexadecimal entity ID
    "breed": "ger_tank_commander",  # Unit type identifier
    "experience": 7.5,       # Veterancy level (0.0-10.0+)
    "squad": "Panzer Platoon" # Parent squad or "Reserve"
}
```

### 3. Surgical Swap Algorithm
```python
def perform_surgical_swap(scn_text, swaps):
    """
    swaps = [(old_id, new_id), ...]
    Only modifies IDs within {CampaignSquads} block
    Uses temporary placeholder IDs to avoid collisions
    """
    # 1. Find CampaignSquads block boundaries
    # 2. Extract block content
    # 3. Apply swaps using three-step process:
    #    a. Replace old_id → temp_id
    #    b. Replace new_id → old_id  
    #    c. Replace temp_id → new_id
    # 4. Reinsert modified block
    # 5. Clean up {mods} block in status.chs if present
```

## Module Specifications

### cli_utils.py - User Interface Layer

#### Color System
```python
class Colors:
    HEADER = '\033[95m'      # Magenta for headers
    BLUE = '\033[94m'        # Blue for information
    GREEN = '\033[92m'       # Green for success
    BG_GREEN = '\033[42m\033[30m'  # Green background for role matches
    WARNING = '\033[93m'     # Yellow/orange for warnings
    FAIL = '\033[91m'        # Red for errors
    MAGENTA = '\033[95m'     # Bright magenta for stage tags
    ENDC = '\033[0m'         # Reset
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text
```

#### Key Functions
- `print_header(text)`: Standardized step headers with screen clearing
- `format_crew_member()`: Formatted display of squad members with color-coded experience
- `format_candidate()`: Formatted display of scout report candidates with role match indicators
- `print_manifest()`: Visual transfer plan with OUT/IN arrows
- `get_valid_integer()`, `get_valid_indices()`, `get_yes_no()`: Validated user input
- `browse_saves_directory()`: Interactive file browser with metadata
- `select_file_interactive()`: Arrow-key or numbered file selection
- `get_output_filename()`: Safe output file naming with overwrite protection

### config_manager.py - Configuration Layer

#### Configuration Schema
```json
{
    "version": "1.0",
    "default_save_path": "",
    "save_directory": "",
    "recent_saves": [],
    "max_candidates": 100,
    "enable_arrow_navigation": true,
    "output_filename_pattern": "{original}_MOD_{timestamp}",
    "show_modified_in_browser": true,
    "strict_role_matching": false,
    "auto_backup": false
}
```

#### Key Functions
- `load_config()`: Loads config with defaults and schema validation
- `save_config(config)`: Saves configuration with error handling
- `update_recent_saves()`: Maintains FIFO list of recent files (max 5)
- `validate_config_schema()`: Ensures configuration integrity

### file_validator.py - Validation Layer

#### Validation Pipeline
1. **File Existence Check**: Verify .sav file exists and is readable
2. **ZIP Format Validation**: Confirm valid ZIP archive structure
3. **Required Files Check**: Ensure campaign.scn exists within archive
4. **Encoding Detection**: Auto-detect UTF-16-LE, UTF-16-BE, or UTF-8
5. **Structure Validation**: Verify CampaignSquads block and entity definitions

#### Key Functions
- `validate_save_file(sav_path)`: Comprehensive file validation
- `validate_campaign_structure(scn_text)`: Campaign structure validation
- `detect_encoding(data)`: Encoding detection with BOM analysis
- `extract_scn_from_zip(sav_path)`: Safe extraction and decoding

## Technical Workflow Implementation

### Step 0: File Selection
```python
# Using config_manager and cli_utils
config = config_manager.load_config()
save_path = cli_utils.get_save_path_interactive(config)
valid, errors = file_validator.validate_save_file(save_path)
if not valid:
    cli_utils.display_validation_errors(errors)
    # Handle error
config = config_manager.update_recent_saves(config, save_path)
config_manager.save_config(config)
```

### Step 1: Squad Discovery
```python
# Parse CampaignSquads block
squads = extract_squads(scn_text)
# Calculate max veterancy per squad
for squad in squads:
    squad['max_exp'] = max(member['exp'] for member in squad['members'])
# Sort by max experience (descending)
squads.sort(key=lambda x: x['max_exp'], reverse=True)
# Display with color-coded status tags
cli_utils.display_squad_list(squads)
```

### Step 2-4: Crew Selection & Scout Report
```python
# Entity indexing
entities = index_all_entities(scn_text)
# Filter candidates (exclude current squad, match roles, sort by experience)
candidates = filter_candidates(entities, current_squad_members, role_patterns)
# Role matching logic
def is_role_compatible(candidate_breed, target_breed):
    # Pattern-based matching
    tank_roles = ['tank', 'panzer', 'armor']
    infantry_roles = ['infantry', 'soldier', 'rifleman']
    # Return True if compatible patterns match
```

### Step 5-7: Transfer & Output
```python
# Generate transfer manifest
swap_list = cli_utils.print_manifest(selected_rookies, selected_vets)
# Get output filename with validation
output_path = cli_utils.get_output_filename(save_path, config['output_filename_pattern'])
# Perform surgical swap
modified_scn = perform_surgical_swap(scn_text, swap_list)
# Create new .sav file
create_modified_save(save_path, output_path, modified_scn)
```

## Data Structures

### Squad Representation
```python
Squad = {
    "name": "Infantry Platoon",
    "max_exp": 7.5,
    "members": [
        ("0x12345678", 1.2, "ger_rifleman"),
        ("0x23456789", 7.5, "ger_tank_commander")
    ],
    "stage": "stage_1"  # Optional stage tag
}
```

### Candidate Representation
```python
Candidate = {
    "id": "0x34567890",
    "breed": "ger_tank_commander",
    "exp": 8.2,
    "squad": "Panzer Division",
    "role_match": True,  # Based on pattern matching
    "stage": "stage_2"   # Optional stage tag
}
```

## Encoding & Parsing Details

### UTF-16-LE Detection
```python
def detect_encoding(data):
    if data.startswith(b'\xff\xfe'):
        return 'utf-16-le', data.decode('utf-16-le', errors='ignore')
    elif data.startswith(b'\xfe\xff'):
        return 'utf-16-be', data.decode('utf-16-be', errors='ignore')
    else:
        return 'utf-8', data.decode('utf-8', errors='ignore')
```

### Brace Matching Algorithm
```python
def extract_block(text, block_name):
    """Extract content between {BlockName ... } braces"""
    pattern = r'\{\s*' + re.escape(block_name) + r'\b[^{]*\{([^}]*)\}[^}]*\}'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else None
```

## Performance Considerations

### Memory Management
- **Stream Processing**: Process large files in chunks where possible
- **Temporary Files**: Use `tempfile` module for secure temporary storage
- **Cleanup**: Automatic cleanup of temporary directories

### Algorithm Complexity
- **Entity Indexing**: O(n) where n = number of entities in save file
- **Role Matching**: O(m×k) where m = candidates, k = role patterns
- **Surgical Swap**: O(s) where s = size of CampaignSquads block

### Optimization Strategies
1. **Lazy Loading**: Only extract and parse necessary sections
2. **Pattern Caching**: Cache compiled regex patterns
3. **Early Exit**: Stop processing when candidate limit reached
4. **Configurable Limits**: `max_candidates` setting prevents overwhelming displays

## Error Handling Strategy

### Validation Chain
```python
# Multi-layer validation
1. File existence and readability
2. ZIP archive structure
3. Required campaign.scn presence
4. Encoding detection and decoding
5. CampaignSquads block existence
6. Entity definitions presence
7. User input validation (ranges, formats, quantities)
```

### Graceful Degradation
- Missing `config.json`: Use hardcoded defaults with warning
- Missing `readchar`: Fallback to numbered selection
- Encoding failure: Try multiple encodings sequentially
- Missing `status.chs`: Skip cleanup step, continue normally

### User Feedback
- Color-coded messages (success=green, warning=yellow, error=red)
- Specific, actionable error messages
- File metadata display for overwrite warnings
- Progress indicators for long operations

## Testing Strategy

### Unit Tests Needed
1. **File Validation**: Invalid files, missing components, encoding issues
2. **Configuration**: Loading, saving, schema validation
3. **CLI Utilities**: Input validation, formatting, edge cases
4. **Parsing Logic**: Entity extraction, squad parsing, role matching
5. **Swap Algorithm**: ID replacement, collision avoidance

### Integration Tests
1. **Complete Workflow**: End-to-end transfer simulation
2. **Error Recovery**: Graceful handling of various failure modes
3. **Configuration Persistence**: Across multiple sessions
4. **Performance**: Large save file processing

### Manual Testing Checklist
- [ ] Valid .sav file processing
- [ ] Invalid file handling (corrupted, wrong format)
- [ ] Arrow key navigation (with and without readchar)
- [ ] Configuration persistence
- [ ] Role matching accuracy
- [ ] Surgical swap correctness
- [ ] Overwrite protection
- [ ] Temporary file cleanup

## Deployment Considerations

### Platform Support
- **Primary**: Windows (game's primary platform)
- **Secondary**: Linux/macOS with path adjustments
- **Dependencies**: Python 3.x standard library

### Distribution Options
1. **Standalone Executable**: PyInstaller or similar
2. **Python Package**: pip installable
3. **Portable Script**: Single-file Python with modules
4. **GitHub Releases**: Versioned releases with changelog

### User Requirements
- **Python 3.6+**: Standard library compatibility
- **Game Save Files**: Call to Arms: Gates of Hell campaign saves
- **Permissions**: Read/write access to save file directories

## Security Considerations

### File Operations
- **Original Preservation**: Never modify original .sav files
- **User Control**: Explicit confirmation for overwrites
- **Path Validation**: Prevent directory traversal attacks
- **Temporary Files**: Secure creation and cleanup

### Input Validation
- **Path Sanitization**: Remove quotes and validate characters
- **Range Checking**: All user inputs validated against allowed ranges
- **Format Validation**: Comma-separated indices, yes/no responses

### Configuration Security
- **Schema Validation**: Prevent malformed config files
- **Default Fallback**: Safe defaults if config corrupted
- **Recent Files Limit**: Prevent unbounded memory usage

## Monitoring & Logging

### Diagnostic Information
```python
# Configurable verbosity levels
VERBOSITY_LEVELS = {
    'silent': 0,    # Errors only
    'normal': 1,    # Basic progress
    'verbose': 2,   # Detailed steps
    'debug': 3      # Technical details
}
```

### Log Areas
1. **File Operations**: Opening, reading, writing files
2. **Parsing Results**: Entities found, squads identified
3. **User Actions**: Selections, confirmations, overrides
4. **Performance Metrics**: Processing times, memory usage
5. **Errors & Warnings**: Validation failures, edge cases

### Error Reporting
- **User-Friendly**: Clear, actionable error messages
- **Technical Details**: Available in debug mode for troubleshooting
- **Context Preservation**: Include file paths, line numbers where relevant