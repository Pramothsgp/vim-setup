#!/usr/bin/env bash
# vim-setup installer — macOS (Homebrew) and Linux (apt, dnf, pacman).
# Safe to run again at any time: it only changes what isn't set up yet.
#
#   ./install.sh              everything
#   ./install.sh --no-deps    skip installing packages (vim, fzf, ripgrep...)
#   ./install.sh --no-shell   don't touch ~/.zshrc / ~/.bashrc or git config
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIMRC_SRC="$REPO_DIR/vimrc"
VIMRC_DST="$HOME/.vimrc"
MARK_BEGIN="# >>> vim-setup >>>"
MARK_END="# <<< vim-setup <<<"
DO_DEPS=1
DO_SHELL=1

for arg in "$@"; do
  case "$arg" in
    --no-deps)  DO_DEPS=0 ;;
    --no-shell) DO_SHELL=0 ;;
    -h|--help)  sed -n '2,7p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $arg (try --help)"; exit 1 ;;
  esac
done

say()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m ok\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m !!\033[0m %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

# ---------------------------------------------------------------- packages
install_deps() {
  say "Installing packages"
  case "$(uname -s)" in
    Darwin)
      if ! have brew; then
        warn "Homebrew not found. Install it from https://brew.sh, then run this again."
        warn "Skipping packages for now."
        return
      fi
      for pkg in vim fzf ripgrep bat node git; do
        if brew list --formula "$pkg" >/dev/null 2>&1; then
          ok "$pkg already installed"
        else
          brew install "$pkg"
        fi
      done
      ;;
    Linux)
      local sudo=""
      if [ "$(id -u)" -ne 0 ]; then
        if have sudo; then sudo="sudo"; else
          warn "Not root and no sudo: skipping packages."; return
        fi
      fi
      if have apt-get; then
        # GUI build gives clipboard support on desktops; servers get the lighter one
        local vimpkg="vim-nox"
        if [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then vimpkg="vim-gtk3"; fi
        $sudo apt-get update -qq
        $sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq "$vimpkg" fzf ripgrep bat git curl nodejs npm
      elif have dnf; then
        $sudo dnf install -y vim-enhanced fzf ripgrep bat git curl nodejs npm
      elif have pacman; then
        $sudo pacman -S --needed --noconfirm vim fzf ripgrep bat git curl nodejs npm
      else
        warn "Unknown package manager. Install these yourself: vim fzf ripgrep bat git curl nodejs"
      fi
      ;;
    *)
      warn "Unsupported OS $(uname -s): skipping packages."
      ;;
  esac
}

check_vim() {
  if ! have vim; then
    warn "vim is not installed. Install it and run this again."; exit 1
  fi
  local ver
  ver="$(vim --version | head -1 | sed -E 's/.*IMproved ([0-9]+)\.([0-9]+).*/\1\2/')"
  if [ "${ver:-0}" -lt 82 ]; then
    warn "Vim $(vim --version | head -1 | sed -E 's/.*IMproved ([0-9.]+).*/\1/') is old; 8.2 or newer is needed for everything to work."
  else
    ok "Vim $(vim --version | head -1 | sed -E 's/.*IMproved ([0-9.]+).*/\1/')"
  fi
  if vim --version | grep -q '+clipboard'; then
    ok "clipboard support"
  else
    warn "This Vim has no clipboard support: copy/paste won't reach the system clipboard."
  fi
  for tool in fzf rg git curl; do
    have "$tool" || warn "$tool not found: some features won't work until it's installed."
  done
}

# ------------------------------------------------------------------ config
link_config() {
  say "Linking ~/.vimrc"
  if [ -L "$VIMRC_DST" ] && [ "$(readlink "$VIMRC_DST")" = "$VIMRC_SRC" ]; then
    ok "already linked to $VIMRC_SRC"
    return
  fi
  if [ -e "$VIMRC_DST" ] || [ -L "$VIMRC_DST" ]; then
    local backup
    backup="$HOME/.vimrc.backup-$(date +%Y%m%d-%H%M%S)"
    mv "$VIMRC_DST" "$backup"
    ok "old config saved as $backup"
  fi
  ln -s "$VIMRC_SRC" "$VIMRC_DST"
  ok "$VIMRC_DST -> $VIMRC_SRC"
  mkdir -p "$HOME/.vim/undo"
}

install_plugins() {
  say "Installing Vim plugins"
  if [ ! -f "$HOME/.vim/autoload/plug.vim" ]; then
    curl -fsSLo "$HOME/.vim/autoload/plug.vim" --create-dirs \
      https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  fi
  vim -Es -i NONE --cmd 'set t_Co=256' -u "$VIMRC_DST" -c 'PlugInstall --sync' -c 'qa!' >/dev/null 2>&1 || true

  local missing
  missing="$(vim -Es -i NONE --cmd 'set t_Co=256' -u "$VIMRC_DST" \
    -c 'call writefile(keys(filter(copy(g:plugs), "!isdirectory(v:val.dir)")), "/dev/stdout")' \
    -c 'qa!' 2>/dev/null || true)"
  if [ -n "$missing" ]; then
    warn "These plugins didn't download (network blocking GitHub?):"
    printf '%s\n' "$missing" | sed 's/^/      /'
    warn "Open vim and run :PlugInstall once you're on a network that allows GitHub."
  else
    ok "all plugins installed"
  fi
}

# ------------------------------------------------------------ shell + git
shell_setup() {
  say "Shell and git settings"
  local rc="$HOME/.bashrc"
  case "${SHELL:-}" in */zsh) rc="$HOME/.zshrc" ;; esac
  touch "$rc"
  if grep -qF "$MARK_BEGIN" "$rc"; then
    ok "already in $rc"
  else
    cat >> "$rc" <<EOF

$MARK_BEGIN
export EDITOR=vim VISUAL=vim
alias v=vim
[[ \$- == *i* ]] && stty -ixon 2>/dev/null   # lets Ctrl-s reach Vim
$MARK_END
EOF
    ok "added EDITOR, alias v and Ctrl-s fix to $rc"
  fi

  if [ -z "$(git config --global core.editor || true)" ]; then
    git config --global core.editor vim
    ok "git now uses vim for commit messages"
  else
    ok "git editor already set to $(git config --global core.editor)"
  fi

  # Each project's hidden-files list (.ignore) shouldn't end up in commits
  local excludes
  excludes="$(git config --global core.excludesfile || true)"
  if [ -z "$excludes" ]; then
    excludes="$HOME/.gitignore_global"
    git config --global core.excludesfile "$excludes"
  fi
  excludes="${excludes/#\~/$HOME}"
  touch "$excludes"
  if grep -qxF ".ignore" "$excludes"; then
    ok ".ignore already in $excludes"
  else
    echo ".ignore" >> "$excludes"
    ok "added .ignore to $excludes"
  fi
}

# -------------------------------------------------------------------- run
[ "$DO_DEPS" -eq 1 ] && install_deps
check_vim
link_config
install_plugins
[ "$DO_SHELL" -eq 1 ] && shell_setup

echo
say "Done. Open a new terminal, then:  vim ~/projects/<some-project>"
echo "    AI: run :Copilot setup once inside Vim; for Claude, install Claude Code"
echo "        (curl -fsSL https://claude.ai/install.sh | bash) and press Space aa"
echo "    Cheat sheet: $REPO_DIR/CHEATSHEET.md"
echo "    Update later: cd $REPO_DIR && git pull && ./install.sh --no-deps"
