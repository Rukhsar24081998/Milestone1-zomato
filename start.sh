#!/bin/zsh
# ─────────────────────────────────────────────────────────────────
#  Zomato AI – Start servers
#
#  Usage:
#    ./start.sh            → backend + Next.js frontend (default)
#    ./start.sh streamlit  → backend + Streamlit frontend
# ─────────────────────────────────────────────────────────────────

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-nextjs}"

echo ""
echo "🍽️  Starting Zomato AI Recommendations  (mode: $MODE)"
echo ""

# ── 1. Backend (always) ───────────────────────────────────────────
echo "▶ Starting backend on http://localhost:8000"
osascript -e "
  tell application \"Terminal\"
    activate
    do script \"cd '$PROJECT_DIR' && source .venv/bin/activate && uvicorn milestone_zomato_api.main:app --reload --port 8000\"
  end tell
"

sleep 2

# ── 2. Frontend ───────────────────────────────────────────────────
if [[ "$MODE" == "streamlit" ]]; then
  echo "▶ Starting Streamlit frontend on http://localhost:8501"
  osascript -e "
    tell application \"Terminal\"
      activate
      do script \"cd '$PROJECT_DIR' && source .venv/bin/activate && streamlit run streamlit_app/app.py --server.port 8501\"
    end tell
  "
  sleep 4
  echo "▶ Opening http://localhost:8501 in browser..."
  open http://localhost:8501
else
  echo "▶ Starting Next.js frontend on http://localhost:3000"
  osascript -e "
    tell application \"Terminal\"
      activate
      do script \"cd '$PROJECT_DIR/frontend-next' && npm run dev\"
    end tell
  "
  sleep 4
  echo "▶ Opening http://localhost:3000 in browser..."
  open http://localhost:3000
fi

echo ""
echo "✅ Done! Servers are running."
echo "   Backend  → http://localhost:8000"
if [[ "$MODE" == "streamlit" ]]; then
  echo "   Frontend → http://localhost:8501  (Streamlit)"
else
  echo "   Frontend → http://localhost:3000  (Next.js)"
fi
echo ""
echo "   To stop: close the Terminal windows that just opened."
echo ""
