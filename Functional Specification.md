# **Functional Specification: GoH Crew Role-Safe Transfer Tool (Smart Scout Edition)**

## **1. Objective**

To provide a utility for *Call to Arms: Gates of Hell* that identifies high-level veterans across all campaign squads and allows the user to selectively transfer them into a specific target squad while maintaining role compatibility and game stability. The tool operates by modifying crew assignments exclusively within the `{CampaignSquads}` data structure to prevent game state corruption.

## **2. User Interaction Flow (Actual Implementation)**

### **Step 1: Squad Discovery & Selection**

* **Action:** The script scans the `campaign.scn` file for the `{CampaignSquads}` block and extracts all squads.
* **Output:** A numbered list of squads sorted by maximum veterancy level.
  * **Squad Info:** e.g., `[1] Infantry Platoon (Max Veterancy: 7.0) ★★★ ELITE ACE`
  * **Experience Indicator:** Color-coded status tags show squad veterancy level at a glance
  * **ADHD-Friendly Design:** Clear visual hierarchy with bold headers and color coding
* **Input:** User enters the number of the target squad.

### **Step 2: Current Crew Review**

* **Action:** Displays all members of the selected squad with detailed information.
* **Output:** Each squad member shown with:
  * Position number (for selection)
  * Hexadecimal ID
  * Breed/Type (e.g., `ger_tank_commander`)
  * Veterancy level with color-coded display
* **Input:** User enters comma-separated position numbers of crew members to replace (e.g., `1, 3, 5`).

### **Step 3: Scout Report Generation**

* **Action:** Scans ALL entities in the save file, filters out current squad members, and identifies potential replacements.
* **Filtering Logic:** Finds soldiers/crew in other squads OR reserves
* **Role Detection:** Auto-detects role compatibility based on breed string pattern matching
* **Sorting Priority:** 1) Experience (high to low), 2) Role match priority
* **Output:** List of candidates showing:
  * Candidate number (for selection)
  * ID, breed, and experience level
  * Current location (squad name or "Reserve")
  * Role match indicator `[Role Match]` when compatible

### **Step 4: Veteran Selection**

* **Action:** User selects replacement veterans from the Scout Report.
* **Validation:** Must select same quantity as rookies selected in Step 2
* **Output:** Confirmation of selections with visual pairing
* **Input:** Comma-separated numbers of veteran candidates (e.g., `2, 4, 7`)

### **Step 5: Transfer Manifest & Execution**

* **Action:** Shows side-by-side comparison of planned swaps in "Transfer Manifest"
* **Visualization:** Clear OUT/IN arrows with color coding (RED for out, GREEN for in)
* **Confirmation:** Final user approval before execution
* **Execution:** Performs surgical ID swap ONLY within `{CampaignSquads}` block
* **Cleanup:** Removes `{mods}` modifications from `status.chs` file
* **Output:** Creates new timestamped save file (`{original}_MOD_HHMM.sav`)
* **Safety:** Original save file is NEVER modified

## **3. Core Features & Validation Logic**

### **A. The "Squad Health" Check**

* When listing squads in Step 1, the script highlights squads with "Low Experience" (Green recruits) and "High Experience" (Elite Aces) using color-coded status tags.
* Users can quickly identify which squads need upgrades most.

### **B. Role-Matching (Pattern-Based)**

* **Pattern Matching:** Uses breed string analysis (e.g., any entity with "tank" in breed name can fill tank slots)
* **Heuristic Approach:** Not 100% guaranteed but effective for most crew types
* **Visual Indicators:** `[Role Match]` tags in Scout Report for quick identification

### **C. Data Extraction & Entity Mapping**

* **Entity Indexing:** Builds complete map of all entities (Human/Vehicle) with their IDs, breeds, and experience
* **Squad Association:** Maps each entity to its parent squad (or "Reserve" status)
* **Fast Block Parsing:** Uses optimized brace-matching algorithm to handle large save files

