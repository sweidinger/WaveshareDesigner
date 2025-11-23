#!/usr/bin/env python3
"""
Fix widget condition operators in the waveshare_dashboard storage file.

This script safely accesses the storage file structure and fixes widgets
that have condition_entity set but condition_operator is null.

Usage:
    python3 fix_widget_conditions.py /path/to/storage/file [widget_id1 widget_id2 ...]

Example:
    python3 fix_widget_conditions.py /config/.storage/waveshare_dashboard w_1763884148253_159 w_1763884173316_9460
"""

import json
import sys
from typing import Any, Dict, List


def find_and_fix_widgets(data: Dict[str, Any], target_widget_ids: List[str]) -> int:
    """
    Recursively search for widgets and fix their condition_operator if needed.
    
    Args:
        data: The loaded JSON data structure
        target_widget_ids: List of widget IDs to fix (empty list means fix all)
    
    Returns:
        Number of widgets fixed
    """
    fixed_count = 0
    
    # Navigate to devices -> [device_name] -> pages structure
    if 'data' not in data:
        print("Error: 'data' key not found in storage file")
        return fixed_count
    
    if 'devices' not in data['data']:
        print("Error: 'devices' key not found in data")
        return fixed_count
    
    # Iterate through all devices
    for device_name, device_data in data['data']['devices'].items():
        if 'pages' not in device_data:
            continue
            
        # Iterate through all pages
        for page_idx, page in enumerate(device_data['pages']):
            if 'widgets' not in page:
                continue
                
            # Iterate through all widgets
            for widget in page['widgets']:
                widget_id = widget.get('id', '')
                
                # Check if this widget needs fixing
                should_fix = False
                if target_widget_ids:
                    # Fix only specified widgets
                    should_fix = widget_id in target_widget_ids
                else:
                    # Fix all widgets with null condition_operator
                    should_fix = (
                        widget.get('condition_entity') and 
                        widget.get('condition_operator') is None
                    )
                
                if should_fix:
                    if widget.get('condition_entity') and widget.get('condition_operator') is None:
                        widget['condition_operator'] = '=='
                        print(f"Fixed widget '{widget_id}' in device '{device_name}', page {page_idx}")
                        fixed_count += 1
                    else:
                        print(f"Widget '{widget_id}' doesn't need fixing (operator={widget.get('condition_operator')})")
    
    return fixed_count


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    storage_file = sys.argv[1]
    target_widget_ids = sys.argv[2:] if len(sys.argv) > 2 else []
    
    # Load the storage file
    try:
        with open(storage_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {storage_file}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Error: Invalid JSON in {storage_file}: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Error reading file: {exc}")
        sys.exit(1)
    
    # Display file structure info
    print(f"Storage file structure:")
    print(f"  Top-level keys: {list(data.keys())}")
    if 'data' in data:
        print(f"  Data keys: {list(data['data'].keys())}")
        if 'devices' in data['data']:
            print(f"  Devices: {list(data['data']['devices'].keys())}")
    print()
    
    # Fix the widgets
    if target_widget_ids:
        print(f"Looking for specific widgets: {', '.join(target_widget_ids)}")
    else:
        print("Looking for all widgets with null condition_operator...")
    print()
    
    fixed_count = find_and_fix_widgets(data, target_widget_ids)
    
    if fixed_count == 0:
        print("No widgets needed fixing.")
        sys.exit(0)
    
    # Save the modified data back to the file
    try:
        with open(storage_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nSuccessfully fixed {fixed_count} widget(s) and saved to {storage_file}")
    except Exception as exc:
        print(f"\nError saving file: {exc}")
        sys.exit(1)


if __name__ == '__main__':
    main()
