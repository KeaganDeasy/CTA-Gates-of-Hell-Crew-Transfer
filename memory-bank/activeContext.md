# Active Context

## Current Development State
**GoH Smart Scout** is in **active development** with core architecture implemented and functional specification v2.0 complete. The project has a solid foundation with modular separation of concerns and is ready for main script implementation.

## Recent Work (Last 1-2 Weeks)

### ✅ Completed Modules
1. **CLI Utilities (`cli_utils.py`)** - Complete
   - ADHD-friendly terminal interface with color-coded visual hierarchy
   - Standardized step headers and formatted displays
   - Input validation functions (get_valid_integer, get_valid_indices, get_yes_no)
   - Interactive path management with directory browsing
   - Arrow key navigation support (with readchar fallback)
   - File selection with metadata display
   - Output filename management with overwrite protection

2. **Configuration Management (`config_manager.py`)** - Complete
   - JSON-based configuration persistence
   - Schema validation and graceful degradation
   - Recent saves history (FIFO, max 5)
   - Default configuration with automatic creation
   - Update functions for recent saves tracking

3. **File Validation (`file_validator.py`)** - Complete
   - Save file structure validation (ZIP format, required files)
   - Campaign structure validation (CampaignSquads block, entity definitions)
   - Encoding detection (UTF-16-LE, UTF-16-BE, UTF-8)
   - Extraction and decoding functions

### ✅ Documentation
1. **Functional Specification v2.0** - Complete
   - Detailed 7-step user interaction flow
   - Technical architecture and implementation patterns
   - Configuration structure and management
   - Error handling and validation strategies
   - Known limitations and future enhancements

## Current Focus Areas

### 🔄 **Immediate Priority**: Main Script Implementation
- **Status**: Pending (Next major milestone)
- **Description**: Integration of completed modules into main workflow
- **Components Needed**:
  - Main orchestration script (likely "GoH Smart Scout" file)
  - Entity parsing and indexing logic
  - Squad extraction from CampaignSquads block
  - Role matching algorithm implementation
  - Surgical swap execution logic

### 🔄 **Configuration Integration**
- **Status**: Modules complete, integration pending
- **Description**: Connecting config_manager with cli_utils for seamless user experience
- **Components**: Path selection using config history, preference application

### 🔄 **Validation Pipeline**
- **Status**: Foundation complete, integration pending
- **Description**: Incorporating file_validator into main workflow
- **Components**: Pre-flight checks, structural validation, error feedback

## Technical Debt & Known Issues

### 1. **Main Script Missing**
- **Impact**: Core functionality not yet implemented
- **Mitigation**: Use Functional Specification as blueprint
- **Priority**: HIGH

### 2. **Testing Coverage**
- **Impact**: Limited automated testing
- **Mitigation**: Manual testing against sample save files
- **Priority**: MEDIUM

### 3. **Platform-Specific Path Handling**
- **Impact**: Windows-focused, may need Linux/macOS adjustments
- **Mitigation**: Use os.path for cross-platform compatibility
- **Priority**: LOW

### 4. **Performance Optimization**
- **Impact**: Large save files (>50MB) may have performance issues
- **Mitigation**: Configurable limits, efficient parsing algorithms
- **Priority**: LOW (address when encountered)

## Development Environment

### Current Setup
- **Repository**: `CTA-Gates-of-Hell-Crew-Transfer` (GitHub)
- **Latest Commit**: `1fe8cc7e73fe3ecc39f0b650cfdee1d80dbbc3ad`
- **IDE**: Visual Studio Code
- **Python Version**: 3.x (assumed)
- **Dependencies**: Standard library + optional `readchar` for arrow navigation

### File Structure
```
.
├── cli_utils.py           # CLI interface and formatting
├── config_manager.py      # Configuration management
├── file_validator.py      # File validation and extraction
├── GoH Smart Scout        # Main script (to be implemented)
├── config.json            # User configuration (auto-generated)
├── Template config.json   # Configuration template
├── .gitignore            # Git ignore rules
├── .clinerules           # Development guidelines
└── memory-bank/          # Project documentation
```

