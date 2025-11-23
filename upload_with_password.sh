#!/bin/bash
# Quick upload script with embedded password

HA_HOST="10.0.1.175"
HA_USER="root"
HA_PASS="03_Nagster!"

echo "📤 Uploading updated files to Home Assistant..."

# Upload storage.py
echo "Uploading storage.py..."
expect << EOF
spawn scp /Users/stefan/Downloads/WaveshareDesigner/custom_components/waveshare_dashboard/storage.py ${HA_USER}@${HA_HOST}:/config/custom_components/waveshare_dashboard/storage.py
expect {
    "password:" {
        send "${HA_PASS}\r"
        exp_continue
    }
    "yes/no" {
        send "yes\r"
        exp_continue
    }
    eof
}
EOF

if [ $? -ne 0 ]; then
    echo "❌ storage.py upload failed"
    exit 1
fi

# Upload editor.js
echo "Uploading editor.js..."
expect << EOF
spawn scp /Users/stefan/Downloads/WaveshareDesigner/custom_components/waveshare_dashboard/frontend/editor.js ${HA_USER}@${HA_HOST}:/config/custom_components/waveshare_dashboard/frontend/editor.js
expect {
    "password:" {
        send "${HA_PASS}\r"
        exp_continue
    }
    "yes/no" {
        send "yes\r"
        exp_continue
    }
    eof
}
EOF

if [ $? -eq 0 ]; then
    echo "✅ Upload complete!"
    echo ""
    echo "⚠️  IMPORTANT: Restart Home Assistant for storage.py changes!"
    echo ""
    echo "Then:"
    echo "1. Hard refresh the dashboard (Cmd+Shift+R)"
    echo "2. Open browser console (Cmd+Option+I)"
    echo "3. Delete pages and click Save"
    echo "4. Check logs: Settings → System → Logs"
else
    echo "❌ editor.js upload failed"
    exit 1
fi
