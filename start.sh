#!/bin/bash
# ============================================================
#  CARYNTH — One-Click Startup Script
#  Run this before every demo / interview
#  Usage: bash start.sh  (from project root)
# ============================================================

echo ""
echo "  ██████╗ █████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗  ██╗"
echo " ██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║"
echo " ██║     ███████║██████╔╝ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║"
echo " ╚██████╗██║  ██║██║  ██║   ██║   ██║ ╚████║   ██║   ██║  ██║"
echo "  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝"
echo ""
echo "  Starting CARYNTH backend + ngrok tunnel..."
echo ""

# Step 1: Kill any previous instances
echo "  [1/3] Cleaning up old processes..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f ngrok 2>/dev/null
sleep 1

# Step 2: Start FastAPI backend in background
echo "  [2/3] Starting FastAPI backend on port 8000..."
cd "$(dirname "$0")/backend"
uvicorn main:app --port 8000 &
BACKEND_PID=$!
sleep 3

# Verify backend is up
if curl -s http://127.0.0.1:8000/ > /dev/null; then
    echo "  ✅ Backend is running (PID: $BACKEND_PID)"
else
    echo "  ❌ Backend failed to start. Check your Python environment."
    exit 1
fi

# Step 3: Start ngrok tunnel
echo "  [3/3] Starting ngrok tunnel..."
ngrok http 8000 --log=stdout > /tmp/ngrok_carynth.log 2>&1 &
NGROK_PID=$!
sleep 4

# Get the public URL
PUBLIC_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for t in d['tunnels']:
        if t['proto'] == 'https':
            print(t['public_url'])
            break
except:
    print('ERROR')
")

if [[ "$PUBLIC_URL" == "ERROR" || -z "$PUBLIC_URL" ]]; then
    echo "  ❌ ngrok failed to start. Check your token / network."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "  ============================================"
echo "  ✅ CARYNTH IS LIVE"
echo "  ============================================"
echo ""
echo "  🌐 Website :  https://carynth.vercel.app"
echo "  🔗 API URL  :  $PUBLIC_URL"
echo "  📡 Backend  :  http://127.0.0.1:8000"
echo "  📊 ngrok UI :  http://127.0.0.1:4040"
echo ""
echo "  Share carynth.vercel.app with anyone."
echo "  Keep this terminal open during the demo!"
echo "  Press Ctrl+C to shut everything down."
echo "  ============================================"
echo ""

# Keep alive and handle clean shutdown
trap "echo ''; echo '  Shutting down...'; kill $BACKEND_PID $NGROK_PID 2>/dev/null; exit 0" INT TERM

# Wait forever
wait $NGROK_PID
