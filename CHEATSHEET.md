# Vim cheat sheet

Every command and shortcut for this setup, grouped by task. Space is the leader key. Keys are case-sensitive: `Shift-l` and `L` are the same thing.

## Shortcuts this setup adds

These come from this repo's `vimrc`; plain Vim doesn't have them.

| Keys | Does |
| --- | --- |
| `Ctrl-p` / `Space p` | Find a file anywhere in the project |
| `Space f` | Find a file in the current folder and below |
| `Space g` | Search text across the project |
| `Space b` | Pick from open files |
| `Space r` | Recently opened files |
| `Space /` | Search lines in this file |
| `Space e` / `Space E` | Toggle explorer / reveal current file in it |
| `Space x` / `Space X` | Hide item from explorer and search / edit the hidden list |
| `:Hide name` / `:Unhide name` | Hide / show by name or glob, e.g. `:Hide node_modules *.log` |
| `Space 1` … `Space 9` | Jump to file tab 1–9 |
| `Shift-l` / `Shift-h` | Next / previous file tab |
| `Space Tab` | Toggle between the last two files |
| `Space c` | Close the file, keep the layout |
| `Space w` / `Ctrl-s` | Save |
| `Space q` | Close window |
| `Space h` | Clear search highlight |
| `Space \` | Split editor side by side |
| `Ctrl-h` `Ctrl-j` `Ctrl-k` `Ctrl-l` | Move between windows |
| `Ctrl-t` / `Space t` | Toggle the terminal panel |
| `Ctrl-/` | Toggle comment |
| `Space gs` / `Space gb` / `Space gd` | Git status / blame / diff |
| `Space o` / `Space s` | Go to symbol in file / in project |
| `Space rn` / `Space ca` / `Space F` | Rename / code action / format |
| `Space d` | List problems in the file |
| `Space aa` / `Space ag` | Claude Code panel / Copilot CLI panel |
| `Space af` | Send this file or selection to the last-used agent panel |
| `Space ai` | Copilot Chat (visual: send selection) |
| `Space ac` / `Space ap` | Copilot suggestions on-off / suggestions panel |
| `jk` (insert mode) | Back to Normal mode |
| `J` / `K` (visual mode) | Move selected lines down / up |

### VS Code equivalents

| VS Code | Vim |
| --- | --- |
| Cmd-P | `Ctrl-p` |
| Cmd-Shift-F | `Space g` |
| Cmd-B / reveal in explorer | `Space e` / `Space E` |
| Ctrl-Tab | `Shift-l` / `Shift-h` |
| Cmd-1 … Cmd-9 | `Space 1` … `Space 9` |
| Cmd-W | `Space c` |
| Cmd-S | `Ctrl-s` |
| Cmd-/ | `Ctrl-/` |
| Cmd-D | `Ctrl-n` |
| Ctrl-` | `Ctrl-t` |
| Cmd-\ | `Space \` |
| F12 / Alt-F12 / Shift-F12 | `gd` / `gp` / `gr` |
| Cmd-Shift-O / Cmd-T | `Space o` / `Space s` |
| F2 / Cmd-. | `Space rn` / `Space ca` |
| Go back / forward | `Ctrl-o` / `Ctrl-i` |
| Problems panel | `Space d` |

## Files, saving and quitting

| Command | Does |
| --- | --- |
| `vim ~/projects/name` | Open a project with the explorer |
| `vim file.py` / `vim +42 file.py` | Open a file / open it at line 42 |
| `:e path` | Open a file (Tab completes) |
| `:e!` | Reload the file, discarding unsaved changes |
| `:enew` | New empty file |
| `:w` / `:w newname` | Save / save a copy under another name |
| `:saveas newname` | Save as, and switch to the new name |
| `:wa` | Save all open files |
| `:x` / `:wq` / `ZZ` | Save and close |
| `:q` / `:q!` / `ZQ` | Close / close without saving |
| `:qa` / `:qa!` / `:wqa` | Quit all / quit all without saving / save all and quit |
| `:cq` | Quit with an error (aborts a Git commit or rebase) |
| `gf` | Open the file path under the cursor |
| `Ctrl-g` | Show file name and position |
| `Ctrl-z` then `fg` | Suspend to the shell, then come back |

## Moving

Any motion takes a count: `5j` moves 5 lines down, `3w` 3 words forward.

| Keys | Moves to |
| --- | --- |
| `h` `j` `k` `l` | Left, down, up, right |
| `w` / `W` | Next word / next WORD (ignores punctuation) |
| `b` / `B` | Previous word / WORD |
| `e` / `E` / `ge` | End of word / WORD / previous word end |
| `0` / `^` / `$` | Line start / first non-blank / line end |
| `g_` | Last non-blank character |
| `f<c>` / `F<c>` | Onto next / previous `c` on the line |
| `t<c>` / `T<c>` | Just before next / after previous `c` |
| `;` / `,` | Repeat last `f` `t` `F` `T` forward / backward |
| `gg` / `G` / `42G` or `:42` | First line / last line / line 42 |
| `50%` | Halfway through the file |
| `{` / `}` | Previous / next blank line |
| `(` / `)` | Previous / next sentence |
| `%` | Matching bracket |
| `[(` / `])` / `[{` / `]}` | Enclosing parenthesis / brace |
| `H` / `M` / `L` | Top / middle / bottom of screen |
| `Ctrl-d` / `Ctrl-u` | Half page down / up |
| `Ctrl-f` / `Ctrl-b` | Full page down / up |
| `Ctrl-e` / `Ctrl-y` | Scroll one line without moving the cursor |
| `zz` / `zt` / `zb` | Put cursor line at middle / top / bottom of screen |
| `Ctrl-o` / `Ctrl-i` | Back / forward through jump history |
| `''` | Back to the line before the last jump |
| `` `. `` / `g;` / `g,` | Last change / older change / newer change |
| `gi` | Back to the last insert position, in Insert mode |
| `ma` / `` `a `` / `'a` | Set mark a / jump to it exactly / jump to its line |
| `mA` | Global mark A, works across files |
| `:marks` / `:jumps` | List marks / jump history |

