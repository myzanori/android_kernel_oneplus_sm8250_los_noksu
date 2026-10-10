#!/usr/bin/env bash
# scripts/bump.sh [major|minor|tag]
set -e
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VERSION_FILE="$ROOT_DIR/mystic_version.sh"

V=$(grep -oP 'MYSTIC_BASE="\K[^"]+' "$VERSION_FILE")
IFS=. read -r MA MI <<<"$V"
case "${1:-}" in
	major)
		MA=$((MA+1)); MI=0
		sed -i "s/^MYSTIC_BASE=.*/MYSTIC_BASE=\"$MA.$MI\"/" "$VERSION_FILE"
		echo "MYSTIC_BASE bumped to $MA.$MI"
		;;
	minor)
		MI=$((MI+1))
		sed -i "s/^MYSTIC_BASE=.*/MYSTIC_BASE=\"$MA.$MI\"/" "$VERSION_FILE"
		echo "MYSTIC_BASE bumped to $MA.$MI"
		;;
	tag)
		. "$VERSION_FILE"
		echo "Current derived version: $MYSTIC_VERSION"
		git tag -a "mystic-v$MYSTIC_VERSION" -m "Mystic Kernel v$MYSTIC_VERSION"
		echo "Created annotated tag: mystic-v$MYSTIC_VERSION"
		;;
	*)
		echo "Usage: $0 [major|minor|tag]"
		echo "  major : Bump MYSTIC_BASE from $V to $((MA+1)).0"
		echo "  minor : Bump MYSTIC_BASE from $V to $MA.$((MI+1))"
		echo "  tag   : Tag current HEAD commit with mystic-v<derived_version>"
		exit 1
		;;
esac