### **D. Surgical Swap Architecture (NEW)**

* **Targeted Modification:** ONLY swaps IDs within the `{CampaignSquads}` block
* **Prevents:** Corruption of entity definitions, breaking mission script references, inventory/equipment loss
* **Game State Safety:** Maintains consistency by not touching entity definitions or other game structures
* **Three-Step Swap:** Uses temporary placeholder IDs to avoid ID collision during batch swaps

## **4. Technical Workflow (Actual Step-by-Step)**

1. **Extract:** Unzip the `.sav` container to temporary directory
2. **Encoding Detection:** Auto-detect UTF-16-LE or UTF-8 encoding of `campaign.scn`
3. **Initial Discovery:** Index squads from `CampaignSquads` block and all entities
4. **User Choice:** Prompt for Target Squad (not individual unit)
5. **Crew Selection:** User selects which crew positions to replace
6. **Scout:** Search entity index for veterans with higher experience than selected crew
7. **Role Analysis:** Apply pattern-based role compatibility matching
8. **Display:** Present the "Scout Report" with top candidates (up to configurable maximum)
9. **Veteran Selection:** User selects replacement veterans
10. **Manifest Generation:** Create visual transfer plan for user review
11. **Update:** Perform surgical batch swap within `CampaignSquads` block only
12. **Status Cleanup:** Remove `{mods}` block from `status.chs` file if present
13. **Rebuild:** Create new timestamped `.sav` file with modified contents
14. **Cleanup:** Remove temporary directory, preserve original save file

## **5. CLI Architecture & Separation** ✅ **IMPLEMENTED v2.0**

* **Modular Design:** CLI formatting functions separated into `cli_utils.py`
* **Color System:** ADHD-friendly terminal colors with consistent visual language
* **Header Formatting:** Standardized step headers for clear workflow progression
* **Fallback Support:** Graceful degradation if `cli_utils.py` is unavailable
* **Formatting Functions:** Dedicated functions for squad display, candidate formatting, manifest generation
* **Input Validation:** Comprehensive validation functions in `cli_utils.py` (get_valid_integer, get_valid_indices, get_yes_no)
* **Path Management:** Interactive path selection with history in `cli_utils.py` (get_save_path_interactive)
* **Validation Display:** File validation error/success display functions
* **Enhanced Display:** Dedicated functions for squad, crew, and candidate lists

## **6. Configuration & Path Management (NEW)**

### **A. Configuration File (`config.json`)**
Stores persistent user settings:
* `default_save_path`: Last used or preferred save file path
* `save_directory`: Root directory for save files (e.g., game profiles folder)
* `recent_saves`: List of 5 most recently accessed saves for quick selection
* `max_candidates`: How many scout results to show (default: 100)
* `strict_role_matching`: Boolean for strict vs. loose role compatibility (future enhancement)
* `auto_backup`: Create `.sav.bak` file before modification (future enhancement)

### **B. Path Management**
* **First Run:** Prompt for save directory, store in config
* **Subsequent Runs:** Show last used file with option to browse or change
* **Path Validation:** Check file existence and readability before processing
* **Quoted Path Support:** Handle drag-and-drop file paths with quotes
* **Error Feedback:** Clear error messages for missing files or invalid paths

### **C. Config Location & Creation**
* Same directory as script: `./config.json`
* Created automatically on first run with sensible defaults
* Persists between sessions for user convenience

## **7. Save File Management Strategy (NEW)**

### **A. Backup Policy**
* **Original File:** NEVER modified, always preserved in original state
* **Backup Creation:** Optional `.sav.bak` creation before processing (configurable)
* **Output File:** New timestamped file: `{original_filename}_MOD_{HHMM}.sav`
* **Clear Distinction:** Modified saves easily distinguishable from originals

### **B. File Naming Convention**
* **Format:** `conquest 27_MOD_1430.sav` (includes hour/minute timestamp)
* **Multiple Modifications:** Allows multiple modifications per session without overwriting
* **User Clarity:** Clear visual indication of modified status in filename