## Editing

Operators combine with any motion or text object: `d` + `w` = delete word, `c` + `i"` = change inside quotes. Doubling an operator acts on the line (`dd`, `cc`, `yy`, `>>`).

### Entering Insert mode

| Keys | Starts typing |
| --- | --- |
| `i` / `a` | Before / after the cursor |
| `I` / `A` | Line start / line end |
| `o` / `O` | New line below / above |
| `s` / `S` | Replace character / whole line |
| `C` | Replace to end of line |
| `R` | Overtype mode (`Esc` to stop) |

### While in Insert mode

| Keys | Does |
| --- | --- |
| `Ctrl-w` / `Ctrl-u` | Delete word / line before the cursor |
| `Ctrl-o` + command | Run one Normal-mode command, stay in Insert |
| `Ctrl-r` + register | Paste a register (`Ctrl-r "` = last copy) |
| `Ctrl-n` / `Ctrl-p` | Complete from words in open files |
| `Ctrl-t` / `Ctrl-d` | Indent / outdent the line |
| `Ctrl-v` + key | Insert the key literally (e.g. a real Tab) |

### Operators

| Key | Operator |
| --- | --- |
| `d` | Delete (cut) |
| `c` | Change: delete, then Insert |
| `y` | Yank (copy) |
| `>` / `<` | Indent / outdent |
| `=` | Auto-indent |
| `gu` / `gU` / `g~` | Lowercase / uppercase / toggle case |
| `gc` | Toggle comment |
| `gq` | Re-wrap text to the line width |
| `!` | Filter through a shell command |

### Text objects (after an operator or `v`)

| Object | Inner (`i`) / around (`a`) |
| --- | --- |
| `iw` / `aw` | Word / word plus space |
| `iW` / `aW` | WORD (includes punctuation) |
| `is` / `as` | Sentence |
| `ip` / `ap` | Paragraph |
| `i"` `i'` `` i` `` / `a"` `a'` `` a` `` | Inside quotes / including quotes |
| `i(` `ib` / `a(` `ab` | Inside parentheses / including them |
| `i{` `iB` / `a{` `aB` | Inside braces / including them |
| `i[` / `a[` | Inside square brackets |
| `i<` / `a<` | Inside angle brackets |
| `it` / `at` | Inside an HTML/XML tag / the whole element |

