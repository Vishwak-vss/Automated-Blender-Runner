#!/bin/bash

# 1. Define variables
FILE_TO_RENDER="$1"
GDRIVE_DIR-="gdrive:BlenderRenderQueue/input"
COLAB_URL="https://colab.research.google.com/drive/1VtL7VuKJasQxtXDrdiBqRyjTEGXdnhPm?runAll=true"

if [ -z "$FILE_TO_RENDER" ]; then
    echo "Usage: ./submit_render.sh path/to/scene.blend"
    exit 1
fi

echo "🚀 Step 1: Sending $FILE_TO_RENDER to Google Drive..."
rclone copy "$FILE_TO_RENDER" "$GDRIVE_DIR"

echo "⏳ Step 2: Delaying for 10 seconds to ensure Drive syncs..."
sleep 10

echo "🖥️ Step 3: Opening Colab and triggering the render engine..."
# Opens the link in your default browser, which automatically triggers 'Run All'

if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
    start "$COLAB_URL"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "$COLAB_URL"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open "$COLAB_URL"
fi

echo "✅ Done! Colab is now rendering your file in the opened browser tab."