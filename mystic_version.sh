#!/usr/bin/env bash
# Mystic Kernel — versioning
# Single source of truth for Mystic Kernel branding
MYSTIC_BASE="1.0"                                   # bump by hand for major/minor
# Set to force an explicit build number (stable release); empty = git-derived.
MYSTIC_BUILD_OVERRIDE="42"

_last_tag="$(git describe --tags --abbrev=0 --match 'mystic-*' 2>/dev/null)"
if [ -n "$_last_tag" ]; then
	MYSTIC_BUILD="$(git rev-list --count "${_last_tag}..HEAD" 2>/dev/null || echo 0)"
	_tag_num="$(echo "$_last_tag" | sed 's/.*\.//')"
	MYSTIC_BUILD="$(( _tag_num + MYSTIC_BUILD ))"
else
	MYSTIC_BUILD="$(git rev-list --count HEAD 2>/dev/null || echo 1)"
fi

# If working tree has uncommitted changes, treat as upcoming build
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
	MYSTIC_BUILD="$((MYSTIC_BUILD + 1))"
fi

[ "$MYSTIC_BUILD" = "0" ] && MYSTIC_BUILD=1
[ -n "${MYSTIC_BUILD_OVERRIDE:-}" ] && MYSTIC_BUILD="$MYSTIC_BUILD_OVERRIDE"

export MYSTIC_NAME="Mystic Kernel"
export MYSTIC_AUTHOR="myzanori"
export MYSTIC_DEVICE="Kona"
export MYSTIC_PLATFORM="Kona"
export MYSTIC_ROM="Universal"
export MYSTIC_VERSION="${MYSTIC_BASE}.${MYSTIC_BUILD}"
# Stable build: MODVERSIONS=n, vendor-compat CRC, NoMount v2.1.0, SUSFS v2.3.0,
# ReSukiSU v4.1.0. Universal for OnePlus 9R (lemonades) + 8T (kebab).
export MYSTIC_FLAVOUR="ReSukiSU_SUSFS_Stable"

# full artifact prefix
export MYSTIC_PREFIX="Mystic_${MYSTIC_DEVICE}_${MYSTIC_AUTHOR}_${MYSTIC_ROM}_v${MYSTIC_VERSION}"
export MYSTIC_UNIFIED_PREFIX="Mystic_Kona_${MYSTIC_AUTHOR}_${MYSTIC_ROM}_v${MYSTIC_VERSION}"
export MYSTIC_LOCALVERSION="-perf-Mystic-Kona-myzanori-v${MYSTIC_VERSION}"

echo "Mystic Kernel Branding Loaded: $MYSTIC_PREFIX (LOCALVERSION: $MYSTIC_LOCALVERSION)"
