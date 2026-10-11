#!/usr/bin/env bash
# Quick switch helper for Mystic Kernel development branches
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

usage() {
    echo "Usage: ./switch-branch.sh <target>"
    echo ""
    echo "Available targets:"
    echo "  universal  -> kona-universal-stable (OnePlus 9R/8T/8/8Pro Universal, OOS14 & ColorOS 17)"
    echo "  gaming     -> kona-gaming-unsigned  (Module signatures disabled for FPS/GPU .ko modules)"
    echo "  legacy-9r  -> main                 (Original v1.0.30 baseline for OnePlus 9R)"
    echo "  cos15      -> cos15-4.19.325-resukisu-susfs (ColorOS 15 branch)"
    echo "  upstream   -> upstream-latest      (Clean upstream tracking branch)"
    echo ""
    echo "Current active branch:"
    git branch --show-current
    exit 1
}

TARGET="${1:-}"

case "$TARGET" in
    universal)
        git checkout kona-universal-stable
        ;;
    gaming)
        git checkout kona-gaming-unsigned
        ;;
    legacy-9r)
        git checkout main
        ;;
    cos15)
        git checkout cos15-4.19.325-resukisu-susfs
        ;;
    upstream)
        git checkout upstream-latest
        ;;
    *)
        usage
        ;;
esac

echo ""
echo ">> Successfully switched to branch: $(git branch --show-current)"
