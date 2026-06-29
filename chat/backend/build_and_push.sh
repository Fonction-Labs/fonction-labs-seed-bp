#!/usr/bin/env bash
# Build the backend Docker image and push to ECR.
# Usage: AWS_REGION=eu-west-3 ECR_REPO=<account>.dkr.ecr.<region>.amazonaws.com/bp-chat-backend ./build_and_push.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

: "${AWS_REGION:?Set AWS_REGION}"
: "${ECR_REPO:?Set ECR_REPO}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "=== 1/4  Run pipeline (regenerate data/processed + dashboard) ==="
cd "$REPO_ROOT"
uv run fonction-bp build --scenario vc_case

echo "=== 2/4  Prepare Docker build context ==="
# Copy data and context files into the backend directory (Docker COPY requires local paths)
rm -rf "$SCRIPT_DIR/data" "$SCRIPT_DIR/context"
mkdir -p "$SCRIPT_DIR/data/processed" "$SCRIPT_DIR/data/assumptions"
cp "$REPO_ROOT/data/processed/model.duckdb" "$SCRIPT_DIR/data/processed/"
cp "$REPO_ROOT/data/processed/model_outputs.json" "$SCRIPT_DIR/data/processed/"
cp "$REPO_ROOT/data/processed/validation_report.json" "$SCRIPT_DIR/data/processed/"
cp "$REPO_ROOT/data/assumptions/vc_case.yaml" "$SCRIPT_DIR/data/assumptions/"

mkdir -p "$SCRIPT_DIR/context/docs"
cp "$REPO_ROOT/CONTEXT_FOR_LLM.md" "$SCRIPT_DIR/context/"
cp "$REPO_ROOT/AGENT.md" "$SCRIPT_DIR/context/"
cp "$REPO_ROOT/docs/"T*.md "$SCRIPT_DIR/context/docs/" 2>/dev/null || true

echo "=== 3/4  Docker build ==="
cd "$SCRIPT_DIR"
docker build -t "bp-chat-backend:$IMAGE_TAG" .

echo "=== 4/4  Push to ECR ==="
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REPO"
docker tag "bp-chat-backend:$IMAGE_TAG" "$ECR_REPO:$IMAGE_TAG"
docker push "$ECR_REPO:$IMAGE_TAG"

echo ""
echo "✅  Pushed $ECR_REPO:$IMAGE_TAG"
echo "   Update your App Runner service to deploy the new image."

# Cleanup local copies (they're in the image now)
rm -rf "$SCRIPT_DIR/data" "$SCRIPT_DIR/context"
