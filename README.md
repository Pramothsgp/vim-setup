# vim-setup

Terminal Vim that works like VS Code: a file explorer on the left, open files as tabs along the top, fuzzy file search, project-wide search, go-to-definition, autocomplete, GitHub Copilot suggestions and chat, Claude Code and Copilot CLI side panels, Git diff and blame, multiple cursors and a built-in terminal panel. One command sets it up on any Mac or Linux machine.

## Install

```bash
git clone https://github.com/Pramothsgp/vim-setup.git ~/.vim-setup
~/.vim-setup/install.sh
```

The installer asks what you want. Every part is optional:

| Setup | What you get | Good for |
| --- | --- | --- |
| **Full** | Everything below, including AI | Your main machine |
| **Developer** | Everything except AI | Machines without AI accounts |
| **Light** | Explorer, file finder, Git, editing extras | Servers where you still browse code |
| **Minimal** | Good settings and shortcuts only; no plugins, nothing downloaded | Quick edits over SSH |
| **Custom** | You pick each part | Anything else |

The parts: theme and file tabs, sidebar explorer, fuzzy finder and project search, editing extras, Git, code intelligence (language servers), Copilot suggestions, Copilot Chat, Claude Code panel, Copilot CLI panel.

It then asks whether to install the packages those parts need (Homebrew on macOS; apt, dnf, pacman, zypper or apk on Linux), whether to install Claude Code or the Copilot CLI if you chose their panels and they're missing, whether to add `EDITOR=vim`, a `v` alias and a `Ctrl-s` fix to your shells (bash, zsh, fish and ksh are all handled), and whether Git should use Vim for commit messages.

Your answers are saved in `~/.vim-setup.conf`. Run `install.sh` again at any time to change them; parts you switch off are removed.

### Without questions (scripts, servers)

```bash
./install.sh --preset minimal --yes          # quick setup on a remote box
./install.sh --preset full --yes --install-ai
./install.sh --yes --without copilot_cli     # keep your choices, drop one part
./install.sh --help                          # every option
```

Open a new terminal, then open any project:

```bash
vim ~/projects/my-project
```

On Windows, use it inside WSL.

## Learn it: Vim from 0 to 100

**[CHEATSHEET.md](CHEATSHEET.md)** takes you from your first `vim file` to working in it every day, in 14 levels. Every row shows the keys, where the cursor starts, the text before and after, and what happened. Every row that doesn't need a sign-in or a mouse is checked automatically against this config, so what it says is what Vim does.

First steps:

| Keys | Does |
| --- | --- |
| `Ctrl-p` | Find a file |
| `Space s` | Search the project |
| `Space e` | Toggle the explorer |
| `]b` / `[b` | Next / previous open file |
| `Space c` | Close the file |
| `Ctrl-s` | Save |
| `gd` / `Ctrl-o` | Go to definition / back |
| `Ctrl-t` | Terminal panel |

Leader keys are grouped so none is the start of another: single keys for files and windows, `Space l…` for code, `Space g…` for Git, `Space a…` for AI. For go-to-definition and autocomplete, open a file of each language you use and run `:LspInstallServer` once.

## Check it on your machine

```bash
~/.vim-setup/tests/run.sh            # every shortcut in the guide, about 5 minutes
~/.vim-setup/tests/run.sh git        # just the cases whose name matches
```

It runs each guide entry in a real Vim with your config, in a throwaway copy of a sample project, and reports any that behave differently. Parts you didn't install are skipped with the reason. Nothing in your own projects is touched. (Python 3 is needed to run it.)

## AI: Copilot and Claude

Each AI part is optional and chosen during install.

**Copilot suggestions** appear in grey as you type. Run `:Copilot setup` once and sign in with GitHub. Needs Node.js and a Copilot plan (there's a free tier, and verified students get free access).

**Copilot Chat** opens a chat window inside Vim (`Space ai`); select code and press `Space ai` to send it to the chat. It asks you to sign in the first time you open it. Needs Vim 9.

**Claude Code** and the **Copilot CLI** run as agent panels on the right that can read and edit your project. Install them during setup, or yourself:

```bash
curl -fsSL https://claude.ai/install.sh | bash        # Claude Code (Claude Pro, Max, Team, Enterprise or Console account)
brew install --cask copilot-cli                       # Copilot CLI (or: npm install -g @github/copilot)
```

Vim finds them however they were installed: native installers, Homebrew, npm (including under nvm, fnm, volta, asdf, mise, pnpm or bun), or an alias in your bash, zsh or fish config. If yours lives somewhere unusual, point to it in `~/.vimrc.local`:

```vim
let g:vim_setup_claude_path = '~/somewhere/claude'
let g:vim_setup_copilot_path = '~/somewhere/copilot'
```

| Keys | Does |
| --- | --- |
| `Tab` | Accept Copilot's suggestion (when the autocomplete menu is closed) |
| `Ctrl-]` | Dismiss the suggestion |
| `Ctrl-j` / `Ctrl-k` | Next / previous suggestion |
| `Ctrl-l` | Accept just the next word |
| `Space ap` / `Space ac` | Suggestions panel / suggestions on-off |
| `Space ai` | Open Copilot Chat; in visual mode, send the selection to it |
| `Space am` | Pick the Copilot Chat model |
| `Space aa` | Open / hide the Claude Code panel |
| `Space ag` | Open / hide the Copilot CLI panel |
| `Space af` | Type `@this/file` (plus selected lines) into the last-used agent panel |
| `Ctrl-w h` / `Ctrl-w l` | Between the editor and a panel |

Files the agents edit reload in Vim automatically.

## Hiding files per project

`Space x` on an item in the explorer hides it; `:Hide node_modules *.log` hides by name. Each project keeps its own list in a `.ignore` file at its root, which also applies to `Ctrl-p` and `Space s`. The installer adds `.ignore` to your global gitignore so these lists never end up in commits.

## Editing the guide

The guide is generated: each level lives in `guide/levels/`, where an entry holds its keys, the text before and after, and the explanation. After editing one, run `python3 guide/build.py` to rewrite CHEATSHEET.md, then `tests/run.sh` to check it.

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

Vim 8.2 or newer (9.x recommended; Copilot Chat needs 9). For copy and paste to reach the system clipboard, Vim needs `+clipboard`: Homebrew's Vim has it, and on Linux desktops the installer picks `vim-gtk3`. Check with `vim --version | grep clipboard`.