### Single-key edits

| Keys | Does |
| --- | --- |
| `x` / `X` | Delete character under / before cursor |
| `r<c>` | Replace one character with `c` |
| `~` | Toggle case of the character |
| `J` / `gJ` | Join next line (with / without a space) |
| `D` | Delete to end of line |
| `Ctrl-a` / `Ctrl-x` | Increment / decrement the number under the cursor |
| `.` | Repeat the last change |
| `xp` / `ddp` | Swap two characters / two lines |

### Undo

| Keys | Does |
| --- | --- |
| `u` / `Ctrl-r` | Undo / redo |
| `U` | Undo all changes on the line |
| `:earlier 10m` / `:later 10m` | File as it was 10 minutes earlier / later |
| `:earlier 1f` | File as it was at the last save |

## Selecting, copying and repeating

### Visual mode

| Keys | Does |
| --- | --- |
| `v` / `V` / `Ctrl-v` | Select characters / lines / a block |
| `gv` | Reselect the last selection |
| `o` | Jump to the other end of the selection |
| `vip` / `vi"` | Select a paragraph / inside quotes |
| `d` `c` `y` `>` `<` `=` `~` `u` `U` | Act on the selection |
| `I` / `A` (block) | Insert / append on every line of the block |
| `$` then `A` (block) | Append at the end of lines of different lengths |
| `:` | Run a command on the selected lines |

### Copy and paste

Copies go straight to the system clipboard (when Vim is built with `+clipboard`).

| Keys | Does |
| --- | --- |
| `yy` / `yiw` / `y$` | Copy line / word / to end of line |
| `p` / `P` | Paste after / before the cursor |
| `gp` | Paste and move the cursor after it |
| `"0p` | Paste the last copy, even after deleting something |
| `"_d` | Delete without touching the clipboard |
| `"ay` / `"ap` | Copy into / paste from register a |
| `"Ay` | Add to register a |
| `:reg` | Show all registers |

### Multiple cursors

| Keys | Does |
| --- | --- |
| `Ctrl-n` | Select the word; press again to add the next match (like Cmd-D) |
| `n` / `N` | Add next / previous match |
| `q` / `Q` | Skip this match / remove this cursor |
| `\\A` | Select all matches |
| `Tab` | Switch between cursor mode and selection mode |
| `Esc` | Exit multi-cursor |

While the cursors are active, normal Vim commands like `c`, `i`, `A` and `d` act on every cursor.

### Macros

| Keys | Does |
| --- | --- |
| `qa` … `q` | Record keystrokes into register a |
| `@a` / `@@` | Play macro a / play the last macro again |
| `10@a` | Play it 10 times |
| `:'<,'>normal @a` | Play it on every selected line |

## Search and replace

| Keys | Does |
| --- | --- |
| `/text` / `?text` | Search forward / backward |
| `n` / `N` | Next / previous match |
| `*` / `#` | Search the word under the cursor forward / backward |
| `/\<word\>` | Whole-word search |
| `/text\C` | Force case-sensitive search |
| `Up` / `Down` after `/` | Browse search history |
| `cgn` then `.` | Change the next match, `.` repeats on each further match |
| `:s/old/new/` | First match on this line |
| `:s/old/new/g` | Every match on this line |
| `:%s/old/new/g` | Every match in the file |
| `:%s/old/new/gc` | Every match, asking each time (`y` `n` `a` all `q` quit) |
| `:'<,'>s/old/new/g` | Inside the selection |
| `:%s//new/g` | Replace whatever you last searched for |
| `:%s/\s\+$//e` | Remove trailing spaces |
| `:g/pattern/d` | Delete every line containing pattern |
| `:v/pattern/d` | Delete every line NOT containing pattern |
| `:g/pattern/normal A;` | Run a Normal command on every matching line |

### Project-wide search and replace

1. `Space g`, type the text; `Alt-a` selects all results (or `Tab` to pick some), then `Enter` sends them to the results list.
2. `:cdo s/old/new/g | update` replaces in every result and saves.

| Command | Moves through the results list |
| --- | --- |
| `:copen` / `:cclose` | Open / close the list |
| `:cnext` / `:cprev` | Next / previous result |
| `:cfirst` / `:clast` | First / last result |

