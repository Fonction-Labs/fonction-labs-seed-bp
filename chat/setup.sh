#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== BP Chat Setup ==="

# 1. Root dependencies (concurrently, etc.)
echo "→ Installing root dependencies..."
cd "$SCRIPT_DIR"
npm install

# 2. Frontend dependencies
echo "→ Installing frontend dependencies..."
cd "$SCRIPT_DIR/frontend"
npm install

# 2. Backend dependencies
echo "→ Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
uv sync

# 3. Symlink data/processed and docs/ from main repo
echo "→ Linking data/processed and docs/ from main repo..."
MAIN_REPO="$(echo "$PROJECT_ROOT" | sed 's/_chat$//')"
if [ ! -e "$PROJECT_ROOT/data/processed" ] && [ -d "$MAIN_REPO/data/processed" ]; then
    ln -sf "$MAIN_REPO/data/processed" "$PROJECT_ROOT/data/processed"
    echo "  → data/processed linked"
fi
if [ ! -e "$PROJECT_ROOT/docs" ] && [ -d "$MAIN_REPO/docs" ]; then
    ln -sf "$MAIN_REPO/docs" "$PROJECT_ROOT/docs"
    echo "  → docs/ linked"
fi

# 4. Link dashboard static files into frontend public/
echo "→ Linking dashboard into frontend public/..."
rm -rf "$SCRIPT_DIR/frontend/public/dashboard"
mkdir -p "$SCRIPT_DIR/frontend/public/dashboard"

# Copy dashboard HTML and assets
cp "$PROJECT_ROOT/dashboard/index.html" "$SCRIPT_DIR/frontend/public/dashboard/"
if [ -d "$PROJECT_ROOT/dashboard/assets" ]; then
    cp -r "$PROJECT_ROOT/dashboard/assets" "$SCRIPT_DIR/frontend/public/dashboard/"
fi
# Logo lives in assets/ (project root), not dashboard/assets/
if [ -f "$PROJECT_ROOT/assets/logo.png" ]; then
    cp "$PROJECT_ROOT/assets/logo.png" "$SCRIPT_DIR/frontend/public/dashboard/assets/"
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
