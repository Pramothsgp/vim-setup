#!/usr/bin/env bash
# vim-setup installer — macOS (Homebrew) and Linux (apt, dnf, pacman, zypper, apk).
# It asks what you want; every part is optional. Safe to run again any time,
# for example to change your choices.
#
#   ./install.sh                         ask about everything
#   ./install.sh --preset minimal        quick setup for a remote/SSH box
#   ./install.sh --yes                   no questions: keep previous choices (or Full)
#
# Options:
#   --preset full|developer|light|minimal
#   --with a,b   --without a,b           switch parts on/off (names below)
#   --yes, -y                            accept defaults, don't ask
#   --no-deps                            don't install packages (no sudo/brew)
#   --no-shell                           don't touch bash/zsh/fish config
#   --no-git-config                      don't change git settings
#   --install-ai                         install Claude Code / Copilot CLI if chosen and missing
#
# Parts: ui explorer finder editing git lsp copilot copilot_chat claude copilot_cli
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIMRC_SRC="$REPO_DIR/vimrc"
VIMRC_DST="$HOME/.vimrc"
CONF="$HOME/.vim-setup.conf"
MARK_BEGIN="# >>> vim-setup >>>"
MARK_END="# <<< vim-setup <<<"
FISH_CONF="$HOME/.config/fish/conf.d/vim-setup.fish"

PARTS="ui explorer finder editing git lsp copilot copilot_chat claude copilot_cli"
AI_PARTS="copilot copilot_chat claude copilot_cli"

label() {
  case "$1" in
    ui)           echo "Theme, status line and file tabs along the top" ;;
    explorer)     echo "Sidebar file explorer" ;;
    finder)       echo "Fuzzy file finder and project-wide search (fzf, ripgrep)" ;;
    editing)      echo "Editing extras: comments, surround, auto-close brackets, multiple cursors" ;;
    git)          echo "Git: diff, blame, staging, change markers in the gutter" ;;
    lsp)          echo "Code intelligence: go to definition, autocomplete, errors (needs Node.js)" ;;
    copilot)      echo "GitHub Copilot suggestions as you type (needs Node.js + Copilot plan)" ;;
    copilot_chat) echo "GitHub Copilot Chat window (needs Vim 9 + Copilot plan)" ;;
    claude)       echo "Claude Code side panel (needs Claude Code + Claude plan)" ;;
    copilot_cli)  echo "GitHub Copilot CLI agent panel (needs Copilot CLI + Copilot plan)" ;;
  esac
}

# ---------------------------------------------------------------- helpers
say()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m ok\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m !!\033[0m %s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

on()    { eval "[ \"\${P_$1:-0}\" = 1 ]"; }
set_p() { eval "P_$1=$2"; }

ASSUME_YES=0
INTERACTIVE=0
# Questions are read from the terminal, so this also works as `curl ... | bash`
if [ -t 1 ] && ( : </dev/tty ) 2>/dev/null; then
  exec 3</dev/tty
  INTERACTIVE=1
fi

# ask "Question" default(y|n) -> returns 0 for yes
ask() {
  local q="$1" def="$2" hint ans
  if [ "$ASSUME_YES" = 1 ] || [ "$INTERACTIVE" = 0 ]; then [ "$def" = y ]; return; fi
  if [ "$def" = y ]; then hint="[Y/n]"; else hint="[y/N]"; fi
  while true; do
    printf '%s %s ' "$q" "$hint"
    IFS= read -r ans <&3 || ans=""
    case "$(printf '%s' "${ans:-$def}" | tr '[:upper:]' '[:lower:]')" in
      y|yes) return 0 ;;
      n|no)  return 1 ;;
    esac
  done
}

# choose "Prompt" default -> echoes the number typed
choose() {
  local q="$1" def="$2" ans
  if [ "$ASSUME_YES" = 1 ] || [ "$INTERACTIVE" = 0 ]; then echo "$def"; return; fi
  printf '%s [%s] ' "$q" "$def" >&2
  IFS= read -r ans <&3 || ans=""
  echo "${ans:-$def}"
}

apply_preset() {
  local p
  for p in $PARTS; do set_p "$p" 0; done
  case "$1" in
    full)      for p in $PARTS; do set_p "$p" 1; done ;;
    developer) for p in ui explorer finder editing git lsp; do set_p "$p" 1; done ;;
    light)     for p in ui explorer finder editing git; do set_p "$p" 1; done ;;
    minimal)   ;;
    *) echo "Unknown preset: $1 (full, developer, light, minimal)"; exit 1 ;;
  esac
}