## Explorer, finder, tabs and windows

### Explorer sidebar

| Keys | Does |
| --- | --- |
| Click or `o` / `Enter` | Open file, expand or collapse folder |
| `go` | Preview file, stay in the explorer |
| `s` / `i` | Open in a side-by-side / stacked split |
| `t` | Open in a new Vim tab page |
| `O` / `X` | Expand all below / collapse all |
| `x` | Collapse the parent folder |
| `p` / `P` | Go to parent / root |
| `C` | Make the selected folder the explorer root |
| `u` | Move the root up one folder |
| `m` | Menu: add, move/rename, delete, copy, reveal in Finder |
| `I` | Show / hide dotfiles |
| `R` / `r` | Refresh whole tree / this folder |
| `cd` | Set Vim's project folder to the selected folder |
| `q` | Close the explorer |
| `?` | List every explorer key |

In `m` → add: end the name with `/` to create a folder.

### File finder (Ctrl-p, Space g, Space b)

| Keys | Does |
| --- | --- |
| Type | Filter (fuzzy; `'word` = exact, `^start`, `end$`, `!exclude`) |
| `Ctrl-j` / `Ctrl-k` | Move down / up |
| `Enter` | Open |
| `Ctrl-v` / `Ctrl-x` / `Ctrl-t` | Open in side-by-side split / stacked split / tab page |
| `Tab` / `Alt-a` | Mark one / mark all (several files at once) |
| `Esc` | Cancel |

### File tabs (open buffers)

| Keys | Does |
| --- | --- |
| `Shift-l` / `Shift-h` | Next / previous tab |
| `Space 1` … `Space 9` | Jump to tab number |
| `Space Tab` | Last two files |
| `Space c` | Close this tab |
| `:bufdo bd` | Close all |
| `:ls` | List open files |

### Windows (splits)

