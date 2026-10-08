# vim-setup

Terminal Vim that works like VS Code: a file explorer on the left, open files as tabs along the top, fuzzy file search, project-wide search, go-to-definition, autocomplete, Git diff and blame, multiple cursors and a built-in terminal panel. One command sets it up on any Mac or Linux machine.

## Install

```bash
git clone https://github.com/<your-username>/vim-setup.git ~/.vim-setup
~/.vim-setup/install.sh
```

Open a new terminal, then open any project:

```bash
vim ~/projects/my-project
```

The installer is safe to run again; it only changes what isn't set up yet. It:

1. Installs `vim`, `fzf`, `ripgrep`, `bat`, `git` and `node` with Homebrew (macOS) or apt, dnf or pacman (Linux).
2. Moves any existing `~/.vimrc` to `~/.vimrc.backup-<date>`, then links `~/.vimrc` to this repo's `vimrc`.
3. Downloads the plugin manager and all plugins.
4. Adds `EDITOR=vim`, an alias `v=vim` and a `Ctrl-s` fix to `~/.zshrc` or `~/.bashrc`, and makes Git use Vim for commit messages.

| Option | Does |
| --- | --- |
| `--no-deps` | Skip installing packages (no sudo needed) |
| `--no-shell` | Don't touch shell config or Git settings |

On Windows, use it inside WSL.

## First steps

| Keys | Does |
| --- | --- |
| `Ctrl-p` | Find a file |
| `Space g` | Search the project |
| `Space e` | Toggle the explorer |
| `Shift-l` / `Shift-h` | Next / previous open file |
| `Space c` | Close the file |
| `Ctrl-s` | Save |
| `gd` / `Ctrl-o` | Go to definition / back |
| `Ctrl-t` | Terminal panel |

For go-to-definition and autocomplete, open a file of each language you use and run `:LspInstallServer` once.

Everything else is in **[CHEATSHEET.md](CHEATSHEET.md)**.

## Hiding files per project

`Space x` on an item in the explorer hides it; `:Hide node_modules *.log` hides by name. Each project keeps its own list in a `.ignore` file at its root, which also applies to `Ctrl-p` and `Space g`. The installer adds `.ignore` to your global gitignore so these lists never end up in commits.

## Customising one machine

Put machine-specific settings in `~/.vimrc.local`. It loads last and isn't part of the repo, for example:

```vim
set foldmethod=indent
colorscheme habamax
```

## Updating

```bash
cd ~/.vim-setup && git pull && ./install.sh --no-deps
```

Because `~/.vimrc` is a link into the repo, edits you make to `vimrc` here take effect immediately. Commit and push them to carry them to your other machines. Inside Vim, `:PlugUpdate` updates the plugins.

## Uninstall

```bash
~/.vim-setup/uninstall.sh           # restores your previous ~/.vimrc
~/.vim-setup/uninstall.sh --purge   # also deletes downloaded plugins
```

## Requirements

Vim 8.2 or newer (9.x recommended). For copy and paste to reach the system clipboard, Vim needs `+clipboard`: Homebrew's Vim has it, and on Linux desktops the installer picks `vim-gtk3`. Check with `vim --version | grep clipboard`.