## Immediate Next Steps

### 1. **Implement Main Script** ⚡ CRITICAL
- Parse CampaignSquads block and extract squad information
- Implement entity indexing across all squads and reserves
- Develop role matching algorithm (pattern-based breed string analysis)
- Create surgical swap logic for ID replacement
- Integrate with existing modules (cli_utils, config_manager, file_validator)

### 2. **Integration Testing**
- Test complete workflow with sample save files
- Validate error handling and graceful degradation
- Test configuration persistence across sessions
- Verify role matching accuracy with various unit types

### 3. **User Documentation**
- Create user guide with step-by-step instructions
- Document role matching limitations and best practices
- Provide troubleshooting guide for common issues
- Create video tutorial demonstrating complete workflow

### 4. **Performance Validation**
- Test with large save files (>50MB if available)
- Optimize parsing algorithms if performance issues found
- Implement progress indicators for long operations
- Add configurable limits for very large campaigns

## Current Challenges & Decisions

### 1. **Role Matching Algorithm Precision**
- **Decision**: Use pattern-based heuristics initially
- **Rationale**: Provides good coverage for common unit types without complex external data
- **Future Enhancement**: Configurable strictness flag, game data integration

### 2. **Arrow Navigation Dependency**
- **Decision**: Use `readchar` as optional enhancement with numbered fallback
- **Rationale**: Better UX when available, functional without it
- **Implementation**: Already handled in `cli_utils.py`

### 3. **Output File Management**
- **Decision**: User-controlled naming with overwrite protection
- **Rationale**: Prevents accidental data loss while giving user control
- **Implementation**: Complete in `cli_utils.py`

## Recent Design Decisions

### 1. **Surgical Swap Approach**
- **Decision**: Modify only CampaignSquads block, leave other structures untouched
- **Rationale**: Maximum game stability, prevents corruption of entity definitions
- **Implementation**: Three-step temporary placeholder ID swap to avoid collisions

### 2. **Modular Architecture**
- **Decision**: Separate CLI, Configuration, and Validation layers
- **Rationale**: Clean separation of concerns, easier testing and maintenance
- **Implementation**: Three dedicated Python modules

### 3. **ADHD-Friendly Interface**
- **Decision**: Color-coded visual hierarchy with consistent patterns
- **Rationale**: Reduces cognitive load, improves accessibility
- **Implementation**: Centralized Colors class and formatting functions

## Team Context
- **Primary Developer**: Keagan (repository owner)
- **Development Approach**: Solo development with community feedback
- **Communication**: GitHub issues and documentation
- **Quality Focus**: Safety and stability over feature velocity

## External Dependencies
- **Game**: Call to Arms: Gates of Hell (save file format)
- **Python Libraries**: Standard library only (plus optional `readchar`)
- **Tools**: Git, Visual Studio Code, standard Python tooling

## Risk Assessment

### High Risk Areas
1. **Main Script Implementation** - Critical path blocker
2. **Save File Format Changes** - Game updates could break parsing
3. **Role Matching Accuracy** - Users may expect perfect compatibility

### Medium Risk Areas
1. **Cross-Platform Compatibility** - Primarily Windows-focused
2. **Performance with Large Saves** - Untested with >50MB files
3. **User Error Recovery** - Limited undo functionality

### Low Risk Areas
1. **Configuration Management** - Well-tested modular approach
2. **CLI Interface** - Comprehensive validation and error handling
3. **File Validation** - Robust validation chain

## Success Metrics Tracking
- **Completion**: Main script implementation
- **Stability**: 0 corruption incidents in testing
- **Performance**: <30 second processing for typical save files
- **Usability**: New users successfully complete transfer within 10 minutes

## Notes & Observations
- The Functional Specification is exceptionally detailed and aligns well with implemented modules
- Core architecture decisions appear sound and focused on stability
- ADHD-friendly design considerations are thoughtful and implementation-ready
- Next major milestone is main script implementation to bring all components together