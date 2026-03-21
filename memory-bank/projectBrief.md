# GoH Smart Scout - Project Brief

## Project Overview
**GoH Smart Scout** is a specialized utility tool for the game *Call to Arms: Gates of Hell* that enables players to transfer high-veterancy crew members between campaign squads while maintaining game stability and role compatibility.

## Core Objective
Identify high-level veterans across all campaign squads and allow selective transfer into a specific target squad through surgical modification of save file data structures, preventing game state corruption.

## Target Audience
- Call to Arms: Gates of Hell players managing large campaign rosters
- Players seeking to optimize squad composition without risking save file corruption
- Users needing ADHD-friendly interface with clear visual hierarchy

## Key Value Propositions
1. **Game Stability**: Original save files remain untouched; modified saves are clearly distinguishable
2. **Role Safety**: Pattern-based role compatibility matching prevents incompatible transfers
3. **User Experience**: ADHD-friendly interface with color-coded visual hierarchy and clear workflow progression
4. **Persistence**: Configuration and path preferences saved between sessions
5. **Safety First**: Extensive validation and error handling with graceful degradation

## Primary Use Case
A player has multiple squads with varying experience levels. They identify a target squad with low-level recruits, scan the entire campaign for higher-level veterans in other squads or reserves, and selectively transfer those veterans into the target squad while maintaining role compatibility (e.g., tank commanders to tank slots).

## Success Criteria
- ✅ High-level "Ace" squads automatically identified and highlighted
- ✅ Transfer is role-safe and maintains game stability
- ✅ Original save file never at risk of corruption
- ✅ Modified saves clearly distinguishable from originals
- ✅ Configuration persists between runs without manual re-entry
- ✅ ADHD-friendly interface with clear visual hierarchy

## Project Status
**Active Development** - Functional Specification v2.0 complete, core modules implemented (CLI utilities, configuration management, file validation).

## Technical Foundation
- **Language**: Python 3.x
- **Architecture**: Modular separation (CLI/Config/Validation layers)
- **File Format**: .sav files as ZIP containers with UTF-16-LE/UTF-8 encoded campaign.scn
- **Modification Strategy**: Surgical ID swaps within CampaignSquads block only

## Future Vision
Potential expansion to GUI interface, batch processing, advanced role matching, and cross-save analysis capabilities.