### **C. Cleanup Options (Future Enhancement)**
* List all `*_MOD_*.sav` files in directory
* Offer to delete old modified saves
* Keep only N most recent modifications (configurable)
* Batch cleanup operations

## **8. Error Handling & Validation (NEW)**

### **A. Pre-Flight Checks**
1. Verify save file exists and is readable
2. Confirm it's a valid ZIP archive (`.sav` format)
3. Check for `campaign.scn` presence within archive
4. Validate `CampaignSquads` block exists and is parseable
5. Detect and handle text encoding (UTF-16-LE, UTF-8)

### **B. User Input Validation**
* **Squad Selection:** Must be valid number within displayed range
* **Crew Selection:** Comma-separated numbers, all must be valid indices
* **Veteran Selection:** Must match exact quantity of rookies selected
* **Confirmation Prompts:** Accept `y`/`yes`/`Y`/`YES` variations
* **Range Checking:** Prevent out-of-bounds selections

### **C. Graceful Degradation**
* If `config.json` invalid/missing: Use hardcoded defaults with warning
* If `cli_utils.py` missing: Fallback to plain text output with basic formatting
* If `status.chs` missing: Skip cleaning step, continue with main operation
* If encoding detection fails: Try multiple encodings with error recovery

## **9. Known Limitations (NEW)**

1. **Squad-Level Operations Only:** Cannot transfer individuals from non-squad entities (reserves only)
2. **Role Matching Heuristic:** Based on breed string patterns, not guaranteed 100% accurate for all unit types
3. **No Undo Function:** Must manually restore from original save file if mistake made
4. **Text Encoding Dependency:** Relies on proper UTF-16-LE detection; may fail with corrupted saves
5. **Single Campaign Support:** Designed for campaign mode `.sav` files, not skirmish saves
6. **Windows Path Focus:** Primarily tested on Windows paths; Linux/macOS may need path adjustments
7. **Memory Usage:** Large save files (>50MB) may cause performance issues

## **10. Future Enhancements (NEW)**

### **A. Usability Improvements**
* GUI interface with drag-and-drop file browser
* Undo/Redo transaction history within session
* Batch processing multiple squads in one operation
* Export/Import crew presets for common transfers

### **B. Technical Enhancements**
* Integration with game launcher for one-click operation
* Cross-save crew comparison and analysis
* Advanced role matching with game data integration
* Performance optimization for very large save files
* Multi-platform path handling improvements

### **C. Feature Expansion**
* Support for skirmish save files
* Crew experience modification (level adjustment)
* Equipment/Inventory transfer between units
* Squad reorganization and merging
* Campaign progress analysis and reporting

## **11. Success Criteria**

* ✅ User can find and select target squad easily within the script
* ✅ High-level "Ace" squads are automatically identified and highlighted
* ✅ Transfer is role-safe and maintains game stability
* ✅ Original save file is never at risk of corruption
* ✅ User can save and reuse save file paths across sessions
* ✅ Modified saves are clearly distinguishable from originals
* ✅ Configuration persists between runs without manual re-entry
* ✅ Path entry is validated with helpful feedback messages
* ✅ Surgical swap prevents unintended game state changes
* ✅ ADHD-friendly interface with clear visual hierarchy and color coding

## **12. Configuration Structure (Updated)**

* **`DEFAULT_SAV_PATH`:** Hardcoded fallback path (editable in script)
* **`MAX_CANDIDATES_TO_SHOW`:** Limits Scout Report display (default: 100)
* **`config.json`:** Persistent user preferences (paths, settings, history)
* **Color System:** Consistent visual language across all interface elements
* **Temporary Directory Management:** Automatic cleanup after processing

---

*Last Updated: Review against actual implementation v1.0*
*Documentation aligned with codebase architecture and usability requirements*