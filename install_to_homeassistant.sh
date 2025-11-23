#!/bin/bash
# Installation script for Waveshare E-Paper Dashboard Designer
# This script copies the integration to your Home Assistant instance

set -e

echo "🎨 Waveshare E-Paper Dashboard Designer - Installation Script"
echo "=============================================================="
echo ""

# Default Home Assistant host
HA_HOST="${1:-homeassistant.local}"
HA_USER="${2:-root}"

echo "Target: $HA_USER@$HA_HOST"
echo ""

# Check if Home Assistant is reachable
if ! ping -c 1 "$HA_HOST" > /dev/null 2>&1; then
    echo "❌ Error: Cannot reach $HA_HOST"
    echo "Usage: $0 [hostname] [username]"
    echo "Example: $0 homeassistant.local root"
    exit 1
fi

echo "✅ Home Assistant is reachable at $HA_HOST"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if custom_components directory exists
if [ ! -d "$SCRIPT_DIR/custom_components/waveshare_dashboard" ]; then
    echo "❌ Error: custom_components/waveshare_dashboard not found!"
    exit 1
fi

echo "📦 Preparing files for installation..."
echo ""

# Create a temporary tarball
TEMP_TAR="/tmp/waveshare_dashboard_$(date +%s).tar.gz"
cd "$SCRIPT_DIR"
tar -czf "$TEMP_TAR" -C custom_components waveshare_dashboard

echo "📤 Uploading to Home Assistant..."
echo ""

# Copy to Home Assistant
scp "$TEMP_TAR" "$HA_USER@$HA_HOST:/tmp/"

if [ $? -ne 0 ]; then
    echo "❌ Failed to upload files"
    echo ""
    echo "💡 Tip: You may need to:"
    echo "   1. Enable SSH on your Home Assistant"
    echo "   2. Set up SSH keys, or"
    echo "   3. Use the correct username (try 'root' or your HA username)"
    exit 1
fi

# Extract on Home Assistant
echo "📂 Installing to /config/custom_components/..."
ssh "$HA_USER@$HA_HOST" << EOF
    mkdir -p /config/custom_components
    cd /config/custom_components
    tar -xzf /tmp/$(basename $TEMP_TAR)
    rm /tmp/$(basename $TEMP_TAR)
    ls -la /config/custom_components/waveshare_dashboard/ | head -10
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation complete!"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Restart Home Assistant"
    echo "   2. Go to Settings → Devices & Services"
    echo "   3. Click '+ Add Integration'"
    echo "   4. Search for 'Waveshare E-Paper Dashboard Designer'"
    echo "   5. Select your display model"
    echo "   6. Navigate to http://$HA_HOST:8123/waveshare-dashboard"
    echo ""
    echo "🎉 Happy dashboard designing!"
else
    echo "❌ Installation failed"
    exit 1
fi

# Cleanup
rm "$TEMP_TAR"
