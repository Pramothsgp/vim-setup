#!/usr/bin/env bash
# vim-setup uninstaller: unlinks ~/.vimrc, restores your previous config if
# there was one, and removes the lines install.sh added to your shell config.
#
#   ./uninstall.sh            keep downloaded plugins in ~/.vim
#   ./uninstall.sh --purge    also delete the plugins and the plugin manager
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIMRC_DST="$HOME/.vimrc"
MARK_BEGIN="# >>> vim-setup >>>"
MARK_END="# <<< vim-setup <<<"
PURGE=0
[ "${1:-}" = "--purge" ] && PURGE=1

ok()   { printf '\033[1;32m ok\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m !!\033[0m %s\n' "$*"; }

if [ -L "$VIMRC_DST" ] && [ "$(readlink "$VIMRC_DST")" = "$REPO_DIR/vimrc" ]; then
  rm "$VIMRC_DST"
  ok "removed ~/.vimrc link"
  latest="$(ls -1 "$HOME"/.vimrc.backup-* 2>/dev/null | sort | tail -1 || true)"
  if [ -n "$latest" ]; then
    mv "$latest" "$VIMRC_DST"
    ok "restored your previous config from $latest"
  fi
else
  warn "$VIMRC_DST isn't linked to this repo; left it alone"
fi

for rc in "$HOME/.zshrc" "$HOME/.bashrc"; do
  if [ ! -f "$rc" ] || ! grep -qF "$MARK_BEGIN" "$rc"; then continue; fi
  tmp="$(mktemp)"
  awk -v b="$MARK_BEGIN" -v e="$MARK_END" '
    $0 == b {skip=1; next} $0 == e {skip=0; next} !skip' "$rc" > "$tmp"
  cat "$tmp" > "$rc" && rm -f "$tmp"
  ok "removed vim-setup lines from $rc"
done

if [ "$PURGE" -eq 1 ]; then
  rm -rf "$HOME/.vim/plugged" "$HOME/.vim/autoload/plug.vim"
  ok "deleted plugins"
fi

echo "Git settings (core.editor, .ignore in your global gitignore) were left as they are."
