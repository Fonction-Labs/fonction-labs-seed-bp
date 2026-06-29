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

# 3. Backend dependencies
echo "→ Installing backend dependencies..."
cd "$SCRIPT_DIR/backend"
uv sync

# 4. Symlink data/processed into chat/ (for backend DuckDB access)
echo "→ Linking data/processed from main repo..."
if [ ! -e "$SCRIPT_DIR/data" ]; then
    ln -sf "$PROJECT_ROOT/data/processed" "$SCRIPT_DIR/data"
    echo "  → data/ linked"
fi

# 5. Symlink docs/ into chat/ (for backend markdown context)
echo "→ Linking docs/ from main repo..."
if [ ! -e "$SCRIPT_DIR/docs" ]; then
    ln -sf "$PROJECT_ROOT/docs" "$SCRIPT_DIR/docs"
    echo "  → docs/ linked"
fi

# 6. Ensure logo.png is accessible from dashboard/assets/ (via symlink)
echo "→ Linking logo.png into dashboard/assets/..."
ln -sf "../../assets/logo.png" "$PROJECT_ROOT/dashboard/assets/logo.png" 2>/dev/null || true

# 7. Symlink dashboard into frontend/public/dashboard (live, no stale copies)
echo "→ Linking dashboard into frontend/public/dashboard..."
mkdir -p "$SCRIPT_DIR/frontend/public"
rm -rf "$SCRIPT_DIR/frontend/public/dashboard"
ln -sf "$PROJECT_ROOT/dashboard" "$SCRIPT_DIR/frontend/public/dashboard"
echo "  → dashboard/ symlinked (always live)"

# 7. Check for OPENAI_API_KEY
if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo ""
    echo "⚠️  OPENAI_API_KEY not set. Export it before running:"
    echo "   export OPENAI_API_KEY=sk-..."
fi

echo ""
echo "✅ Setup complete. Run with:"
echo "   cd $SCRIPT_DIR && npm run dev"
echo ""
echo "   Backend  → http://localhost:8002"
echo "   Frontend → http://localhost:3000  (dashboard + chat)"
