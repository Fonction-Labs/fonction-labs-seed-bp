#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== BP Chat Setup ==="

# 1. Frontend dependencies
echo "→ Installing frontend dependencies..."
cd "$SCRIPT_DIR/frontend"
npm install

# 2. Backend dependencies
echo "→ Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
uv sync

# 3. Link dashboard static files into frontend public/
echo "→ Linking dashboard into frontend public/..."
rm -rf "$SCRIPT_DIR/frontend/public/dashboard"
mkdir -p "$SCRIPT_DIR/frontend/public/dashboard"

# Copy dashboard HTML and assets
cp "$PROJECT_ROOT/dashboard/index.html" "$SCRIPT_DIR/frontend/public/dashboard/"
if [ -d "$PROJECT_ROOT/dashboard/assets" ]; then
    cp -r "$PROJECT_ROOT/dashboard/assets" "$SCRIPT_DIR/frontend/public/dashboard/"
fi

# 4. Check for OPENAI_API_KEY
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY not set. Export it before running:"
    echo "   export OPENAI_API_KEY=sk-..."
fi

echo ""
echo ""
echo "✅ Setup complete. Run with:"
echo "   cd $SCRIPT_DIR && npm run dev"
echo ""
echo "   Backend  → http://localhost:8002"
echo "   Frontend → http://localhost:3000"
