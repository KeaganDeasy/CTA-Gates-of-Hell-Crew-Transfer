# System Patterns

## Architectural Overview
**GoH Smart Scout** follows a modular, layered architecture with clear separation of concerns:

1. **CLI Layer** (`cli_utils.py`) - User interface and interaction
2. **Configuration Layer** (`config_manager.py`) - Persistent settings management
3. **Validation Layer** (`file_validator.py`) - File and data validation
4. **Core Logic** (Main script) - Business logic and orchestration

## Core Design Patterns

### 1. Surgical Swap Pattern
**Purpose**: Modify save files without corrupting game state

**Implementation**:
- Only swaps entity IDs within the `{CampaignSquads}` block
- Leaves entity definitions, mission scripts, and other structures untouched
- Uses three-step temporary placeholder IDs to avoid collisions during batch swaps

**Benefits**:
- Prevents corruption of entity definitions
- Maintains inventory/equipment associations
- Preserves mission script references

### 2. Role-Matching Heuristics
**Purpose**: Ensure transferred crew fit appropriate roles

**Implementation**:
- Pattern-based breed string analysis (e.g., "tank" in breed name matches tank slots)
- Visual indicators: `[Role Match]` tags in Scout Report
- Configurable strictness (`strict_role_matching` flag for future enhancement)

**Limitations**:
- Heuristic approach, not guaranteed 100% accurate
- Relies on consistent breed naming conventions

### 3. Configuration Persistence Pattern
**Purpose**: Maintain user preferences across sessions

**Implementation**:
- JSON configuration file (`config.json`) with sensible defaults
- Automatic creation on first run
- Schema validation and graceful degradation
- Recent saves history (FIFO, max 5 entries)

### 4. ADHD-Friendly UI Pattern
**Purpose**: Create accessible, clear interface for users with attention challenges

**Implementation**:
- Color-coded visual hierarchy (Colors class in `cli_utils.py`)
- Clear step-by-step progression with standardized headers
- High-contrast status tags and visual indicators
- Consistent formatting patterns across all displays

### 5. Validation Chain Pattern
**Purpose**: Progressive validation with clear error feedback

**Implementation**:
- **Pre-flight checks**: File existence, ZIP format, required files
- **Structural validation**: CampaignSquads block presence, entity definitions
- **User input validation**: Range checking, format validation, quantity matching
- **Graceful degradation**: Fallback modes when optional components unavailable

## Data Flow Patterns

### 1. Entity Indexing Pattern
```
Save File → Extract → Parse → Index Entities → Map to Squads → Filter Candidates
```

- Builds complete map of all entities (Human/Vehicle) with IDs, breeds, experience
- Maps each entity to parent squad or "Reserve" status
- Fast brace-matching algorithm for large save file processing

### 2. Candidate Filtering Pattern
```
All Entities → Exclude Current Squad → Role Match Filter → Experience Sort → Limit Display
```

- Filters out current squad members to avoid self-transfer
- Applies role compatibility matching
- Sorts by experience (high to low), then role match priority
- Limited to configurable maximum (default: 100)

### 3. Configuration Update Pattern
```
User Action → Update Config → Validate → Save → Persist Across Sessions
```

- Updates triggered by user file selections and preferences
- Schema validation before saving
- Automatic backup of previous configuration on corruption

## Error Handling Patterns

### 1. Graceful Degradation Pattern
- Missing `config.json`: Use hardcoded defaults with warning
- Missing `cli_utils.py`: Fallback to plain text output
- Missing `status.chs`: Skip cleaning step, continue operation
- Encoding detection failure: Try multiple encodings with error recovery

### 2. Validation Feedback Pattern
- Clear error messages with specific actionable information
- Color-coded success/error indicators
- File metadata display for existing file warnings

### 3. Safe File Operations Pattern
- Original files never modified
- User-controlled output naming with overwrite protection
- Temporary directory cleanup after processing

## User Workflow Pattern (7-Step Process)

### Step 0: Save File Selection
**Pattern**: Interactive path management with history
- Option selection (last/browse/custom)
- Directory browsing with metadata
- Arrow key navigation with fallback

### Step 1: Squad Discovery
**Pattern**: Data extraction and categorization
- Parse CampaignSquads block
- Calculate maximum veterancy per squad
- Apply visual status tags based on experience levels

### Step 2: Crew Review
**Pattern**: Detailed entity examination
- Display squad members with experience color coding
- Position-based selection system

### Step 3: Scout Report
**Pattern**: Comprehensive candidate search
- Scan all entities across squads and reserves
- Role compatibility analysis
- Sorted presentation with visual indicators

### Step 4: Veteran Selection
**Pattern**: Quantity-matched user selection
- Must match exact quantity of rookies selected
- Validation against scout report indices

### Step 5: Transfer Manifest
**Pattern**: Visual confirmation interface
- Side-by-side OUT/IN comparison
- Color-coded arrows (RED for out, GREEN for in)
- Final approval step before execution

### Step 6: Output Management
**Pattern**: Safe file creation
- User-controlled naming with validation
- Overwrite protection with file details
- Automatic .sav extension handling

### Step 7: Execution & Cleanup
**Pattern**: Surgical modification
- ID swap within CampaignSquads only
- status.chs cleanup (remove {mods} block)
- Temporary directory cleanup

## Technical Implementation Patterns

### 1. Encoding Detection Pattern
- Check BOM markers (UTF-16-LE, UTF-16-BE)
- Fallback to UTF-8
- Null character cleanup

### 2. Temporary File Management Pattern
- Use `tempfile` module for secure temporary directories
- Automatic cleanup on completion or error
- Preserve original file untouched

### 3. Color System Pattern
- Centralized Colors class with ANSI escape codes
- Consistent semantic color usage across interface
- Fallback to monochrome when terminal doesn't support colors

## Scalability Considerations

### Current Limitations
- Squad-level operations only (no individual non-squad entity transfers)
- Windows path focus (may need adjustments for Linux/macOS)
- Memory usage with large save files (>50MB)

### Future Pattern Extensions
- Batch processing pattern for multiple squads
- GUI layer abstraction pattern
- Plugin architecture for role matching algorithms
- Cross-save analysis pattern for campaign progress tracking