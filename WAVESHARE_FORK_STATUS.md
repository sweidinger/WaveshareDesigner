# Waveshare E-Paper Dashboard Designer - Fork Status

This is a fork of [ReTerminalDesigner](https://github.com/koosoli/ReTerminalDesigner) adapted to support Waveshare E-Paper displays with the Waveshare ESP32 Driver Board.

## Current Status: 🚧 Work in Progress

### ✅ Completed Changes

1. **Project Setup**
   - ✅ Cloned original repository
   - ✅ Created `waveshare-support` branch
   - ✅ Updated manifest.json with new domain and name
   - ✅ Created Waveshare ESP32 template (waveshare_esp32_template.yaml)

2. **Constants Updates**
   - ✅ Added DISPLAY_MODELS dictionary with common Waveshare displays:
     - 2.90in (296x128)
     - 4.20in (400x300)
     - 7.50in (640x384)
     - 7.50inV2 (800x480)
     - 7.50in-bV3-bwr (800x480 tri-color)
   - ✅ Changed domain from `reterminal_dashboard` to `waveshare_dashboard`

### 🔄 In Progress

1. **Directory Renaming**
   - [ ] Rename `custom_components/reterminal_dashboard/` to `custom_components/waveshare_dashboard/`
   - [ ] Update all internal imports

2. **YAML Generator Updates**
   - [ ] Update display platform from `reterminal` to `waveshare_epaper`
   - [ ] Update pin configurations to Waveshare ESP32 Driver Board:
     ```yaml
     cs_pin: GPIO15
     dc_pin: GPIO27
     busy_pin: GPIO25 (inverted: true)
     reset_pin: GPIO26
     spi:
       clk_pin: GPIO13
       mosi_pin: GPIO14
     ```
   - [ ] Make display model configurable via `${display_model}` variable
   - [ ] Remove reTerminal-specific hardware (buttons, sensors, buzzer)

3. **Config Flow**
   - [ ] Add display model selection dropdown
   - [ ] Update canvas dimensions based on selected model
   - [ ] Store selected model in device configuration

4. **Frontend Updates**
   - [ ] Make canvas size dynamic based on display model
   - [ ] Update URL from `/reterminal-dashboard` to `/waveshare-dashboard`
   - [ ] Add display model selector in UI

### 📋 TODO

1. **Core Functionality**
   - [ ] Test with actual Waveshare 7.5" V2 display
   - [ ] Add support for tri-color displays (red/black/white)
   - [ ] Add color picker for tri-color widgets

2. **Optional Hardware Support**
   - [ ] Make buttons optional (not included by default)
   - [ ] Make sensors optional
   - [ ] Add ability to configure custom GPIO pins

3. **Documentation**
   - [ ] Update README.md with Waveshare-specific instructions
   - [ ] Create pin mapping guide
   - [ ] Add troubleshooting section for common issues
   - [ ] Create example configurations for popular displays

4. **Testing**
   - [ ] Test with 2.9" display
   - [ ] Test with 4.2" display
   - [ ] Test with 7.5" displays (V1, V2, tri-color)
   - [ ] Test with different ESP32 boards

## Key Differences from ReTerminal

| Feature | ReTerminal E1001 | Waveshare ESP32 Driver Board |
|---------|------------------|------------------------------|
| Display Platform | `reterminal` | `waveshare_epaper` |
| Display Size | Fixed 800x480 | Multiple sizes supported |
| Color Support | Monochrome only | B/W, tri-color, 7-color |
| Built-in Buttons | Yes (GPIO 3,4,5) | No (optional external) |
| Built-in Sensors | Yes (SHT4x) | No (optional external) |
| Buzzer | Yes | No (optional external) |
| Battery Monitoring | Yes | No (can be added) |
| SPI Pins | Custom | GPIO13 (CLK), GPIO14 (MOSI) |
| CS Pin | GPIO10 | GPIO15 |
| DC Pin | GPIO11 | GPIO27 |
| Busy Pin | GPIO13 | GPIO25 (inverted) |
| Reset Pin | GPIO12 | GPIO26 |

## Installation (When Complete)

1. Add this repository to HACS as a custom repository
2. Search for "Waveshare E-Paper Dashboard Designer" and install
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration
5. Search for "Waveshare E-Paper Dashboard Designer"
6. Select your display model
7. Follow the configuration wizard

## Hardware Setup

### Required Hardware
- Waveshare E-Paper display (any supported model)
- Waveshare E-Paper ESP32 Driver Board
- USB cable for programming

### Hardware Configuration
1. **Set the hardware switch** on the ESP32 Driver Board:
   - Check your display's documentation for Position A or B
   - Most displays use Position B

2. **Connect the display**:
   - Plug the flat cable from your display into the ESP32 Driver Board connector

3. **Power**:
   - USB-C for programming and testing
   - Can be powered by battery (external)

## Contributing

This fork is in early development. Contributions welcome!

Priority areas:
1. Testing with different display models
2. Frontend canvas resizing implementation
3. Config flow for display model selection
4. Tri-color support

## Credits

- Original ReTerminal Designer by [@koosoli](https://github.com/koosoli)
- Waveshare fork adaptation in progress

## License

GPL-3.0 license (same as original)