| Keys | Does |
| --- | --- |
| `Space \` or `:vsp` / `:sp` | Split side by side / stacked |
| `Ctrl-h` `j` `k` `l` | Move between windows |
| `Ctrl-w w` | Cycle through windows |
| `Ctrl-w =` | Equal sizes |
| `Ctrl-w _` / `Ctrl-w \|` | Maximise height / width |
| `Ctrl-w +` / `-` / `>` / `<` | Taller / shorter / wider / narrower |
| `Ctrl-w H` `J` `K` `L` | Move this window far left / bottom / top / right |
| `Ctrl-w o` | Close all other windows |
| `Ctrl-w q` or `Space q` | Close this window |

### Terminal panel

| Keys | Does |
| --- | --- |
| `Ctrl-t` / `Space t` | Open or hide the terminal at the bottom |
| `Esc Esc` | Stop typing in the terminal so you can scroll and copy |
| `i` | Back to typing in the terminal |
| `:term` / `:vert term` | Extra terminal below / beside |

### Vim tab pages (separate layouts)

`:tabnew` opens one, `gt` / `gT` switch, `:tabclose` closes. Most people only need file tabs and splits.

## Code

Language features need a server: open a file of each language once and run `:LspInstallServer`.

### Navigation and refactoring

| Keys | Does |
| --- | --- |
| `gd` or `F12` | Go to definition (`Ctrl-o` back) |
| `gp` | Peek definition in a popup |
| `gr` or `Shift-F12` | All references |
| `gi` / `gt` | Implementation / type definition |
| `K` | Hover: type and docs |
| `Space o` / `Space s` | Symbol in this file / in the project |
| `Space rn` or `F2` | Rename everywhere |
| `Space ca` | Code action / quick fix |
| `Space F` | Format the file |
| `]g` / `[g` | Next / previous error |
| `Space d` | Problems list for the file |
| `:LspStatus` / `:LspInstallServer` | Check server / install one |

### Completion and brackets

| Keys | Does |
| --- | --- |
| `Tab` / `Shift-Tab` | Move through suggestions |
| `Enter` | Accept suggestion |
| `Ctrl-e` | Dismiss suggestions |
| `(` `[` `{` `"` `'` | Auto-closed; typing the closer steps over it |
| `Backspace` in `()` | Deletes both brackets |

### Comments and surroundings

| Keys | Does |
| --- | --- |
| `Ctrl-/` or `gcc` | Toggle comment on line |
| `gc` + motion, `gcip` | Comment a paragraph or selection |
| `ysiw"` | Surround word with quotes |
| `yss)` | Surround the whole line with parentheses |
| `S"` (visual) | Surround selection |
| `cs"'` / `cs({` | Change surrounding `"` → `'` / `(` → `{` |
| `ds"` / `ds(` | Delete surrounding quotes / parentheses |
| `cst<div>` / `dst` | Change / delete the surrounding tag |

### Indentation

| Keys | Does |
| --- | --- |
| `>>` / `<<` | Indent / outdent line |
| `>ip` / `=ip` | Indent / auto-indent paragraph |
| `gg=G` | Auto-indent the whole file |
| `:retab` | Convert tabs to spaces |

### Folding

| Keys | Does |
| --- | --- |
| `:set foldmethod=indent` | Fold by indentation (put in `~/.vimrc.local` to keep) |
| `za` | Toggle fold |
| `zc` / `zo` | Close / open fold |
| `zM` / `zR` | Close / open all folds |
| `zj` / `zk` | Next / previous fold |

### Spelling

| Keys | Does |
| --- | --- |
| `:set spell` / `:set nospell` | Spellcheck on / off |
| `]s` / `[s` | Next / previous misspelling |
| `z=` | Suggestions |
| `zg` / `zw` | Add word to dictionary / mark as wrong |

### Running code

| Command | Does |
| --- | --- |
| `:!python3 %` | Run this file (`%` = current file) |
| `:!npm test` | Run any shell command |
| `:r !date` | Insert a command's output |
| `:make` | Run `make`; errors go to the results list |

## Git

Diffs, blame, history, staging and conflicts all work inside Vim. Any git command also works as `:Git <command>`.

### Changes in this file (gutter markers)

| Keys | Does |
| --- | --- |
| `]c` / `[c` | Next / previous changed block |
| `Space hp` | Preview what changed in this block |
| `Space hs` | Stage just this block |
| `Space hu` | Undo this block back to the last commit |
| `vic` / `dac` | Select / delete the changed block |
| `:GitGutterFold` | Fold everything except changes |

### Diff

| Command | Shows |
| --- | --- |
| `Space gd` or `:Gdiffsplit` | This file vs the last commit, side by side |
| `:Gdiffsplit main` | This file vs the `main` branch |
| `:Gdiffsplit HEAD~3` | This file vs 3 commits ago |
| `:Git diff` | Full diff of all unstaged changes |
| `:Git diff --staged` | What you're about to commit |
| `:Git difftool -y main` | Every changed file vs `main`, one tab each |

Inside a diff: `]c` / `[c` jump between changes, `do` pulls the other side's version in, `dp` pushes yours across, `:diffoff` ends it.

### Who wrote this (blame and ownership)

| Command | Shows |
| --- | --- |
| `Space gb` or `:Git blame` | Author, date and commit beside every line |
| `Enter` (in blame) | Open that line's commit |
| `~` (in blame) | Blame the version before that commit |
| `g?` (in blame) | All blame keys |
| `:!git shortlog -sn -- %` | Everyone who has changed this file, most commits first |
| `:Git log -L .,.:%` | Every commit that touched the current line |
| `:e .github/CODEOWNERS` | The repo's owners file, if it has one (`/` to search for your path) |

### History

| Command | Shows |
| --- | --- |
| `:0Gclog` | Every version of this file; `:cnext` steps through them |
| `:Gclog` | Project commit history in the results list |
| `:Git log --oneline --graph` | Branch graph |
| `:Gedit main:%` | This file as it is on `main` (read-only) |

### Status, staging and commits

| Keys in `Space gs` | Does |
| --- | --- |
| `s` / `u` / `-` | Stage / unstage / toggle the file under the cursor |
| `=` | Show the file's diff inline |
| `dv` | Side-by-side diff of that file |
| `X` | Discard changes to that file |
| `cc` / `ca` / `ce` | Commit / amend / amend without editing message |
| `czz` / `czp` | Stash / pop stash |
| `g?` | All status keys |

| Command | Does |
| --- | --- |
| `:Gwrite` / `:Gread` | Stage this file / revert it to the last commit |
| `:Git push` / `:Git pull` | Push / pull |
| `:Git switch -c name` | New branch |
| `:GMove newname` / `:GDelete` | Rename / delete a tracked file |

### Merge conflicts

| Keys | Does |
| --- | --- |
| `:Gvdiffsplit!` | Three columns: yours, result, theirs |
| `]c` | Next conflict |
| `:diffget //2` / `:diffget //3` | Take your side / their side for this conflict |
| `:Gwrite` | Mark resolved and stage |

### In a rebase todo list (`git rebase -i`)

| Task | Keys |
| --- | --- |
| Change `pick` to `squash` | `ciw` `s` `Esc` |
| Same on the next line | `j` `.` |
| Drop a commit | `dd` |
| Move a commit down / up | `ddp` / `ddkP` |
| Finish / abort | `:x` / `:cq` |

## AI

### GitHub Copilot (grey suggestions as you type)

Run `:Copilot setup` once and sign in with GitHub.

| Keys | Does |
| --- | --- |
| `Tab` | Accept the suggestion (when the autocomplete menu is closed) |
| `Ctrl-]` | Dismiss the suggestion |
| `Ctrl-j` / `Ctrl-k` | Next / previous suggestion (also `Alt-]` / `Alt-[`) |
| `Ctrl-l` | Accept just the next word |
| `Space ap` or `:Copilot panel` | Window with up to 10 suggestions |
| `Space ac` | Turn suggestions on / off |
| `:Copilot status` | Check sign-in and whether it's working |

If the autocomplete menu is open, `Tab` moves through the menu instead; press `Ctrl-e` to close the menu, then `Tab` takes Copilot's suggestion.

### Copilot Chat (chat window)

| Keys | Does |
| --- | --- |
| `Space ai` | Open the chat (signs in the first time) |
| `Space ai` (visual) | Send the selected code to the chat |
| `Enter` (normal mode, in chat) | Send your message |
| `#file:` (in chat) | Attach a project file; Tab completes |
| `Space am` | Pick the model |
| `:CopilotChatReset` / `:CopilotChatSave name` / `:CopilotChatLoad name` | New chat / save / reopen a chat |

### Claude Code and Copilot CLI (agent panels)

| Keys | Does |
| --- | --- |
| `Space aa` | Open / hide the Claude Code panel on the right |
| `Space ag` | Open / hide the Copilot CLI panel |
| `Space af` | Type `@this/file.py` into the last-used panel, ready for your question |
| `Space af` (visual) | Same, plus the selected line numbers |
| `Ctrl-w h` / `Ctrl-w l` | Panel to editor / editor to panel |
| `Esc` (in Claude) | Interrupt Claude |
| `Shift-Tab` (in Claude) | Cycle permission modes, e.g. plan mode |
| `/login` (in Copilot CLI) | Sign in the first time |

Files the agents change reload in Vim automatically when you move back to them.

## Handy commands

| Command | Does |
| --- | --- |
| `:sort` / `:sort u` / `:sort n` | Sort lines / sort and remove duplicates / sort numerically (works on a selection) |
| `:'<,'>normal A,` | Run Normal keys on every selected line (here: add a comma) |
| `:%normal @a` | Run macro a on every line |
| `:r file` | Insert another file's contents |
| `:'<,'>w newfile` | Save the selected lines to a new file |
| `:'<,'>!jq .` | Replace the selection with a shell command's output (here: format JSON) |
| `:w !sudo tee %` | Save a file you opened without permission |
| `:set wrap` / `:set nowrap` | Wrap long lines on / off |
| `:set list` | Show tabs and trailing spaces |
| `:set ft=json` | Treat the file as another language |
| `:noh` | Clear highlights |
| `:help topic` | Vim's manual (`Ctrl-]` follows links, `Ctrl-o` back) |
| `:Maps` / `:Commands` | Fuzzy-search every shortcut / command |
| `:PlugInstall` / `:PlugUpdate` / `:PlugClean` | Install / update / remove plugins |
| `:source ~/.vimrc` | Reload the config without restarting |
| `@:` | Repeat the last `:` command |
| `q:` | Browse and edit command history |
