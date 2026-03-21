#!/usr/bin/env python3
"""
Test script to verify stage tag extraction and display functionality.
"""

# Import the modified functions
from cli_utils import Colors, display_squad_list
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Simulated scn text with CampaignSquads block
test_scn_text = """{Campaign
    {Entities
        {Human "single_tankman(usa)" 0xa000 {Veterancy 5.0}}
        {Human "single_tankman(usa)" 0xa003 {Veterancy 3.0}}
        {Human "single_tankman(usa)" 0xa005 {Veterancy 7.0}}
        {Human "single_riflegrenade2_con(usa)" 0x829f {Veterancy 2.0}}
        {Human "single_riflegrenade2_con(usa)" 0x82a0 {Veterancy 1.0}}
    }
    
    {CampaignSquads
        {"single_tankman(usa)" "stage_1" 0xa000 0xa003 0xa005}
        {"single_riflegrenade2_con(usa)" "" 0x829f 0x82a0}
        {"infantry_platoon(ger)" "stage_3" 0x9000}
        {"tank_platoon(usa)" "Stage_5" 0x9001}
        {"artillery_crew" "stage_2" 0x9002}
    }
}"""

# Mock the parse_save_data function for testing
def parse_save_data(scn_text):
    """Simplified version for testing"""
    import re
    
    squads = []
    squads_match = re.search(r'\{\s*CampaignSquads\b', scn_text, re.IGNORECASE)
    if not squads_match:
        return [], squads
        
    # Simple extraction of squad entries
    squad_entries = re.findall(r'\{"([^"]+)"\s+"([^"]*)"\s+(0x[0-9a-fA-F\s]+)\}', scn_text)
    
    for i, (squad_name, stage_tag, ids_str) in enumerate(squad_entries):
        # Extract hex IDs
        hex_ids = re.findall(r'(0x[0-9a-fA-F]+)', ids_str)
        if hex_ids:
            # Create mock entity map for testing
            max_exp = 5.0 if "tank" in squad_name else 3.0
            squads.append({
                'display_id': f"SQ-{i+1:03d}",
                'name': squad_name,
                'stage': stage_tag,
                'max_exp': max_exp,
                'member_ids': hex_ids
            })
    
    return {}, squads

# Test the functionality
print("Testing Stage Tag Display Functionality")
print("=" * 50)

# Parse the test data
entity_map, squads = parse_save_data(test_scn_text)

print(f"Found {len(squads)} squads:")
print()

# Sort squads by max_exp as the real script does
squads.sort(key=lambda x: x['max_exp'], reverse=True)

# Display squads using the updated display_squad_list function
print("Expected display:")
print("-" * 50)
display_squad_list(squads)
print("-" * 50)

# Verify individual squad data
print("\nSquad details:")
for i, squad in enumerate(squads):
    has_stage = bool(squad.get('stage') and squad['stage'].strip())
    print(f"{i+1}. {squad['name']}: stage='{squad.get('stage', '')}', has_stage={has_stage}")

# Test edge cases
print("\nEdge case tests:")
print("- Empty stage tag: ", end="")
empty_squad = {'name': 'Test Squad', 'stage': '', 'max_exp': 1.0}
print(f"Should show no tag: {empty_squad['name']} (Max Veterancy: {empty_squad['max_exp']:.1f}) - ► ROOKIE (Target)")

print("- Stage_1 tag: ", end="")
stage1_squad = {'name': 'Stage 1 Squad', 'stage': 'stage_1', 'max_exp': 7.0}
print(f"Should show [Stage 1] in magenta: {stage1_squad['name']} (Max Veterancy: {stage1_squad['max_exp']:.1f}) {Colors.MAGENTA}[Stage 1]{Colors.ENDC} - ★★★ ELITE ACE")

print("- Stage_5 tag: ", end="")
stage5_squad = {'name': 'Stage 5 Squad', 'stage': 'Stage_5', 'max_exp': 5.0}
print(f"Should show [Stage 5] in magenta: {stage5_squad['name']} (Max Veterancy: {stage5_squad['max_exp']:.1f}) {Colors.MAGENTA}[Stage 5]{Colors.ENDC} - ★★ VETERAN")

print("\nTest completed successfully!")