load_conf() {
  local p v
  for p in $PARTS; do
    v="$(sed -n "s/^VIM_SETUP_$(echo "$p" | tr '[:lower:]' '[:upper:]')=\([01]\).*/\1/p" "$CONF" | tail -1)"
    set_p "$p" "${v:-0}"
  done
}

apply_list() {   # apply_list "a,b" 1|0
  local item
  for item in $(echo "$1" | tr ',' ' '); do
    case " $PARTS " in
      *" $item "*) set_p "$item" "$2" ;;
      *) echo "Unknown part: $item (parts: $PARTS)"; exit 1 ;;
    esac
  done
}

any_plugins() {
  local p
  for p in ui explorer finder editing git lsp copilot copilot_chat; do on "$p" && return 0; done
  return 1
}
any_ai() { local p; for p in $AI_PARTS; do on "$p" && return 0; done; return 1; }
needs_node() { on lsp || on copilot; }

# Find a program the way you'd find it in your own shell: PATH, the usual
# install folders (native installers, Homebrew, npm/nvm/fnm/volta...), then
# by asking your login shell (catches aliases and PATH set in rc files).
find_tool() {
  local name="$1" p sh
  if have "$name"; then command -v "$name"; return 0; fi
  for p in "$HOME/.local/bin/$name" "$HOME/bin/$name" "/opt/homebrew/bin/$name" "/usr/local/bin/$name" \
           "$HOME/.claude/local/$name" "$HOME/.npm-global/bin/$name" "$HOME/.volta/bin/$name" \
           "$HOME/.bun/bin/$name" "$HOME/Library/pnpm/$name" "$HOME/.local/share/pnpm/$name" \
           "$HOME"/.nvm/versions/node/*/bin/"$name"; do
    if [ -x "$p" ]; then echo "$p"; return 0; fi
  done
  sh="${SHELL:-/bin/sh}"
  case "$(basename "$sh")" in
    fish)          p="$("$sh" -l -i -c "command -v $name; or functions $name" </dev/null 2>/dev/null || true)" ;;
    bash)          p="$("$sh" -l -i -c "[ -f ~/.bashrc ] && . ~/.bashrc >/dev/null 2>&1; alias $name 2>/dev/null; command -v $name" </dev/null 2>/dev/null || true)" ;;
    zsh|ksh)       p="$("$sh" -l -i -c "alias $name 2>/dev/null; command -v $name" </dev/null 2>/dev/null || true)" ;;
    *)             p="$("$sh" -l -c "command -v $name" </dev/null 2>/dev/null || true)" ;;
  esac
  for p in $(printf '%s' "$p" | tr "='\";" '    '); do
    p="${p/#\~/$HOME}"
    case "$p" in */"$name") if [ -x "$p" ]; then echo "$p"; return 0; fi ;; esac
  done
  return 1
}

# ---------------------------------------------------------------- options
PRESET=""; WITH=""; WITHOUT=""
DO_DEPS=1; DO_SHELL=1; DO_GITCONF=1; INSTALL_AI=0
while [ $# -gt 0 ]; do
  case "$1" in
    --preset)        PRESET="${2:-}"; shift ;;
    --preset=*)      PRESET="${1#*=}" ;;
    --with)          WITH="${2:-}"; shift ;;
    --with=*)        WITH="${1#*=}" ;;
    --without)       WITHOUT="${2:-}"; shift ;;
    --without=*)     WITHOUT="${1#*=}" ;;
    -y|--yes)        ASSUME_YES=1 ;;
    --no-deps)       DO_DEPS=0 ;;
    --no-shell)      DO_SHELL=0 ;;
    --no-git-config) DO_GITCONF=0 ;;
    --install-ai)    INSTALL_AI=1 ;;
    -h|--help)       sed -n '2,21p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1 (try --help)"; exit 1 ;;
  esac
  shift
done

# ---------------------------------------------------------------- choose parts
choose_parts() {
  local c p
  if [ -n "$PRESET" ]; then
    apply_preset "$PRESET"
  elif [ -f "$CONF" ]; then
    load_conf
    echo "Your current setup:"
    for p in $PARTS; do
      if on "$p"; then printf '   [x] %s\n' "$(label "$p")"; else printf '   [ ] %s\n' "$(label "$p")"; fi
    done
    if ! ask "Keep these choices?" y; then PRESET="ask"; fi
  else
    PRESET="ask"
  fi

  if [ "$PRESET" = ask ]; then
    if [ "$INTERACTIVE" = 1 ] && [ "$ASSUME_YES" = 0 ]; then
      cat <<'EOF'
Which setup do you want?
  1) Full       everything, including AI (Copilot suggestions and chat, Claude Code)
  2) Developer  everything except AI
  3) Light      explorer, file finder, git and editing extras; no language servers or AI
  4) Minimal    good settings and shortcuts only; no plugins, nothing downloaded
                (best for quick edits on a remote server over SSH)
  5) Custom     choose each part yourself
