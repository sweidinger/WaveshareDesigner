# Utility Scripts

This directory contains utility scripts for maintaining and troubleshooting the Waveshare Dashboard Designer.

## fix_widget_conditions.py

Fixes widget condition operators in the waveshare_dashboard storage file.

### Problem it Solves

When widgets have a `condition_entity` set but `condition_operator` is `null`, this can cause issues with conditional visibility. This script safely fixes those widgets by setting the operator to `==` (equality).

### Storage File Structure

The Home Assistant storage file has this structure:

```
{
  "version": 1,
  "minor_version": 1,
  "key": "waveshare_dashboard",
  "data": {
    "devices": {
      "device_name": {
        "pages": [
          {
            "widgets": [
              {
                "id": "w_...",
                "condition_entity": "sensor.example",
                "condition_operator": null  // <-- This gets fixed to "=="
              }
            ]
          }
        ]
      }
    }
  }
}
```

### Usage

**On local machine:**
```bash
# Fix specific widgets
python3 scripts/fix_widget_conditions.py /path/to/storage/file widget_id1 widget_id2

# Fix all widgets with null operators
python3 scripts/fix_widget_conditions.py /path/to/storage/file
```

**On remote Home Assistant (via SSH):**
```bash
# Copy the script to Home Assistant
scp scripts/fix_widget_conditions.py root@homeassistant.local:/tmp/

# Run it on the remote machine
ssh root@homeassistant.local "python3 /tmp/fix_widget_conditions.py /config/.storage/waveshare_dashboard"

# Or fix specific widgets
ssh root@homeassistant.local "python3 /tmp/fix_widget_conditions.py /config/.storage/waveshare_dashboard w_1763884148253_159"
```

### Safety Features

- ✅ Checks for file existence
- ✅ Validates JSON syntax
- ✅ Verifies expected data structure
- ✅ Only modifies widgets that need fixing
- ✅ Provides detailed output of changes
- ✅ Handles missing keys gracefully (no KeyError!)

### Example Output

```
Storage file structure:
  Top-level keys: ['version', 'minor_version', 'key', 'data']
  Data keys: ['devices']
  Devices: ['waveshare_display', 'reterminal_e1001']

Looking for specific widgets: w_1763884148253_159, w_1763884173316_9460

Fixed widget 'w_1763884148253_159' in device 'waveshare_display', page 0
Fixed widget 'w_1763884173316_9460' in device 'waveshare_display', page 0

Successfully fixed 2 widget(s) and saved to /config/.storage/waveshare_dashboard
```
