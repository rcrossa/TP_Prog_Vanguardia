#!/usr/bin/env bash
set -euo pipefail

# Directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}/.."
VENDOR_DIR="${ROOT_DIR}/static/js/vendor/markmap"

mkdir -p "${VENDOR_DIR}"

# Versions pinned for reproducibility
D3_VERSION="7.8.5"
MARKMAP_VIEW_VERSION="0.15.4"
MARKMAP_LIB_VERSION="0.15.4"

## Files to download (multiple mirrors)
D3_URLS=(
  "https://cdn.jsdelivr.net/npm/d3@${D3_VERSION}/dist/d3.min.js"
  "https://unpkg.com/d3@${D3_VERSION}/dist/d3.min.js"
)
MARKMAP_VIEW_URLS=(
  "https://cdn.jsdelivr.net/npm/markmap-view@${MARKMAP_VIEW_VERSION}/dist/browser/index.min.js"
  "https://cdn.jsdelivr.net/npm/markmap-view@${MARKMAP_VIEW_VERSION}/dist/browser/index.js"
  "https://unpkg.com/markmap-view@${MARKMAP_VIEW_VERSION}/dist/browser/index.min.js"
  "https://unpkg.com/markmap-view@${MARKMAP_VIEW_VERSION}/dist/browser/index.js"
)
MARKMAP_LIB_URLS=(
  "https://cdn.jsdelivr.net/npm/markmap-lib@${MARKMAP_LIB_VERSION}/dist/browser/index.min.js"
  "https://cdn.jsdelivr.net/npm/markmap-lib@${MARKMAP_LIB_VERSION}/dist/browser/index.js"
  "https://unpkg.com/markmap-lib@${MARKMAP_LIB_VERSION}/dist/browser/index.min.js"
  "https://unpkg.com/markmap-lib@${MARKMAP_LIB_VERSION}/dist/browser/index.js"
)

# Output paths
D3_FILE="${VENDOR_DIR}/d3.min.js"
MARKMAP_VIEW_FILE="${VENDOR_DIR}/markmap-view.min.js"
MARKMAP_LIB_FILE="${VENDOR_DIR}/markmap-lib.min.js"

# Download function supporting curl or wget
fetch_first_available() {
  local out="$1"; shift
  local last_err=1
  for url in "$@"; do
    echo "Intentando: $url"
    if command -v curl >/dev/null 2>&1; then
      if curl -fsSL "$url" -o "$out"; then
        return 0
      else
        last_err=$?
      fi
    elif command -v wget >/dev/null 2>&1; then
      if wget -q "$url" -O "$out"; then
        return 0
      else
        last_err=$?
      fi
    else
      echo "Error: necesita curl o wget instalado para descargar dependencias" >&2
      exit 1
    fi
  done
  return $last_err
}

echo "Descargando dependencias Markmap en ${VENDOR_DIR}..."
if fetch_first_available "$D3_FILE" "${D3_URLS[@]}"; then
  echo "- d3 ${D3_VERSION}"
else
  echo "Error descargando d3" >&2
  exit 1
fi

if fetch_first_available "$MARKMAP_LIB_FILE" "${MARKMAP_LIB_URLS[@]}"; then
  echo "- markmap-lib ${MARKMAP_LIB_VERSION}"
else
  echo "Error descargando markmap-lib" >&2
  exit 1
fi

if fetch_first_available "$MARKMAP_VIEW_FILE" "${MARKMAP_VIEW_URLS[@]}"; then
  echo "- markmap-view ${MARKMAP_VIEW_VERSION}"
else
  echo "Error descargando markmap-view" >&2
  exit 1
fi

echo "Listo. Archivos:"
ls -la "${VENDOR_DIR}"