EOF
    fi
    while true; do
      c="$(choose "Choice" 1)"
      case "$c" in
        1) apply_preset full; break ;;
        2) apply_preset developer; break ;;
        3) apply_preset light; break ;;
        4) apply_preset minimal; break ;;
        5) apply_preset full
           echo "Choose each part:"
           for p in $PARTS; do
             if ask "  $(label "$p")?" y; then set_p "$p" 1; else set_p "$p" 0; fi
           done
           break ;;
      esac
    done
  fi
  [ -n "$WITH" ] && apply_list "$WITH" 1
  [ -n "$WITHOUT" ] && apply_list "$WITHOUT" 0
  return 0
}

write_conf() {
  local p
  {
    echo "# vim-setup: which parts are switched on (1) or off (0)."
    echo "# Edit this file or rerun $REPO_DIR/install.sh to change it."
    for p in $PARTS; do
      if on "$p"; then echo "VIM_SETUP_$(echo "$p" | tr '[:lower:]' '[:upper:]')=1"
      else echo "VIM_SETUP_$(echo "$p" | tr '[:lower:]' '[:upper:]')=0"; fi
    done
  } > "$CONF"
  ok "choices saved to $CONF"
}

# ---------------------------------------------------------------- packages
pkg_install() {   # pkg_install <brew names> -- <apt> -- <dnf> -- <pacman> -- <zypper> -- <apk>
  local sudo=""
  if [ "$(uname -s)" = Darwin ]; then
    if ! have brew; then
      warn "Homebrew not found (https://brew.sh). Skipping packages: install them yourself."
      return
    fi
    local pkg
    for pkg in $BREW_PKGS; do
      if brew list --formula "$pkg" >/dev/null 2>&1; then ok "$pkg already installed"; else brew install "$pkg"; fi
    done
    return
  fi
  if [ "$(id -u)" -ne 0 ]; then
    if have sudo; then sudo="sudo"; else warn "Not root and no sudo: skipping packages."; return; fi
  fi
  if have apt-get; then
    $sudo apt-get update -qq
    # shellcheck disable=SC2086
    $sudo env DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $APT_PKGS
  elif have dnf; then
    # shellcheck disable=SC2086
    $sudo dnf install -y $DNF_PKGS
  elif have pacman; then
    # shellcheck disable=SC2086
    $sudo pacman -S --needed --noconfirm $PACMAN_PKGS
  elif have zypper; then
    # shellcheck disable=SC2086
    $sudo zypper --non-interactive install $DNF_PKGS
  elif have apk; then
    # shellcheck disable=SC2086
    $sudo apk add $APT_PKGS
  else
    warn "Unknown package manager. Install these yourself: $APT_PKGS"
  fi
}

plan_packages() {
  local vimpkg="vim-nox"
  if [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then vimpkg="vim-gtk3"; fi   # clipboard on desktops
  BREW_PKGS="vim"; APT_PKGS="$vimpkg"; DNF_PKGS="vim-enhanced"; PACMAN_PKGS="vim"
  if any_plugins; then
    BREW_PKGS="$BREW_PKGS git"; APT_PKGS="$APT_PKGS git curl"
    DNF_PKGS="$DNF_PKGS git curl"; PACMAN_PKGS="$PACMAN_PKGS git curl"
  fi
  if on finder; then
    BREW_PKGS="$BREW_PKGS fzf ripgrep bat"; APT_PKGS="$APT_PKGS fzf ripgrep bat"
    DNF_PKGS="$DNF_PKGS fzf ripgrep bat"; PACMAN_PKGS="$PACMAN_PKGS fzf ripgrep bat"
  fi
  if needs_node && ! have node && [ -z "$(find_tool node || true)" ]; then
    BREW_PKGS="$BREW_PKGS node"; APT_PKGS="$APT_PKGS nodejs npm"
    DNF_PKGS="$DNF_PKGS nodejs npm"; PACMAN_PKGS="$PACMAN_PKGS nodejs npm"
  fi
}

check_vim() {
  if ! have vim; then warn "vim is not installed. Install it and run this again."; exit 1; fi
  local first ver
  first="$(vim --version | head -1)"
  ver="$(printf '%s' "$first" | sed -E 's/.*IMproved ([0-9]+)\.([0-9]+).*/\1\2/')"
  if [ "${ver:-0}" -lt 82 ]; then
    warn "$(printf '%s' "$first" | sed -E 's/.*(IMproved [0-9.]+).*/Vim \1/' | sed 's/IMproved //') is old; 8.2 or newer is needed for most parts."
  else
    ok "Vim $(printf '%s' "$first" | sed -E 's/.*IMproved ([0-9.]+).*/\1/')"
  fi
  if on copilot_chat && [ "${ver:-0}" -lt 90 ]; then warn "Copilot Chat needs Vim 9; it will stay off on this machine."; fi
  if vim --version | grep -q '+clipboard'; then ok "clipboard support"
  else
    warn "This Vim has no clipboard support: copy/paste won't reach the system clipboard."
    on copilot_chat && warn "Copilot Chat's sign-in needs a Vim with clipboard support (e.g. vim-gtk3, or Homebrew's vim)."
  fi
  if needs_node; then
    local node; node="$(find_tool node || true)"
    if [ -z "$node" ]; then warn "Node.js not found: code intelligence and Copilot suggestions won't work until it's installed."
    else ok "Node.js $("$node" --version 2>/dev/null) ($node)"; fi
  fi
  if on finder; then for t in fzf rg; do have "$t" || warn "$t not found: the file finder falls back to Vim's built-in :find."; done; fi
}

# ---------------------------------------------------------------- AI tools
setup_ai_tools() {
  local p
  if on claude; then
    if p="$(find_tool claude)"; then ok "Claude Code found ($p)"
    elif [ "$INSTALL_AI" = 1 ] || ask "Claude Code isn't installed. Install it now?" n; then
      curl -fsSL https://claude.ai/install.sh | bash && ok "Claude Code installed (sign in the first time you open it)"
    else
      warn "Claude panel is on, but Claude Code isn't installed: curl -fsSL https://claude.ai/install.sh | bash"
    fi
  fi
  if on copilot_cli; then
    if p="$(find_tool copilot)"; then ok "Copilot CLI found ($p)"
    elif [ "$INSTALL_AI" = 1 ] || ask "GitHub Copilot CLI isn't installed. Install it now?" n; then
      if have brew; then brew install --cask copilot-cli
      else curl -fsSL https://gh.io/copilot-install | bash; fi
      ok "Copilot CLI installed (type /login the first time you open it)"
    else
      warn "Copilot CLI panel is on, but the CLI isn't installed: brew install --cask copilot-cli"
    fi
  fi
}

# ------------------------------------------------------------------ config
link_config() {
  say "Linking ~/.vimrc"
  if [ -L "$VIMRC_DST" ] && [ "$(readlink "$VIMRC_DST")" = "$VIMRC_SRC" ]; then
    ok "already linked to $VIMRC_SRC"
  else
    if [ -e "$VIMRC_DST" ] || [ -L "$VIMRC_DST" ]; then
      local backup
      backup="$HOME/.vimrc.backup-$(date +%Y%m%d-%H%M%S)"
      mv "$VIMRC_DST" "$backup"
      ok "old config saved as $backup"
    fi
    ln -s "$VIMRC_SRC" "$VIMRC_DST"
    ok "$VIMRC_DST -> $VIMRC_SRC"
  fi
  mkdir -p "$HOME/.vim/undo"
  rm -f "$HOME/.vim/.tool-paths"   # re-detect AI tools and Node on next start
}

install_plugins() {
  if ! any_plugins; then ok "no plugins needed for this setup"; return; fi
  say "Installing Vim plugins"
  if [ ! -f "$HOME/.vim/autoload/plug.vim" ]; then
    curl -fsSLo "$HOME/.vim/autoload/plug.vim" --create-dirs \
      https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
  fi
  # t_Co: give headless Vim colours so the theme loads without errors
  vim -Es -i NONE --cmd 'set t_Co=256' -u "$VIMRC_DST" -c 'PlugInstall --sync' -c 'PlugClean!' -c 'qa!' </dev/null >/dev/null 2>&1 || true

  local missing
  missing="$(vim -Es -i NONE --cmd 'set t_Co=256' -u "$VIMRC_DST" \
    -c 'call writefile(exists("g:plugs") ? keys(filter(copy(g:plugs), "!isdirectory(v:val.dir)")) : [], "/dev/stdout")' \
    -c 'qa!' </dev/null 2>/dev/null || true)"
  if [ -n "$missing" ]; then
    warn "These plugins didn't download (network blocking GitHub?):"
    printf '%s\n' "$missing" | sed 's/^/      /'
    warn "Open vim and run :PlugInstall once you're on a network that allows GitHub."
  else
    ok "all plugins for your setup are installed"
  fi
}

# ------------------------------------------------------------ shell + git
add_block() {   # add_block <file> <content>
  local rc="$1"
  mkdir -p "$(dirname "$rc")"; touch "$rc"
  if grep -qF "$MARK_BEGIN" "$rc"; then ok "already in $rc"; return; fi
  printf '\n%s\n%s\n%s\n' "$MARK_BEGIN" "$2" "$MARK_END" >> "$rc"
  ok "added to $rc"
}

shell_setup() {
  say "Shell settings (EDITOR=vim, alias v, Ctrl-s fix)"
  local posix fish shname
  shname="$(basename "${SHELL:-}")"
  posix='export EDITOR=vim VISUAL=vim
alias v=vim
case $- in *i*) stty -ixon 2>/dev/null ;; esac   # lets Ctrl-s reach Vim'
  fish='set -gx EDITOR vim
set -gx VISUAL vim
alias v vim
status is-interactive; and stty -ixon 2>/dev/null   # lets Ctrl-s reach Vim'

  # Every shell you use: your login shell's file, plus any other that exists
  if [ "$shname" = zsh ] || [ -f "$HOME/.zshrc" ]; then add_block "$HOME/.zshrc" "$posix"; fi
  if [ "$shname" = bash ] || [ -f "$HOME/.bashrc" ]; then add_block "$HOME/.bashrc" "$posix"; fi
  if [ -f "$HOME/.bash_profile" ]; then add_block "$HOME/.bash_profile" "$posix"; fi
  if [ "$shname" = ksh ] || [ "$shname" = mksh ] || [ -f "$HOME/.kshrc" ]; then add_block "$HOME/.kshrc" "$posix"; fi
  if [ "$shname" = fish ] || have fish || [ -d "$HOME/.config/fish" ]; then
    if [ -f "$FISH_CONF" ]; then ok "already in $FISH_CONF"
    else mkdir -p "$(dirname "$FISH_CONF")"; printf '%s\n%s\n%s\n' "$MARK_BEGIN" "$fish" "$MARK_END" > "$FISH_CONF"; ok "added $FISH_CONF"; fi
  fi
  case "$shname" in
    zsh|bash|fish|ksh|mksh|"") ;;
    *) warn "Your shell ($shname) isn't set up automatically: set EDITOR=vim and an alias v=vim yourself." ;;
  esac
}

git_setup() {
  say "Git settings"
  if [ -z "$(git config --global core.editor || true)" ]; then
    if ask "Use Vim for Git commit messages?" y; then git config --global core.editor vim; ok "git now uses vim"; fi
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
  if grep -qxF ".ignore" "$excludes"; then ok ".ignore already in $excludes"
  else echo ".ignore" >> "$excludes"; ok "added .ignore to $excludes"; fi
}

# -------------------------------------------------------------------- run
echo
say "vim-setup"
choose_parts
any_ai || INSTALL_AI=0

if [ "$DO_DEPS" = 1 ]; then
  plan_packages
  if ask "Install the packages this setup needs ($BREW_PKGS)? Uses Homebrew or sudo." y; then
    say "Installing packages"; pkg_install
  else
    DO_DEPS=0
  fi
fi
if [ "$DO_SHELL" = 1 ] && ! ask "Add EDITOR=vim, an alias 'v' and the Ctrl-s fix to your shell config?" y; then DO_SHELL=0; fi
if [ "$DO_GITCONF" = 1 ] && ! have git; then DO_GITCONF=0; fi

say "Checking tools"
check_vim
write_conf
link_config
install_plugins
any_ai && setup_ai_tools
[ "$DO_SHELL" = 1 ] && shell_setup
[ "$DO_GITCONF" = 1 ] && git_setup

echo
say "Done. Open a new terminal, then:  vim ~/projects/<some-project>"
on copilot && echo "    Copilot suggestions: run :Copilot setup once inside Vim"
on copilot_chat && echo "    Copilot Chat: Space ai (signs in the first time)"
on claude && echo "    Claude Code panel: Space aa"
on copilot_cli && echo "    Copilot CLI panel: Space ag"
echo "    Change your choices any time: $REPO_DIR/install.sh"
echo "    Cheat sheet: $REPO_DIR/CHEATSHEET.md"
exit 0
