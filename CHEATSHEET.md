# Vim from 0 to 100

A complete path from opening Vim for the first time to working in it every day, with this repo's setup. Work through the levels in order; each builds on the last.

## How to read this guide

- **`▌` is the cursor.** It sits on the character right after it: in `ca▌t` the cursor is on `t`. In Insert mode it's a thin bar between the two characters.
- **Keys:** `Ctrl-r` means hold Ctrl and press r. `Space` is the leader key: `Space p` means press Space, then p. Keys are case-sensitive: `A` means Shift-a. Commands starting with `:` end with `Enter`.
- **Cursor starts** says where to put the cursor before pressing the keys. **Before ↓ after** shows the text before and after. `·` stands for a space at the start of a line, `⇥` for a Tab.
- **Counts:** almost every command takes a number first: `3dd` deletes 3 lines, `5j` moves down 5.
- **Tested:** all 422 rows without † were run automatically in real Vim with this setup's Full install and gave exactly the result shown. Run `tests/run.sh` to check them on your own machine. The 19 rows marked † need a person (a sign-in, a mouse, macOS); the reason is given.

## This setup's shortcuts at a glance

Space is the leader key. Each is explained, with an example, in the levels below.

| | Keys | Does |
| --- | --- | --- |
| **Files** | `Ctrl-p` / `Space p` | Find a file in the project |
|  | `Space f` | Find a file in this folder |
|  | `Space s` | Search text in the project |
|  | `Space b` / `Space r` | Open files / recent files |
|  | `Space /` | Search lines in this file |
|  | `Space e` / `Space E` | Explorer / reveal this file |
|  | `]b` / `[b` | Next / previous file tab |
|  | `Space 1`…`9`, `Space Tab` | Go to tab N / last file |
|  | `Space c` | Close the file |
|  | `Ctrl-s` / `Space w` | Save |
|  | `Space x` / `Space X` | Hide from explorer and search / edit the list |
| **Windows** | `Space \` | Split side by side |
|  | `Ctrl-h/j/k/l` | Move between windows |
|  | `Space q` | Close window |
|  | `Ctrl-t` / `Space t` | Terminal panel |
|  | `Space h` | Clear search highlight |
| **Code (`Space l`…)** | `gd` / `F12` | Go to definition |
|  | `gr` / `Shift-F12` | References |
|  | `K` | Hover docs |
|  | `Space lp` / `li` / `lt` | Peek / implementation / type definition |
|  | `Space lr` / `F2` | Rename |
|  | `Space la` / `lf` | Code action / format |
|  | `Space lo` / `ls` | Symbol in file / project |
|  | `]g` / `[g`, `Space ld` | Next / previous problem, all problems |
|  | `Ctrl-/` | Toggle comment |
|  | `Ctrl-n` | Multiple cursors (in Normal mode) |
| **Git (`Space g`…)** | `Space gs` | Status |
|  | `Space gd` / `gb` / `gl` | Diff / blame / file history |
|  | `]c` / `[c` | Next / previous change |
|  | `Space gp` / `ga` / `gu` | Preview / stage / undo a change |
| **AI (`Space a`…)** | `Space aa` / `ag` | Claude Code / Copilot CLI panel |
|  | `Space af` | Send file or selection to the panel |
|  | `Space ai` / `am` | Copilot Chat / pick model |
|  | `Space ac` / `ap` | Copilot suggestions on-off / panel |
|  | `Tab` | Accept a Copilot suggestion |

## Levels

- [Level 0: Survival](#level-0-survival)
- [Level 1: Moving around](#level-1-moving-around)
- [Level 2: Basic edits](#level-2-basic-edits)
- [Level 3: The grammar: operator + motion](#level-3-the-grammar-operator--motion)
- [Level 4: Text objects](#level-4-text-objects)
- [Level 5: Visual mode, copy and paste](#level-5-visual-mode-copy-and-paste)
- [Level 6: Search and replace](#level-6-search-and-replace)
- [Level 7: Marks, jumps and macros](#level-7-marks-jumps-and-macros)
- [Level 8: Files, windows, tabs and the terminal](#level-8-files-windows-tabs-and-the-terminal)
- [Level 9: This setup's VS Code layer](#level-9-this-setups-vs-code-layer)
- [Level 10: Code: navigation, completion, folding, spelling](#level-10-code-navigation-completion-folding-spelling)
- [Level 11: Git](#level-11-git)
- [Level 12: AI](#level-12-ai)
- [Level 13: Command-line power](#level-13-command-line-power)
- [When a key doesn't work](#when-a-key-doesnt-work)

## Level 0: Survival

Enough to open a file, change it, save it and get out — and to recover when
something goes wrong. Vim starts in **Normal mode**, where keys are commands,
not text. You type text in **Insert mode**. If you ever feel lost, press
`Esc` twice: you're back in Normal mode and nothing else happens.

### Open and quit

Run these in your terminal (the first three) or inside Vim.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `vim notes.txt` | In your terminal | Vim opens `notes.txt` | Opens a file. If it doesn't exist yet, it's created when you save. |
| `vim +2 notes.txt` | In your terminal | Opens with the cursor on line 2 | Opens a file at a given line — handy with line numbers from error messages. |
| `vim src` | In your terminal, with a folder name | Explorer on the left, empty editor on the right; `src` becomes the project folder | Opens a folder like VS Code does. Every search and the explorer stay inside it. |
| `:w` Enter | Anywhere, in Normal mode | `▌changed text`<br>↓<br>`▌changed text` | Saves the file. |
| `:q` Enter | Anywhere, file saved | Vim closes | Quits. If there are unsaved changes, Vim refuses and says so — use `:q!` or `:wq`. |
| `:q!` Enter | Anywhere, with unsaved changes | Vim closes; the file on disk is unchanged | Quits and throws away unsaved changes. |
| `:wq` Enter  or  `:x` Enter  or  `ZZ` | Anywhere, with changes | Vim saves, then closes | Save and quit. `:x` and `ZZ` only write if something changed. |
| `ZQ` | Anywhere, with changes | Vim closes without saving | Same as `:q!`, in two keystrokes. |
| `:qa` / `:qa!` / `:wqa` Enter | With several files open | Vim closes every file: normally / discarding changes / after saving all | The `a` means all windows and files. |
| `:cq` Enter | Anywhere | Vim closes with an error code | Quit as a failure. When Git opened Vim for a commit message or a rebase, this cancels it. |

### Modes

The mode shows in the bottom-left corner (`NORMAL`, `INSERT`, `VISUAL`...).
In Insert mode the cursor is a thin bar, in Normal mode a block.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `i` … `Esc` | On the `w` of `world` | `Hello ▌world`<br>↓<br>`Hello Vim▌ world` | `i` starts typing before the cursor (here: `Vim` and a space). `Esc` goes back to Normal mode and steps the cursor back one. |
| `jk` | In Insert mode, while typing | `▌`<br>↓<br>`ab▌c` | Typing `j` then `k` quickly works like `Esc` — your hands never leave the home row. (Set up by this config.) |
| `v` | On the `b` | `a▌bcd`<br>↓<br>`a▌bcd` | Starts Visual mode to select text; move to grow the selection. `Esc` cancels. |
| `:` | Anywhere in Normal mode | The cursor jumps to the bottom line, ready for a command | Command-line mode, for commands like `:w`. `Esc` cancels, `Enter` runs it. |
| `R` … `Esc` | On the `a` | `▌abcd`<br>↓<br>`x▌ycd` | Replace mode: what you type overwrites the text instead of pushing it right. |
| `Esc` `Esc` | Anywhere, in any mode | `a▌bcd`<br>↓<br>`a▌bcd` | When you're not sure which mode you're in: two `Esc`s always land in Normal mode. |

### Undo and redo

Undo history is kept even after you close and reopen a file (this config saves it).

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `u` | Anywhere, after a change | `▌one two`<br>↓<br>`▌one two` | Undoes the last change. Here `dw` deleted `one `, then `u` brought it back. |
| `Ctrl-r` | Right after an undo | `▌one two`<br>↓<br>`▌two` | Redoes what you just undid. |
| `U` | On a line you just changed | `▌abc`<br>↓<br>`▌abc` | Undoes all recent changes on the current line at once (here two `x`s). |
| `5u` | Anywhere | `▌a b c d e f`<br>↓<br>`▌a b c d e f` | Any command takes a count: undo the last 5 changes. |
| `:earlier 1f` Enter | Anywhere, after saving and changing again | `saved`<br>↓<br>`▌saved` | Rewinds the whole file to how it was when you last saved. `:later 1f` goes forward again. You can also use time: `:earlier 10m`. |
| `:e!` Enter | Anywhere, with unsaved changes | `▌alpha`<br>↓<br>`▌alpha` | Reloads the file from disk, throwing away everything since the last save. |
| Undo after reopening | Save, quit, reopen the file, press `u` | Your change from the last session is undone | Undo history is stored on disk, so `u` still works tomorrow. |

### Help

Vim's manual is built in and excellent.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:help iw` Enter | Anywhere | A help window opens at the entry for `iw` (inner word) | `:help` plus any key, command or topic. `:q` closes help. |
| `Ctrl-]` | In a help window, on a link (text between `\|` bars) | Jumps to that topic | Follows a link. `Ctrl-o` goes back. |
| `Ctrl-o` | After following a help link | Back where you were | Goes back to the previous position (works everywhere, not just in help). |
| `vimtutor` | In your terminal | An interactive 30-minute lesson opens | The best first step: it teaches the basics by having you do them. †*Not checked automatically: Runs outside Vim; just type it in your terminal.* |

## Level 1: Moving around

In Normal mode you move with keys instead of the mouse or arrow keys. Start
with `h j k l`, then learn word and line jumps — they're what makes Vim fast.
Every motion takes a count: `3w` moves three words.

### Characters and lines

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `h` / `l` | On the `c` | `ab▌cd`<br>↓<br>`a▌bcd` | Left / right one character. (`l` would land on `d`.) |
| `j` / `k` | On the `b` of `abc` | `a▌bc`<br>`xyz`<br>↓<br>`abc`<br>`x▌yz` | Down / up one line, keeping the column. |
| `3l` | On the `a` | `▌abcdef`<br>↓<br>`abc▌def` | A count repeats the motion: 3 characters right. |
| `2j` | On line 1 | `▌one`<br>`two`<br>`three`<br>↓<br>`one`<br>`two`<br>`▌three` | Down 2 lines. |

### Words

A **word** is letters, digits and `_`; punctuation counts as its own word. A
**WORD** (capital keys) is anything between spaces.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `w` | On the `f` | `▌foo.bar baz`<br>↓<br>`foo▌.bar baz` | Start of the next word: `.` counts as a word. |
| `W` | On the `f` | `▌foo.bar baz`<br>↓<br>`foo.bar ▌baz` | Start of the next WORD: skips to after the space. |
| `b` | On the `b` of `baz` | `foo.bar ▌baz`<br>↓<br>`foo.▌bar baz` | Back to the start of the previous word. |
| `B` | On the `b` of `baz` | `foo.bar ▌baz`<br>↓<br>`▌foo.bar baz` | Back to the start of the previous WORD. |
| `e` | On the `f` | `▌foo bar`<br>↓<br>`fo▌o bar` | To the end of the word. |
| `E` | On the `f` | `▌foo.bar baz`<br>↓<br>`foo.ba▌r baz` | To the end of the WORD. |
| `ge` | On the `r` of `bar` | `foo ba▌r`<br>↓<br>`fo▌o bar` | Back to the end of the previous word. |

### Within the line

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `0` | Anywhere on the line | `····hello wor▌ld`<br>↓<br>`▌····hello world` | Very start of the line, even before the indent. |
| `^` | Anywhere on the line | `····hello wor▌ld`<br>↓<br>`····▌hello world` | First non-blank character: where the code starts. |
| `$` | Anywhere on the line | `▌hello world`<br>↓<br>`hello worl▌d` | Last character of the line. |
| `f,` | At the start | `▌call(a, b, c)`<br>↓<br>`call(a▌, b, c)` | **f**ind: jump onto the next `,` on this line. Works with any character. |
| `;` | After `f,` | `▌call(a, b, c)`<br>↓<br>`call(a, b▌, c)` | Repeats the last `f`/`t`/`F`/`T` — on to the next `,`. |
| `,` | After `f,` `;` | `▌call(a, b, c)`<br>↓<br>`call(a▌, b, c)` | Repeats it the other way. |
| `t,` | At the start | `▌call(a, b, c)`<br>↓<br>`call(▌a, b, c)` | **t**ill: jump to just before the next `,`. Great with `d` and `c` later. |
| `F(` | At the end | `call(a, b, ▌c)`<br>↓<br>`call▌(a, b, c)` | Like `f`, but backwards. |
| `T(` | At the end | `call(a, b, ▌c)`<br>↓<br>`call(▌a, b, c)` | Like `t`, but backwards: stops just after the `(`. |

### Whole file

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `gg` | Anywhere | `one`<br>`two`<br>`th▌ree`<br>↓<br>`▌one`<br>`two`<br>`three` | First line. |
| `G` | Anywhere | `o▌ne`<br>`two`<br>`three`<br>↓<br>`one`<br>`two`<br>`▌three` | Last line. |
| `2G`  or  `:2` Enter | Anywhere | `▌one`<br>`two`<br>`three`<br>↓<br>`one`<br>`▌two`<br>`three` | Go to line 2. Line numbers are on the left; relative numbers show how far other lines are, for `5j`-style jumps. |
| `50%` | Anywhere | `▌1`<br>`2`<br>`3`<br>`4`<br>↓<br>`1`<br>`▌2`<br>`3`<br>`4` | Jump to a percentage of the file: halfway. |
| `{` / `}` | In the first paragraph | `o▌ne`<br>`two`<br>*(empty line)*<br>`three`<br>↓<br>`one`<br>`two`<br>`▌`<br>`three` | Previous / next blank line — jumps between paragraphs or blocks of code. |
| `%` | On a bracket | `if ▌(a and (b or c)):`<br>↓<br>`if (a and (b or c)▌):` | Jumps to the matching bracket: `()`, `[]`, `{}`. |
| `[(` | Inside the parentheses | `f(a, ▌b)`<br>↓<br>`f▌(a, b)` | Back to the `(` that encloses the cursor. `])` goes to its `)`; `[{` and `]}` do the same for braces. |
| `]}` | Inside a `{ }` block | `if x {`<br>`··y = ▌1`<br>`}`<br>↓<br>`if x {`<br>`··y = 1`<br>`▌}` | Forward to the enclosing `}`. |
| `)` / `(` | In a sentence | `▌One. Two. Three.`<br>↓<br>`One. ▌Two. Three.` | Next / previous sentence. |

### Screen

This config keeps 8 lines visible above and below the cursor, so the screen
scrolls before you reach the edge.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-d` / `Ctrl-u` | Anywhere in a long file | The view and cursor move half a screen down / up | Half-page scrolling — the quickest way to read through a file. |
| `Ctrl-f` / `Ctrl-b` | Anywhere in a long file | A full screen down / up | Page down / page up. |
| `Ctrl-e` / `Ctrl-y` | Anywhere in a long file | The view scrolls one line; the cursor stays on its line | Scroll without moving the cursor (until it would leave the screen). |
| `zz` | Anywhere | The cursor's line moves to the middle of the window | Centre the screen on the cursor. `zt` puts it at the top, `zb` at the bottom (keeping the 8-line margin). |
| `H` / `M` / `L` | Anywhere | Cursor to the top / middle / bottom of the window | Jump to the screen's top, middle or bottom (8 lines from the edge, because of the margin). |

## Level 2: Basic edits

Ways into Insert mode, and single keys that change text without entering it.
The examples type `X` (or a word) and then press `Esc`; the result is what you
see after `Esc`, which steps the cursor back one character.

### Ways into Insert mode

Each starts typing at a different place. Pick the one that saves a move.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `i` | On the `c` | `ab▌cd`<br>↓<br>`ab▌Xcd` | Insert **before** the cursor. |
| `a` | On the `c` | `ab▌cd`<br>↓<br>`abc▌Xd` | **A**ppend after the cursor. |
| `I` | Anywhere on the line | `····ab▌cd`<br>↓<br>`····▌Xabcd` | Insert at the start of the text, after the indent. |
| `A` | Anywhere on the line | `ab▌cd`<br>↓<br>`abcd▌X` | Append at the end of the line. The one you'll use most. |
| `o` | Anywhere on the line | `ab▌c`<br>`xyz`<br>↓<br>`abc`<br>`ne▌w`<br>`xyz` | Open a new line **below** and start typing. |
| `O` | Anywhere on the line | `abc`<br>`x▌yz`<br>↓<br>`abc`<br>`ne▌w`<br>`xyz` | Open a new line **above**. |
| `s` | On the `c` | `ab▌cd`<br>↓<br>`ab▌Xd` | **S**ubstitute: delete the character, then type. |
| `S`  or  `cc` | Anywhere on the line | `····ab▌cd`<br>↓<br>`····ne▌w` | Replace the whole line's text, keeping its indent. |
| `C` | On the `c` | `ab▌cd`<br>↓<br>`ab▌X` | Change to the end of the line. |
| `gi` | Anywhere, after you inserted text somewhere else | `▌abc`<br>`xyz`<br>↓<br>`abcX▌Y`<br>`xyz` | Go back to where you last typed and keep typing there. Here: typed `X` at the end of line 1, moved down, then `gi` + `Y`. |

### While typing (Insert mode)

Small fixes without leaving Insert mode.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-w` | While typing | `▌`<br>↓<br>`one ▌` | Delete the word before the cursor. Here: typed `one two`, then `Ctrl-w`. |
| `Ctrl-u` | While typing | `▌`<br>↓<br>`▌` | Delete everything typed on this line. Here: typed `one two`, then `Ctrl-u`. |
| `Ctrl-o` + a command | While typing | `▌`<br>↓<br>`X▌ab` | Run one Normal-mode command and keep typing. Here: typed `ab`, then `Ctrl-o` `0` jumped to the line start, then typed `X`. |
| `Ctrl-t` / `Ctrl-d` | While typing | `▌`<br>↓<br>`····x▌` | Indent / unindent the current line. Here: typed `x`, then `Ctrl-t`. |
| `Ctrl-v` `Tab` | While typing | `▌`<br>↓<br>`⇥x▌` | Insert the next key literally. Here: `Ctrl-v` `Tab` put a real Tab character (not spaces), then typed `x`. |

### Single-key changes

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `x` | On the `c` | `ab▌cd`<br>↓<br>`ab▌d` | Delete the character under the cursor. |
| `X` | On the `c` | `ab▌cd`<br>↓<br>`a▌cd` | Delete the character before the cursor (like Backspace). |
| `rz` | On the `c` | `ab▌cd`<br>↓<br>`ab▌zd` | **R**eplace one character with `z` (or any key), without entering Insert mode. |
| `~` | On the `a` | `▌abc`<br>↓<br>`A▌bc` | Toggle upper/lower case and move right. Hold it to change a run of letters. |
| `J` | On line 1 | `▌one`<br>`two`<br>↓<br>`one▌ two` | **J**oin the next line onto this one, with a space between. |
| `gJ` | On line 1 | `▌one`<br>`two`<br>↓<br>`one▌two` | Join without adding a space. |
| `D` | On the `c` | `ab▌cd`<br>↓<br>`a▌b` | Delete from the cursor to the end of the line. |
| `dd` | Anywhere on the line | `o▌ne`<br>`two`<br>↓<br>`▌two` | Delete the whole line (it's kept for pasting with `p`). |
| `3x` | On the `a` | `▌abcdef`<br>↓<br>`▌def` | Counts work here too: delete 3 characters. |
| `2dd` | On line 1 | `▌one`<br>`two`<br>`three`<br>↓<br>`▌three` | Delete 2 lines. |

### Numbers

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-a` | Anywhere before or on the number | `▌x = 5`<br>↓<br>`x = ▌6` | Add 1 to the next number on the line — the cursor doesn't need to be on it. |
| `Ctrl-x` | Anywhere before or on the number | `▌x = 10`<br>↓<br>`x = ▌9` | Subtract 1. |
| `5` `Ctrl-a` | Anywhere before the number | `▌x = 5`<br>↓<br>`x = 1▌0` | Add 5. |

### Quick fixes

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `xp` | On the first of two swapped letters | `t▌eh`<br>↓<br>`th▌e` | Swap two characters: delete one, paste it after the next. |
| `ddp` | On the upper line | `▌one`<br>`two`<br>↓<br>`two`<br>`▌one` | Swap a line with the one below. |
| `ddkP` | On the lower line | `one`<br>`▌two`<br>↓<br>`▌two`<br>`one` | Swap a line with the one above. |

### Repeat: the dot

`.` repeats your last change, wherever the cursor is now. Make a change once,
then move and press `.` — this is how Vim users avoid typing anything twice.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `.` | After any change | `▌a b c`<br>↓<br>`▌c` | Here `dw` deleted `a `, then `.` deleted `b ` too. |
| `.` after Insert | After typing something | `▌one`<br>`two`<br>↓<br>`one;`<br>`two▌;` | Repeats a whole insert: here `A;` `Esc` on line 1, then `j` and `.` on line 2. |

## Level 3: The grammar: operator + motion

This is the idea that makes Vim click. An **operator** (what to do) followed
by a **motion** (how far) is a complete command: `d` + `w` deletes a word,
`c` + `$` changes to the end of the line, `y` + `}` copies to the end of the
paragraph. Learn one new operator and it works with every motion you know;
learn one new motion and it works with every operator. Doubling an operator
(`dd`, `cc`, `yy`, `>>`, `gUU`) applies it to the whole line.

### Delete: d

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `dw` | On the first letter of `one` | `▌one two`<br>↓<br>`▌two` | Delete to the start of the next word (the space goes too). |
| `de` | On the first letter of `one` | `▌one two`<br>↓<br>`▌·two` | Delete to the end of the word (the space stays). |
| `d$`  (same as `D`) | On the `e` of `one` | `on▌e two`<br>↓<br>`o▌n` | Delete to the end of the line. |
| `d0` | On the `w` of `two` | `one t▌wo`<br>↓<br>`▌wo` | Delete back to the start of the line. |
| `dt)` | On the `a` | `f(▌a, b)`<br>↓<br>`f(▌)` | Delete **till** the `)`: everything up to, not including, it. |
| `df,` | On the `a` | `▌a, b`<br>↓<br>`▌·b` | Delete up to and **including** the `,`. |
| `dj` | On line 1 | `▌1`<br>`2`<br>`3`<br>↓<br>`▌3` | Delete this line and the one below (vertical motions delete whole lines). |
| `dG` | On line 2 | `1`<br>`▌2`<br>`3`<br>↓<br>`▌1` | Delete to the end of the file. |
| `dgg` | On line 2 | `1`<br>`▌2`<br>`3`<br>↓<br>`▌3` | Delete to the start of the file. |
| `d}` | On line 1 | `▌a`<br>`b`<br>*(empty line)*<br>`c`<br>↓<br>`▌`<br>`c` | Delete to the end of the paragraph. |
| `d2w`  or  `2dw` | On the `a` | `▌a b c`<br>↓<br>`▌c` | A count can go before the operator or the motion. |

### Change: c

`c` deletes like `d`, then leaves you in Insert mode to type the replacement.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `cw` | On the first letter of `one` | `▌one two`<br>↓<br>`ne▌w two` | Change the word. (`cw` stops at the end of the word, like `ce`.) |
| `c$`  (same as `C`) | On the `t` | `one ▌two`<br>↓<br>`one ▌X` | Change to the end of the line. |
| `ct)` | On the `a` | `f(▌a, b)`<br>↓<br>`f(▌x)` | Change everything up to the `)`. |
| `cc` | Anywhere on the line | `····▌hello`<br>↓<br>`····▌X` | Change the whole line, keeping the indent. |

### Copy (yank): y — and paste: p

Vim calls copying **yanking**. `p` pastes after the cursor (below the line,
for whole lines), `P` before (above).

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `yw` then `P` | On the first letter of `one` | `▌one two`<br>↓<br>`one▌ one two` | Copy a word, then paste it in front of the cursor. |
| `yy` then `p` | Anywhere on line 1 | `▌one`<br>`two`<br>↓<br>`one`<br>`▌one`<br>`two` | Copy the line, paste it below. |
| `yy` then `P` | Anywhere on line 2 | `one`<br>`▌two`<br>↓<br>`one`<br>`▌two`<br>`two` | Copy the line, paste it above. |
| `y$` then `$p` | On the `t` of `two` | `one ▌two`<br>↓<br>`one twotw▌o` | Copy to the end of the line, then paste it at the end. The cursor lands on the last pasted character. |

### Indent: > and <

This config indents by 4 spaces (2 for web files).

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `>>` | Anywhere on the line | `▌if x:`<br>↓<br>`····▌if x:` | Indent the line. |
| `<<` | Anywhere on the line | `····▌x`<br>↓<br>`▌x` | Remove one level of indent. |
| `>j` | On line 1 | `▌a`<br>`b`<br>↓<br>`····▌a`<br>`····b` | Indent this line and the next. |
| `>ip` | Anywhere in the paragraph | `a`<br>`▌b`<br>*(empty line)*<br>`c`<br>↓<br>`····▌a`<br>`····b`<br>*(empty line)*<br>`c` | Indent the paragraph (`ip` is a text object — next level). |

### Case: gU, gu, g~

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `gUiw` | Anywhere in the word | `hel▌lo world`<br>↓<br>`▌HELLO world` | Uppercase the word. |
| `guu` | Anywhere on the line | `HELLO ▌World`<br>↓<br>`▌hello world` | Lowercase the whole line. |
| `gUU` | Anywhere on the line | `hello ▌world`<br>↓<br>`▌HELLO WORLD` | Uppercase the whole line. |
| `g~w` | On the first letter | `▌Hello world`<br>↓<br>`▌hELLO world` | Toggle the case of a word. |

### Format and filter

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `gqq` | Anywhere on a long line (here with the width set to 20) | `▌one two three four five six seven`<br>↓<br>`one two three four`<br>`▌five six seven` | Re-wrap the line to the text width. `gqip` re-wraps a paragraph. |
| `!ip` `sort` Enter | Anywhere in the paragraph | `c`<br>`▌b`<br>`a`<br>↓<br>`▌a`<br>`b`<br>`c` | Send the paragraph through a shell command and replace it with the output. Here `sort`. |

## Level 4: Text objects

Text objects let an operator act on a *thing* — a word, the text inside
quotes, a function call's arguments — no matter where in it the cursor is.
They start with `i` (**inside**) or `a` (**around**, including the quotes,
brackets or surrounding space). Use them after `d`, `c`, `y`, `v`, `gU`...
`ci"` (change inside quotes) is the one you'll use daily.

### Words and sentences

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `diw` | Anywhere in the word | `one tw▌o three`<br>↓<br>`one ▌ three` | Delete the word, leave the spaces. |
| `daw` | Anywhere in the word | `one tw▌o three`<br>↓<br>`one ▌three` | Delete the word and one space. |
| `ciw` | Anywhere in the word | `one tw▌o three`<br>↓<br>`one ne▌w three` | Change the word. |
| `diW` | Anywhere in the WORD | `a foo.b▌ar c`<br>↓<br>`a ▌ c` | A WORD includes punctuation: `foo.bar` goes as one. |
| `dis` | Anywhere in the sentence | `One. T▌wo here. Three.`<br>↓<br>`One. ▌ Three.` | Delete the sentence, leaving the spaces around it. `das` takes a space with it. |

### Quotes

Works from anywhere inside the quotes — or even before them on the same line.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `ci"` | Inside the quotes | `say("hel▌lo there")`<br>↓<br>`say("h▌i")` | Change inside double quotes. |
| `ci"` | Before the quotes, on the same line | `▌x = "old"`<br>↓<br>`x = "ne▌w"` | Vim looks ahead for the next quotes. |
| `di"` | Inside the quotes | `say("hel▌lo")`<br>↓<br>`say("▌")` | Delete inside double quotes. |
| `da"` | Inside the quotes | `x = "a▌b" + y`<br>↓<br>`x = ▌+ y` | Delete the quotes too, and the space after them. |
| `ci'` | Inside the quotes | `name = 'B▌ob'`<br>↓<br>`name = 'Alic▌e'` | Same for single quotes. |
| `` di` `` | Inside the backticks | `` run `l▌s -l` now ``<br>↓<br>`` run `▌` now `` | Same for backticks. |

### Brackets

`b` is short for `(`, and `B` for `{`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `di(`  or  `dib` | Anywhere inside the parentheses | `f(a, ▌b)`<br>↓<br>`f(▌)` | Delete the arguments. |
| `ci(` | Anywhere inside | `f(a, ▌b)`<br>↓<br>`f(▌x)` | Change the arguments. |
| `da(`  or  `dab` | Anywhere inside | `f(a, ▌b)`<br>↓<br>`▌f` | Delete the parentheses and what's in them. |
| `di{`  or  `diB` | Inside a `{ }` block | `if x {`<br>`····a = 1`<br>`····b▌ = 2`<br>`}`<br>↓<br>`if x {`<br>`▌}` | Delete everything inside the braces. |
| `ci{` | Inside a `{ }` block | `if x {`<br>`····▌a = 1`<br>`}`<br>↓<br>`if x {`<br>`····▌y`<br>`}` | Replace the block's contents. |
| `di[` | Inside the square brackets | `x[▌1, 2]`<br>↓<br>`x[▌]` | Delete inside `[ ]`. |
| `di<` | Inside the angle brackets | `List<Str▌ing>`<br>↓<br>`List<▌>` | Delete inside `< >`. |

### Tags and paragraphs

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `dit` | Anywhere inside the tag's text | `<p>he▌llo</p>`<br>↓<br>`<p>▌</p>` | Delete inside an HTML/XML tag. |
| `cit` | Anywhere inside | `<p>he▌llo</p>`<br>↓<br>`<p>by▌e</p>` | Change a tag's text. |
| `dat` | Anywhere inside | `x <b>b▌old</b> y`<br>↓<br>`x ▌ y` | Delete the whole element, tags included. |
| `dip` | Anywhere in the paragraph | `a`<br>`▌b`<br>*(empty line)*<br>`c`<br>↓<br>`▌`<br>`c` | Delete the paragraph (the lines up to a blank line). |
| `dap` | Anywhere in the paragraph | `a`<br>`▌b`<br>*(empty line)*<br>`c`<br>↓<br>`▌c` | Delete the paragraph and the blank line after it. |
| `yip` then `P` | Anywhere in the paragraph | `▌a`<br>`b`<br>*(empty line)*<br>`c`<br>↓<br>`▌a`<br>`b`<br>`a`<br>`b`<br>*(empty line)*<br>`c` | Copy a paragraph and paste it above. |

## Level 5: Visual mode, copy and paste

Visual mode is for when you want to *see* what you're about to change: select
first, then apply an operator. Then the **registers**: Vim's clipboards. Every
delete and copy lands in one; you can also name your own.

### Selecting

Move with any motion to grow the selection. `Esc` cancels.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `v` … `d` | On the `a` | `▌abcdef`<br>↓<br>`▌def` | Select characters (here 3 with `ll`), then delete them. |
| `V` … `d` | Anywhere on line 1 | `▌1`<br>`2`<br>`3`<br>↓<br>`▌3` | Select whole lines (here 2 with `j`), then delete. |
| `Ctrl-v` … `d` | On the first `x` | `a▌xb`<br>`axb`<br>`axb`<br>↓<br>`a▌b`<br>`ab`<br>`ab` | Select a block — a rectangle, column by column. Here the column of `x`s. |
| `gv` | After a selection ended | `▌abcd`<br>↓<br>`a▌bcd` | Reselect the last selection. |
| `o` | In a selection | `▌abcd`<br>↓<br>`▌abcd` | Jump to the other end of the selection, to grow it from that side. |
| `vip` | Anywhere in the paragraph | `a`<br>`▌b`<br>*(empty line)*<br>`c`<br>↓<br>`a`<br>`▌b`<br>*(empty line)*<br>`c` | Select a paragraph (any text object works: `vi"`, `va(`...). |
| `vi"` | Inside the quotes | `x = "he▌llo"`<br>↓<br>`x = "hell▌o"` | Select inside quotes. |

### Acting on a selection

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `U` / `u` / `~` | After selecting | `▌hello there`<br>↓<br>`▌HELLO there` | Uppercase / lowercase / toggle case of the selection. |
| `>` / `<` | After selecting lines | `▌a`<br>`b`<br>↓<br>`····a`<br>`▌····b` | Indent / unindent. This config keeps the selection, so press `>` again to indent more. |
| `J` / `K` | After selecting lines | `▌1`<br>`2`<br>`3`<br>↓<br>`2`<br>`▌1`<br>`3` | Move the selected lines down / up (this config). Keeps the selection. |
| `c` | After selecting | `▌hello there`<br>↓<br>`bye▌ there` | Change the selection. |
| `y` then `P` | After selecting | `▌ab cd`<br>↓<br>`a▌bab cd` | Copy the selection, then paste. |
| `:` with a selection | After selecting lines | `▌a1`<br>`a2`<br>`b3`<br>↓<br>`▌b1`<br>`b2`<br>`b3` | Vim fills in `:'<,'>` — the command runs only on the selected lines. Here `s/a/b/`. |

### Block selection (columns)

Edit many lines at once: select a column with `Ctrl-v`, then type once.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-v` … `I` | On the first character of the first line | `▌abc`<br>`abc`<br>`abc`<br>↓<br>`▌# abc`<br>`# abc`<br>`# abc` | Insert at the start of every selected line. The text appears on all lines after `Esc`. |
| `Ctrl-v` … `A` | On the first character | `▌ab`<br>`ab`<br>↓<br>`a▌b;`<br>`ab;` | Append after the block on every line. |
| `Ctrl-v` … `$A` | On the first character | `▌ab`<br>`abcd`<br>↓<br>`ab;`<br>`abcd;` | Append at the end of lines of different lengths. |
| `Ctrl-v` … `c` | On the `x` of line 1 | `a▌x1`<br>`ax2`<br>↓<br>`aY1`<br>`aY2` | Change the block on every line. |
| `g Ctrl-a` | After selecting lines of zeros | `▌0`<br>`0`<br>`0`<br>↓<br>`▌1`<br>`2`<br>`3` | Make a numbered sequence: each line gets 1 more than the one above. |

### Registers: Vim's clipboards

`p` pastes the unnamed register: whatever you last deleted or copied. With
this config, copying also puts the text on your system clipboard (when Vim
supports it — Homebrew's Vim does).

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `p` / `P` | On a line, after copying a line | `▌one`<br>`two`<br>↓<br>`one`<br>`▌one`<br>`two` | Paste after / before. Whole lines go below / above the cursor's line. |
| `gp` | After copying a line | `▌one`<br>`two`<br>↓<br>`one`<br>`one`<br>`▌two` | Paste, then put the cursor just after what was pasted. |
| `"0p` | After copying, then deleting something else | `▌keep`<br>`delete me`<br>↓<br>`keep`<br>`▌keep` | Register 0 always holds your last *copy*, even after deletes replaced the normal paste. |
| `"_dd` | On a line you want gone | `▌one`<br>`two`<br>↓<br>`one`<br>`▌one` | The `_` register is a black hole: delete without losing what you copied. Here: copy `one`, delete `two` into the hole, paste `one`. |
| `"ayy` / `"ap` | On a line | `▌one`<br>`two`<br>↓<br>`one`<br>`two`<br>`▌one` | Copy into register `a` (any letter), paste from it later — even after other copies. |
| `"Ayy` | On another line | `▌one`<br>`two`<br>↓<br>`one`<br>`two`<br>`▌one`<br>`two` | Capital letter **adds** to register `a` instead of replacing it. |
| `:reg` Enter | Anywhere | A list of every register and what's in it | See what you can paste. `:reg a` shows just `a`. |
| `Ctrl-r` `"` | In Insert mode | `▌one`<br>↓<br>`one on▌e` | Paste a register while typing (`"` = last copy; any register letter works). |
| `y` → `Cmd-V` elsewhere | After copying in Vim | The text pastes into other Mac apps | Copies go to the macOS clipboard, and `p` pastes what you copied in other apps. †*Not checked automatically: Needs Vim built with clipboard support on your Mac (Homebrew's is); this test machine's Vim has none.* |

## Level 6: Search and replace

Searching is also the fastest way to *move*: `/word` Enter jumps straight
there. This config ignores case unless you type a capital letter, and
highlights matches as you type.

### Search in the file

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `/foo` Enter | Anywhere | `▌a foo b foo`<br>↓<br>`a ▌foo b foo` | Jump to the next `foo`. |
| `?foo` Enter | Anywhere | `a foo b foo▌.`<br>↓<br>`a foo b ▌foo.` | Search backwards. |
| `n` / `N` | After a search | `▌a foo b foo`<br>↓<br>`a foo b ▌foo` | Next / previous match (here `n` after `/foo`). |
| `*` | On a word | `▌foo bar foo`<br>↓<br>`foo bar ▌foo` | Search for the word under the cursor, forwards. No typing needed. |
| `#` | On a word | `foo bar ▌foo`<br>↓<br>`▌foo bar foo` | Same, backwards. |
| `/\<is\>` Enter | Anywhere | `▌this is`<br>↓<br>`this ▌is` | `\<` and `\>` mark word edges: finds `is`, not the `is` inside `this`. |
| `/foo` finds `Foo` | Anywhere | `▌x Foo`<br>↓<br>`x ▌Foo` | Lowercase searches ignore case. |
| `/Foo` Enter | Anywhere | `▌foo Foo`<br>↓<br>`foo ▌Foo` | A capital letter makes the search match case exactly. |
| `/foo\C` Enter | Anywhere | `▌x Foo foo`<br>↓<br>`x Foo ▌foo` | `\C` anywhere in the search forces exact case. |
| `/` then `Up` | Anywhere | `▌x foo`<br>↓<br>`x ▌foo` | Browse earlier searches with the arrow keys. Here: searched `foo`, went back to the start, then `/` `Up` Enter. |
| `Space h` | After searching | The match highlighting disappears | Clear the highlight (until the next search). |

### Change every match, one at a time

Faster than `:s` when you want to check each one.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `cgn` then `.` | After searching (here `*` on `foo`, then `N` back to the first) | `▌foo x foo x foo`<br>↓<br>`bar x bar x bar` | `cgn` changes the next match; each `.` changes the one after. Press `n` to skip one. |

### Substitute: :s

`:s/old/new/` replaces text. `%` means every line; `g` every match on a line,
not just the first; `c` asks before each one.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:s/a/b/` Enter | On the line | `▌a a`<br>`a`<br>↓<br>`b a`<br>`a` | First match on this line. |
| `:s/a/b/g` Enter | On the line | `▌a a`<br>`a`<br>↓<br>`b b`<br>`a` | Every match on this line. |
| `:%s/a/b/g` Enter | Anywhere | `▌a a`<br>`a`<br>↓<br>`b b`<br>`b` | Every match in the file. |
| `:%s/a/b/gc` Enter, then `y` `n` `y` | Anywhere | `▌a a a`<br>↓<br>`b a b` | Ask before each one: `y` yes, `n` no, `a` all the rest, `q` stop. |
| `:%s//new/g` Enter | After a search | `▌old x old`<br>↓<br>`new x new` | An empty search part reuses your last search. |
| `:%s/\s\+$//e` Enter | Anywhere | `▌a  `<br>`b `<br>↓<br>`a`<br>`b` | Remove trailing spaces. `e` means don't complain if there are none. |
| `&` | On another line, after a `:s` | `▌a a`<br>`a a`<br>↓<br>`b a`<br>`b a` | Repeat the last `:s` on the current line. |
| `g&` | Anywhere, after a `:s` | `▌a a`<br>`a a`<br>↓<br>`b b`<br>`b b` | Repeat the last `:s` on every line. |
| `:%s/\v(\w+) (\w+)/\2 \1/` Enter | Anywhere | `▌hello world`<br>↓<br>`world hello` | Groups: `\v` lets you write `( )` plainly; `\1`, `\2` put back what each group matched. Here: swap two words. |
| `:s/, /\r/g` Enter | On the line | `▌a, b, c`<br>↓<br>`a`<br>`b`<br>`c` | `\r` in the replacement starts a new line. |

### Act on matching lines: :g and :v

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:g/x/d` Enter | Anywhere | `▌keep`<br>`x1`<br>`keep`<br>`x2`<br>↓<br>`keep`<br>`keep` | Delete every line containing `x`. |
| `:v/x/d` Enter | Anywhere | `▌keep`<br>`x1`<br>`keep`<br>`x2`<br>↓<br>`x1`<br>`x2` | Delete every line **not** containing `x`. |
| `:g/x/normal A;` Enter | Anywhere | `▌keep`<br>`x1`<br>`keep`<br>`x2`<br>↓<br>`keep`<br>`x1;`<br>`keep`<br>`x2;` | Run Normal-mode keys on every matching line. |

### Search the whole project

`Space s` searches every file (it uses ripgrep, so it's fast and skips
what's in `.gitignore` and your hidden list). The results can go to the
**quickfix list** — a list of places you can step through or edit all at once.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space s`, type, `Enter` | Anywhere in the project | A search window; Enter opens the file at the match | Type to filter the matching lines live; Enter jumps there. |
| `Space s`, type, `Alt-a`, `Enter` | Anywhere in the project | Every match goes into the quickfix list | `Alt-a` selects all results, then `Enter`. On a Mac, Alt must be set to send Esc: iTerm2 → Profiles → Keys → Left Option key: Esc+; Terminal.app → Settings → Profiles → Keyboard → Use Option as Meta key. |
| `:grep add` Enter | Anywhere in the project | Matches go into the quickfix list | Project search without the popup (also uses ripgrep here). Then `:copen` to see them. |
| `:cdo s/old/new/g \| update` Enter | After filling the quickfix list | Every listed line is changed and saved | Project-wide replace: search first, check the list, then run this. |
| `:copen` / `:cclose` Enter | After a project search | The quickfix list opens / closes at the bottom | Enter on a line in the list jumps there. |
| `:cnext` / `:cprev` Enter | After a project search | Next / previous match, opening its file | Step through the results. `:cfirst` and `:clast` jump to the ends. |

## Level 7: Marks, jumps and macros

Marks are bookmarks. Jumps are Vim's own history of where you've been. Macros
record keystrokes and replay them — the tool for any edit you need to repeat
on many lines.

### Marks

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `ma` … `` `a `` | Set it anywhere, jump from anywhere | `one ▌two`<br>`three`<br>↓<br>`one ▌two`<br>`three` | `ma` puts mark `a` at the cursor (any letter); `` `a `` jumps back to that exact spot. Here: set, go down, jump back. |
| `'a` | Anywhere, after setting mark `a` | `one ▌two`<br>`three`<br>↓<br>`▌one two`<br>`three` | Jump to the *line* of mark `a` (its first non-blank character). |
| `mA` … `` `A `` | In any file | Jumps to the other file, at the mark | Capital marks work across files — bookmark a file you keep coming back to. |
| `:marks` Enter | Anywhere | A list of your marks | See what's set. |

### Jumping back

Big moves (search, `G`, `%`, `gd`, opening another file...) are remembered,
so you can always get back.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-o` / `Ctrl-i` | After a jump | `▌1`<br>`2`<br>`3`<br>↓<br>`▌1`<br>`2`<br>`3` | Back / forward through the places you jumped from. Here: `G`, then `Ctrl-o` back. |
| `Ctrl-i` | After `Ctrl-o` | `▌1`<br>`2`<br>`3`<br>↓<br>`1`<br>`2`<br>`▌3` | Forward again. |
| `` `` `` | After a jump | `▌1`<br>`2`<br>`3`<br>↓<br>`▌1`<br>`2`<br>`3` | Toggle between here and where you jumped from. `''` does it by line. |
| `` `. `` | Anywhere | `▌abc`<br>`xyz`<br>↓<br>`abc`<br>`▌yz` | Jump to where you last changed something. |
| `g;` / `g,` | Anywhere | `▌a`<br>`b`<br>`c`<br>↓<br>`a`<br>`b▌!`<br>`c!` | Step back / forward through the places you changed. Here: changed lines 2 and 3, then `g;` `g;` back to line 2's change. |
| `:jumps` / `:changes` Enter | Anywhere | Lists of your jumps / your changes | See the history. |

### Macros: record and replay

`qa` starts recording into register `a` (any letter); `q` stops. `@a`
replays. End the recording by moving to the next line, so each replay
continues where the last one stopped.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `qa` … `q` then `@a` | On the first line | `▌a`<br>`b`<br>`c`<br>↓<br>`a;`<br>`b;`<br>`▌c` | Record: `A;` `Esc` `j` (add `;`, go down). Replay once on line 2. |
| `@@` | After playing a macro | `▌a`<br>`b`<br>`c`<br>↓<br>`a;`<br>`b;`<br>`c▌;` | Play the last macro again. |
| `3@a` | After recording | `▌1`<br>`2`<br>`3`<br>`4`<br>`5`<br>↓<br>`1;`<br>`2;`<br>`3;`<br>`4;`<br>`▌5` | Play it 3 times. |
| `:'<,'>normal @a` Enter | With lines selected | `▌a`<br>`b`<br>`c`<br>↓<br>`a;`<br>`b;`<br>`c;` | Play the macro on every selected line (no need to end it with `j`). Here: recorded on line 1, then selected lines 2–3. |
| `:%normal A;` Enter | Anywhere | `▌a`<br>`b`<br>↓<br>`a;`<br>`b;` | Run the same keys on every line — often quicker than a macro. |
| `@:` | After any `:` command | `▌a`<br>`b`<br>↓<br>`a!`<br>`b!` | Repeat the last command-line command. Here `:s/$/!/` on line 1, then `j` `@:`. |
| `q:` | Anywhere | A window listing your past commands; edit one and press Enter to run it | Command history you can edit like text. `:q` closes it. |

## Level 8: Files, windows, tabs and the terminal

An open file is a **buffer**. A **window** is a view onto a buffer — split
the screen and you have several windows. A **tab page** holds a whole layout
of windows. (The file tabs along the top in this setup are buffers; Level 9
covers them.)

### Opening and saving files

Press `Tab` while typing a file name to complete it.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:e notes.txt` Enter | Anywhere | notes.txt opens | **E**dit (open) a file. Paths work: `:e src/a.py`. |
| `:enew` Enter | Anywhere | A new empty, unnamed file | Save it later with `:w name`. |
| `:w copy.txt` Enter | In a file | copy.txt is written; you keep editing the original | Save a copy under another name. |
| `:saveas other.txt` Enter | In a file | Saved as other.txt, and you're now editing other.txt | Save As. |
| `:wa` Enter | With several changed files | All of them are saved | **W**rite **a**ll. |
| `gf` | On a file name in the text | That file opens | **G**o to **f**ile. |
| `Ctrl-^` | Anywhere | Back to the file you had open before | Flip between the last two files. |
| `Ctrl-g` | Anywhere | The file's name, line count and position appear at the bottom | Where am I? |
| `:r notes.txt` Enter | On the line to insert below | `▌top`<br>↓<br>`top`<br>`▌alpha`<br>`beta`<br>`gamma` | **R**ead another file into this one, below the cursor. |

### Leaving for a moment

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-z`, then `fg` | Anywhere in Normal mode | Vim pauses and you're back in the shell; `fg` returns to Vim exactly as you left it | Quick trip to the shell. (In other editors `Ctrl-z` is undo — in Vim, undo is `u`.) †*Not checked automatically: Suspends the test's own Vim; try it in your terminal.* |
| Mouse | Anywhere | Click to place the cursor, drag to select, scroll with the wheel | The mouse works in all modes in this setup. †*Not checked automatically: Needs a mouse.* |

### Buffers (open files)

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:ls` Enter | Anywhere | A numbered list of open files | `%` marks the current one, `#` the previous one. |
| `:b notes` Enter | Anywhere | Switches to notes.txt | Switch by part of the name; `Tab` completes. |
| `:bd` Enter | In a file | The file is closed (and its window, if it had its own) | **B**uffer **d**elete. In this setup `Space c` does it without closing the window. |
| `:%bd` Enter | Anywhere | Every file is closed | Close all files at once. |

### Windows (splits)

Several views side by side — of different files or the same one.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space \` | Anywhere | The window splits side by side | Split vertically (this config). Built in: `Ctrl-w v`. |
| `:sp notes.txt` / `:vsp notes.txt` Enter | Anywhere | notes.txt opens in a new window, below / beside | Split and open a file. Without a name, both windows show the current file. `Ctrl-w s` / `Ctrl-w v` also split. |
| `Ctrl-h` / `Ctrl-j` / `Ctrl-k` / `Ctrl-l` | With two or more windows | The cursor moves to the window on the left / below / above / right | Move between windows (this config; built in: `Ctrl-w` then `h` `j` `k` `l`). |
| `Ctrl-w w` | With two or more windows | The cursor goes to the next window | Cycle through windows, wrapping around at the end. |
| `Ctrl-w =` | After resizing | All windows get equal size | Even them out. |
| `Ctrl-w _` / `Ctrl-w \|` | In a split | This window takes all the height / width | Maximise for a moment; `Ctrl-w =` to restore. |
| `5 Ctrl-w +` / `-` / `>` / `<` | In a split | 5 lines taller / shorter, or 5 columns wider / narrower | Resize by steps. |
| `Ctrl-w H` / `J` / `K` / `L` | In a split | The window moves to the far left / bottom / top / right | Rearrange the layout: here a top/bottom split becomes side by side. |
| `Ctrl-w o` | In one of several windows | Only this window is left | Close all **o**ther windows (files stay open). |
| `Ctrl-w q`  or  `Space q` | In a split | This window closes | Close the window. |

### Tab pages

Each tab page is a separate layout of windows. Most people only need splits.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:tabnew` Enter | Anywhere | A new tab page with an empty window | Also `:tabnew file`. |
| `gt` / `gT` | With several tab pages | Next / previous tab page | Switch tab pages. |
| `Ctrl-w T` | In a split | That window moves to its own tab page | Pull a window out into a tab. |
| `:tabclose` Enter | In a tab page | The tab page closes | Close it (the files stay open). |

### Terminal panel

A shell inside Vim, like VS Code's terminal. While you're typing in it, keys
go to the shell; `Ctrl-w` then `h`/`j`/`k`/`l` moves to another window.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-t`  or  `Space t` | Anywhere | A terminal opens at the bottom, ready to type | Toggle the terminal panel (this config). It keeps running when hidden. |
| `Ctrl-t` (in the panel) | While typing in the terminal | The panel hides; the shell keeps running | Toggle it off again. |
| Type a command, Enter | In the terminal panel | The command runs in your shell | It's a normal shell. |
| `Esc` `Esc` | In the terminal panel | You can scroll and copy the output with Vim keys | Leave typing mode (this config, only in this panel). `i` goes back to typing. |
| `i` | In the panel, after `Esc` `Esc` | Typing goes to the shell again | Back to typing. |
| `Ctrl-w k` | Typing in the terminal panel | The cursor moves to the editor above | Leave the terminal without closing it. |
| `:term` / `:vert term` Enter | Anywhere | An extra terminal opens below / beside | As many terminals as you like; `exit` closes one. |

## Level 9: This setup's VS Code layer

Everything in this level comes from this repo's config: an explorer sidebar,
a fuzzy file finder, file tabs, comments, surround and multiple cursors. Open
a project with `vim ~/projects/name` to get the VS Code layout.

### Explorer sidebar

Inside the explorer, keys act on the file or folder under the cursor. Move
with `j`/`k` or search with `/`, like in any buffer.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space e` | Anywhere | The explorer opens on the left (press again to close) | Toggle the explorer. |
| `Space E` | In a file | The explorer opens with that file highlighted | Reveal the current file in the explorer. |
| Click | On a file or folder in the explorer | Opens the file / expands the folder | A single click works, like VS Code. †*Not checked automatically: Needs a mouse.* |
| `o`  or  `Enter` | On a file | The file opens in the editor on the right | Open. |
| `o`  or  `Enter` | On a folder | The folder expands (press again to collapse) | Open or close a folder. |
| `go` | On a file | The file opens, but the cursor stays in the explorer | Preview without leaving the explorer. |
| `s` / `i` | On a file | Opens it in a new split beside / below | Open in a split. |
| `t` | On a file | Opens it in a new tab page | Open in a tab page. |
| `O` | On a folder (or the top line) | Everything inside opens, all levels down | Expand all. |
| `X` | On a folder (or the top line) | Everything inside collapses | Collapse all. |
| `x` | On a file inside an open folder | Its folder collapses | Close the parent folder. |
| `p` / `P` | On a file inside a folder | The cursor jumps to its folder / to the top | Go to parent / root. |
| `C` | On a folder | The explorer shows only that folder | Make it the explorer's top. `u` goes back up a level. |
| `u` | Anywhere in the explorer | The explorer's top moves up one folder | Go up a level. |
| `m` `a`, name, Enter | On a folder | A new file (or folder, if the name ends with `/`) is created there | The `m` menu adds, renames/moves, copies and deletes files. |
| `m` `d`, `y` | On a file | The file is deleted | Delete (asks to confirm). |
| `I` | Anywhere in the explorer | Files starting with `.` appear (press again to hide) | Show hidden files. |
| `R` | Anywhere in the explorer | New files made outside Vim appear | Refresh. (`r` refreshes just the folder under the cursor.) |
| `cd` | On a folder | That folder becomes Vim's project folder | Searches and the file finder now start there. |
| `q` | In the explorer | The explorer closes | Close it (same as `Space e`). |
| `?` | In the explorer | A list of every explorer key appears at the top | Help; `?` again hides it. |

### Find files and text

These open a search window: type part of a name (letters don't need to be
next to each other), move with `Ctrl-j`/`Ctrl-k`, open with `Enter`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-p`  or  `Space p` | Anywhere | Search window of every file in the project | Open any file by typing part of its name — like Cmd-P. |
| `Space f` | In a file | Same, but only the current file's folder and below | Narrow the search to where you are. |
| `Space b` | With several files open | Search window of the open files | Switch to an open file. |
| `Space r` | Anywhere | Search window of recently opened files | Reopen something you had open earlier. |
| `Space /` | In a file | Search window of this file's lines | Jump to a line by typing part of it. |
| `Space s` | Anywhere | Search window of every line in the project | Search text in all files (see Level 6). |
| `Ctrl-v` / `Ctrl-x` / `Ctrl-t` | In a search window, on a result | Opens it in a split beside / below, or a new tab page | Open in a split instead of the current window. |
| `Alt-a`, `Enter` | In the project search window (`Space s`) | All results go to the quickfix list | Select everything (see Level 6 for the Alt key on a Mac). |
| `Esc` | In a search window | It closes, nothing opens | Cancel. |
| `^src b` | Typing in the file search | Opens src/b.py | Search syntax: `^` start of path, `$` end, `'word` exact, `!word` exclude. |

### Hiding files per project

Hidden items disappear from the explorer, the file finder and project search.
Each project keeps its own list in a `.ignore` file at its top folder (one
name or pattern per line; the installer keeps it out of Git).

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space x` | On a file or folder in the explorer (or in any file) | It disappears from the explorer and searches | Hide it in this project. |
| `:Hide name` Enter | Anywhere | Those names or patterns are hidden | Hide by name, e.g. `:Hide dist *.log`. |
| `:Unhide name` Enter | Anywhere | It's shown again | `Tab` completes from what's hidden. |
| `Space X` | Anywhere | The project's `.ignore` list opens; save it to apply | Edit the list by hand. |

### File tabs

Every open file is a tab along the top, numbered for `Space 1`…`Space 9`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| (open files) | Open two or more files | Their names show as tabs along the top; `+` marks unsaved ones | Like VS Code's tabs. |
| `]b` / `[b` | With several files open | Next / previous tab | Switch file tabs (like Ctrl-Tab). |
| `Space 1` … `Space 9` | With several files open | Jumps to that numbered tab | Like Cmd-1…9. |
| `Space Tab` | With several files open | Back to the previous file | Flip between the last two. |
| `Space c` | In a file | The file's tab closes; the window and layout stay | Close the file — like Cmd-W. |
| `Ctrl-s`  or  `Space w` | In a file, in Normal or Insert mode | Saved | Save — like Cmd-S. (On macOS add `stty -ixon` to your shell config; the installer does.) |

### Comments

Uses the right comment style for each language.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-/`  or  `gcc` | Anywhere on the line | `x = ▌1`<br>↓<br>`▌# x = 1` | Toggle the line's comment. Again to uncomment. |
| `gcc` (again) | On a commented line | `# x = ▌1`<br>↓<br>`▌x = 1` | Uncomment. |
| `Ctrl-/`  or  `gc` | With lines selected | `▌a = 1`<br>`b = 2`<br>↓<br>`▌# a = 1`<br>`# b = 2` | Toggle comments on the selection. |
| `gcip` | Anywhere in the paragraph | `a = 1`<br>`▌b = 2`<br>*(empty line)*<br>`c = 3`<br>↓<br>`▌# a = 1`<br>`# b = 2`<br>*(empty line)*<br>`c = 3` | `gc` + any motion or text object: here a paragraph. |
| `Ctrl-/` while typing | In Insert mode | `x = 1▌`<br>↓<br>`# x = 1▌` | Toggle the comment without leaving Insert mode. |

### Surround

Add, change or delete quotes, brackets and tags around text.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `ysiw"` | Anywhere in the word | `say hel▌lo`<br>↓<br>`say ▌"hello"` | **Y**ou **s**urround the word (`iw`) with `"`. Any text object works. |
| `yss)` | Anywhere on the line | `a ▌b`<br>↓<br>`▌(a b)` | Surround the whole line. |
| `ysiw<em>` Enter | Anywhere in the word | `▌hello`<br>↓<br>`▌<em>hello</em>` | Surround with a tag. |
| `S"` | With text selected | `▌hello world`<br>↓<br>`▌"hello" world` | Surround the selection. |
| `cs"'` | Inside the quotes | `x = "h▌i"`<br>↓<br>`x = ▌'hi'` | **C**hange **s**urrounding `"` to `'`. |
| `cs)]` | Inside the brackets | `f(▌a)`<br>↓<br>`f▌[a]` | Change `( )` to `[ ]`. Typing the *opening* bracket instead (`cs)[`) adds spaces inside: `[ a ]`. |
| `ds"` | Inside the quotes | `x = "h▌i"`<br>↓<br>`x = ▌hi` | **D**elete **s**urrounding quotes. |
| `ds(` | Inside the brackets | `f(▌a)`<br>↓<br>`f▌a` | Delete surrounding brackets. |
| `cst<div>` Enter | Inside a tag | `<p>h▌i</p>`<br>↓<br>`▌<div>hi</div>` | Change the surrounding tag. |
| `dst` | Inside a tag | `<p>h▌i</p>`<br>↓<br>`▌hi` | Delete the surrounding tag. |

### Brackets and quotes close themselves

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `(` | Typing in Insert mode | `▌`<br>↓<br>`(▌)` | Typing an opening bracket or quote adds the closing one. |
| `)` | Typing, just before an auto-added `)` | `▌`<br>↓<br>`(a)▌` | Typing the closer steps over it instead of adding another. |
| `Backspace` | Between an empty pair | `▌`<br>↓<br>`▌` | Deletes both halves. |
| `"` | Typing in Insert mode | `▌`<br>↓<br>`"▌"` | Same for quotes. |

### Multiple cursors

Like Cmd-D in VS Code. While multiple cursors are active, normal Vim keys
(`c`, `i`, `A`, `d`...) act at every cursor; `Esc` twice to finish.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-n` … `c` | On a word | `▌foo bar foo baz foo`<br>↓<br>`x bar x baz x` | `Ctrl-n` selects the word; each `Ctrl-n` adds the next match. Then `c` and type to change them all. |
| `q` | With several matches selected | `▌foo foo foo`<br>↓<br>`x foo x` | Skip this match and go to the next. |
| `\\A` | On a word | `▌foo bar foo`<br>↓<br>`x bar x` | Select every match in the file at once. |
| `Ctrl-n` … `A` | On a word | `▌foo`<br>`foo`<br>↓<br>`foo;`<br>`foo;` | Any insert key works at every cursor: here append `;`. |

## Level 10: Code: navigation, completion, folding, spelling

Go-to-definition, find references, rename and error markers come from a
**language server** — the same engines VS Code uses. Install one per language
once: open a file of that language and run `:LspInstallServer`. Language keys
live under `Space l`.

### Navigate code

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `gd`  or  `F12` | On a name where it's used | `def add(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = ▌add(1, 2)`<br>`print(greet("Vim"), total)`<br>↓<br>`def ▌add(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = add(1, 2)`<br>`print(greet("Vim"), total)` | Go to where it's defined — even in another file. `Ctrl-o` comes back. |
| `gr`  or  `Shift-F12` | On a name | A list of every place it's used | Find all references. Enter on a line in the list jumps there. |
| `K` | On a name | A popup with its type and documentation | Hover info. Move the cursor to close it. |
| `Space lp` | On a name | The definition in a popup, without leaving your place | Peek definition. |
| `Space li` | On an interface or method | Jumps to the code that implements it | Go to implementation (languages with interfaces: TypeScript, Go, Java...). |
| `Space lt` | On a variable | Jumps to the definition of its type | Go to type definition. |
| `Space lo`, type, Enter | In a file | A searchable list of the file's functions and classes | Go to a symbol in this file (like Cmd-Shift-O). |
| `Space ls`, type, Enter | Anywhere | Search symbols across the whole project | Go to a symbol anywhere (like Cmd-T). |
| `Ctrl`-click | On a name | Goes to its definition | Like Cmd-click in VS Code. †*Not checked automatically: Needs a mouse.* |

### Change code

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space lr`  or  `F2`, new name, Enter | On a name | `def add(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = ▌add(1, 2)`<br>`print(greet("Vim"), total)`<br>↓<br>`def plus(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = ▌plus(1, 2)`<br>`print(greet("Vim"), total)` | Rename everywhere it's used (in every file). The old name is pre-filled: `Ctrl-u` clears it. |
| `Space lf` | Anywhere in the file | `▌const   x=1`<br>↓<br>`const x = 1` | Format the file with the language's formatter. |
| `Space la` | On code with a problem or a possible refactor | A list of fixes and refactors to pick from | Code actions (like Cmd-.). Pick with `j`/`k` and Enter. |

### Errors and warnings

Problems are marked in the left column and shown at the end of the line.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `]g` / `[g` | Anywhere | `▌count: int = "not a number"`<br>`value = undefined_name`<br>↓<br>`count: int = ▌"not a number"`<br>`value = undefined_name` | Next / previous problem. Here the first is the text that isn't a number. |
| `Space ld` | In a file | A list of every problem in the file | All problems at once (like VS Code's Problems panel). |
| `:LspStatus` Enter | In a code file | Shows whether the language server is running | Check this first when `gd` does nothing. |
| `:LspInstallServer` Enter | In a file of the language | Downloads and sets up that language's server | Run once per language. †*Not checked automatically: Downloads from the internet; this test machine installed its servers this way beforehand.* |

### Completion

Suggestions appear as you type in files with a language server. `Ctrl-n` /
`Ctrl-p` complete from words already in your open files, in any file.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-n` / `Ctrl-p` | While typing a word | `alphabet`<br>`▌`<br>↓<br>`alphabet`<br>`alphabet▌` | Complete from words in open files. With one match it's filled straight in. |
| `Tab` / `Shift-Tab`, then `Enter` | While the suggestion menu is open | `def add(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = ▌add(1, 2)`<br>`print(greet("Vim"), total)`<br>↓<br>`def add(a, b):`<br>`····return a + b`<br>*(empty line)*<br>*(empty line)*<br>`def greet(name):`<br>`····return "Hello, " + name`<br>*(empty line)*<br>*(empty line)*<br>`total = add(1, 2)`<br>`greet▌`<br>`print(greet("Vim"), total)` | Move down / up the menu, then accept with `Enter`. (When the menu is closed, `Tab` takes Copilot's suggestion or indents.) |
| `Ctrl-e` | While the suggestion menu is open | `alphabet`<br>`alphas`<br>`▌`<br>↓<br>`alphabet`<br>`alphas`<br>`alph▌` | Close the menu and keep what you typed. |

### Indentation

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `gg=G` | Anywhere | `▌function f() {`<br>`return 1;`<br>`}`<br>↓<br>`▌function f() {`<br>`··return 1;`<br>`}` | Re-indent the whole file. `=ip` does a paragraph, `==` a line. |
| `:retab` Enter | Anywhere | `▌⇥x`<br>↓<br>`▌····x` | Turn Tab characters into spaces. |

### Folding

Fold (collapse) blocks of code. Here folding follows indentation; to make that
the default, put `set foldmethod=indent` in `~/.vimrc.local`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `zc` / `zo` | Inside an indented block | The block collapses into one line / opens again | Close / open a fold. |
| `za` | On a fold | Toggles it | Open if closed, close if open. |
| `zM` / `zR` | Anywhere | Every fold closes / opens | Overview of a long file, then back. |
| `zj` / `zk` | Anywhere | The cursor moves to the next / previous fold | Jump between folds. (A fold needs at least 2 lines to close.) |
| `zfj` | Anywhere (with manual folding) | This line and the next become a closed fold | `zf` + any motion makes a fold by hand. |

### Spelling

Commit messages get spell checking automatically.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:setlocal spell` Enter | Anywhere | Misspelled words are underlined | `:setlocal nospell` turns it off. |
| `]s` / `[s` | With spelling on | `▌This is wrnog text`<br>↓<br>`This is ▌wrnog text` | Next / previous misspelled word. |
| `z=`, number, Enter | On a misspelled word | `This is ▌wrnog`<br>↓<br>`This is ▌wrong` | Pick a suggestion from the list. |
| `zg` | On a correctly spelled word Vim doesn't know | It's no longer marked | Add the word to your dictionary. `zw` marks one as wrong. |

### Run code and commands

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:!python3 %` Enter | In a Python file | The file runs; its output shows, press Enter to return | `:!` runs any shell command; `%` is the current file. |
| `:r !echo hi` Enter | On the line to insert below | `▌top`<br>↓<br>`top`<br>`▌hi` | Insert a command's output into the file. |
| `:make` Enter | In a project with a Makefile | Errors go to the quickfix list, and Vim jumps to the first | Build and jump straight to the errors. `:make check` runs the `check` target. |

## Level 11: Git

Diff, blame, history, staging, commits and conflicts, without leaving Vim.
Git keys live under `Space g`. Any Git command also works as `:Git <command>`.

### Changes in the file you're editing

Changed lines are marked in the left column: `+` added, `~` changed, `-`
removed. A changed block of lines is called a **hunk**.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `]c` / `[c` | Anywhere in a changed file | Cursor jumps to the next / previous changed block | Jump between changes. |
| `Space gp` | On a changed line | A popup shows what the line was before | Preview the change. |
| `Space ga` | On a changed line | Just that change is staged for the next commit | Stage this hunk (not the whole file). |
| `Space gu` | On a changed line | The change is undone, back to the last commit | Undo this hunk. |
| `dic`  /  `vic` | On a changed line | Deletes / selects the changed lines | `ic` is the changed block as a text object (`ac` includes a blank line after). |
| `:GitGutterFold` Enter | In a changed file | Everything except the changes folds away | Review just what you changed. Run it again to unfold. |

### Diff

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space gd` | In a changed file | Side by side: the committed version on the left, your file on the right | Diff this file against what Git has. |
| `:Gdiffsplit HEAD~1` Enter | In a file | Your file on the left, that version on the right | Diff against any commit or branch: `HEAD~1`, `main`... |
| `]c` / `[c` in a diff | In either side of a diff | Jumps to the next / previous difference | Same keys as for change markers. |
| `do` / `dp` | On a difference, in your file (the right side) | **d**iff **o**btain: take the other side's text here / **d**iff **p**ut: send yours across | Copy one difference between the sides. |
| `:diffoff` Enter | In a diff | The diff highlighting stops | Turn it off (`:only` also closes the other side). |
| `:Git diff` Enter | Anywhere | The full diff of all your unstaged changes | `:Git diff --staged` shows what you're about to commit. |
| `:Git difftool -y main` Enter | On a branch | One tab page per changed file, each as a side-by-side diff | Review a whole branch before a pull request. |

### Who wrote this

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space gb` | In a file | A column beside the file with the commit, author and date of every line | Blame. `q` closes it. |
| `Enter` in blame | On a line in the blame column | Opens the commit that last changed that line | See why a line changed. |
| `g?` in blame | In the blame column | The list of blame keys | Help. |
| `:Git shortlog -sn HEAD -- %` Enter | In a file | Everyone who has changed this file, most commits first | Find who knows a file best. `%` is the current file. |
| `:Git log -L 2,2:%` Enter | In a file | Every commit that changed line 2, with its diff | The history of specific lines. Use your own line numbers. |
| `:e .github/CODEOWNERS` Enter | In a repo that has one | The file that says who owns which paths | `/` then a path to find its owners. |

### History

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space gl` | In a file | Every version of this file goes into the quickfix list | File history; `:cnext` / `:cprev` step through the versions. |
| `:Gclog` Enter | Anywhere | The project's commits in the quickfix list | Project history. |
| `:Git log --oneline --graph` Enter | Anywhere | A compact log with the branch graph | Overview of history. |
| `:Gedit main:%` Enter | In a file | This file as it is on `main` (read-only) | Look at another branch's version. |

### Status, staging and commits

`Space gs` opens Git status. In it, put the cursor on a file and use the keys
below. `g?` lists them all.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space gs` | Anywhere in a repo | The Git status window | Staged, unstaged and untracked files. |
| `s` | On a file in status | The file is staged | Stage. |
| `u` | On a staged file | Unstaged | Unstage. |
| `=` | On a file in status | Its diff opens inline, under the file name | Peek at the change; `=` again folds it. |
| `dv` | On a file in status | A side-by-side diff of that file | Full diff view. |
| `X` | On a changed file in status | Its changes are thrown away | Discard (fugitive tells you how to undo it). |
| `cc`, message, `:wq` | In status, after staging | A commit-message window; saving it makes the commit | Commit. `ca` amends the last commit, `ce` amends without changing its message. |
| `czz` / `czp` | In status | Your changes are stashed away / brought back | Stash and pop. |
| `:Gwrite` Enter | In a file | Saves and stages the file | Stage the whole file. |
| `:Gread` Enter | In a changed file | The file goes back to the last commit (undo with `u`) | Revert the file in the editor. |
| `:Git push` Enter | After committing | Your commits go to the remote | `:Git pull` brings others' commits in. |
| `:Git pull` Enter | When the remote has new commits | They're merged into your branch | Update from the remote. |
| `:Git switch -c new-branch` Enter | Anywhere | A new branch, checked out | Any `git` command works after `:Git`. |
| `:GMove newname.txt` Enter | In a tracked file | Renamed on disk and in Git; the buffer follows | Rename. `:GDelete` deletes the file the same way. |

### Merge conflicts

After a merge stops with conflicts, open the conflicted file and use a
three-way diff: your version on the left, the result in the middle, theirs on
the right.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:Gvdiffsplit!` Enter | In a file with conflicts | Three columns: yours, the result, theirs | Three-way merge view. |
| `:diffget //2` Enter | In the middle column, on a conflict | Takes **your** side (left) for that conflict | `:diffget //3` takes **theirs** (right). |
| `:Gwrite` Enter | In the middle column, when done | Saves the result and marks the conflict resolved | Then commit as usual. |

### Interactive rebase

`git rebase -i` opens its list of commits in Vim. Edit the words, save with `:x`, or cancel with `:cq`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `ciw` `s` `Esc` | On `pick` | `▌pick 1a2b3c4 First`<br>`pick 5d6e7f8 Second`<br>↓<br>`▌s 1a2b3c4 First`<br>`pick 5d6e7f8 Second` | Change `pick` to `s` (squash into the commit above). |
| `j` `.` | After changing one line | `▌pick 1a2b3c4 First`<br>`pick 5d6e7f8 Second`<br>↓<br>`s 1a2b3c4 First`<br>`▌s 5d6e7f8 Second` | Repeat the same change on the next line. |
| `:Squash` Enter | On a line | `▌pick 1a2b3c4 First`<br>`pick 5d6e7f8 Second`<br>↓<br>`▌squash 1a2b3c4 First`<br>`pick 5d6e7f8 Second` | Built-in commands: `:Squash`, `:Fixup`, `:Reword`, `:Edit`, `:Drop`, `:Pick`. |
| `dd` / `ddp` | On a line | `▌pick 1a2b3c4 First`<br>`pick 5d6e7f8 Second`<br>↓<br>`pick 5d6e7f8 Second`<br>`▌pick 1a2b3c4 First` | Drop a commit / move it down (`ddkP` moves it up). |

## Level 12: AI

Three ways to use AI, each optional at install: **Copilot suggestions**
(grey text as you type), **Copilot Chat** (a chat window), and **agent
panels** for Claude Code and the Copilot CLI that can read and edit your
project. AI keys live under `Space a`. Signing in happens the first time you
use each one, so the sign-in steps can't be tested automatically.

### Agent panels: Claude Code and Copilot CLI

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space aa` | Anywhere | Claude Code opens in a panel on the right | Toggle the Claude panel; it keeps running when hidden. |
| `Space aa` (again) | With the panel open | The panel hides; Claude keeps running | Hide it. |
| `Space ag` | Anywhere | The GitHub Copilot CLI opens in a panel on the right | Toggle the Copilot CLI panel. Type `/login` in it the first time. |
| `Space af` | In a file | The panel opens with `@your/file` typed in, ready for your question | Give the agent this file as context. |
| `Space af` (with lines selected) | With lines selected | Types `@your/file lines 2-3` | Point the agent at exact lines. |
| `Ctrl-w h` / `Ctrl-w l` | In a panel / in the editor | Moves between the panel and your code | The panel keeps running while you edit. |
| (edits appear) | Any file you have open, when an agent changes it | The file reloads by itself within a second | No need to reopen files after Claude or Copilot edits them. (Checked every second while a panel or terminal is open, and whenever you switch windows.) |
| `Esc`, `Shift-Tab`, `/`… | Inside the Claude panel | Claude's own keys: interrupt, change permission mode, commands | Everything Claude Code does in a terminal works in the panel. †*Not checked automatically: These belong to Claude Code itself and need your Claude account.* |

### Copilot Chat

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space ai` | Anywhere | A chat window opens (it asks you to sign in with GitHub the first time) | Ask Copilot anything; press `Enter` in Normal mode to send. †*Not checked automatically: Opening the chat starts a GitHub sign-in, so it needs your account.* |
| `Space ai` (with code selected) | With lines selected | The chat opens with your code pasted in | Ask about specific code. †*Not checked automatically: Needs a GitHub sign-in, like the chat itself.* |
| `#file:` in the chat | Typing in the chat | Attaches a project file; `Tab` completes the name | Give the chat more context. †*Not checked automatically: Needs a Copilot sign-in to get an answer.* |
| `Space am` | Anywhere | Pick which AI model the chat uses | Choose a model. †*Not checked automatically: Needs a Copilot sign-in to list models.* |

### Copilot suggestions as you type

Run `:Copilot setup` once and follow the steps to sign in.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Space ac` | Anywhere | Suggestions turn off (or back on); a message says which | Toggle suggestions — handy when they get in the way. |
| `Tab` | When grey suggestion text appears | The suggestion is inserted | Accept. (If the completion menu is open, `Tab` moves in the menu; `Ctrl-e` closes it.) †*Not checked automatically: Needs a Copilot sign-in to get suggestions.* |
| `Ctrl-]` | When a suggestion shows | The suggestion disappears | Dismiss. †*Not checked automatically: Needs a Copilot sign-in.* |
| `Ctrl-j` / `Ctrl-k` | When a suggestion shows | Next / previous alternative suggestion | Cycle. †*Not checked automatically: Needs a Copilot sign-in.* |
| `Ctrl-l` | When a suggestion shows | Only the next word of it is inserted | Accept part of a suggestion. †*Not checked automatically: Needs a Copilot sign-in.* |
| `Space ap` | Anywhere | A window with up to 10 suggestions for where you are | Browse options. †*Not checked automatically: Needs a Copilot sign-in.* |
| `:Copilot status` Enter | Anywhere | Says whether you're signed in and suggestions work | Check this when nothing appears. †*Not checked automatically: Depends on your GitHub account.* |

## Level 13: Command-line power

The `:` command line can act on any range of lines and pipe text through
shell tools. A **range** goes before the command: `%` is every line, `2,5`
lines 2 to 5, `.` the current line, `.,+2` this line and the next two,
`'<,'>` the selection.

### Ranges

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:2,3d` Enter | Anywhere | `▌1`<br>`2`<br>`3`<br>`4`<br>↓<br>`1`<br>`▌4` | Delete lines 2 to 3. |
| `:.,+1d` Enter | On a line | `1`<br>`▌2`<br>`3`<br>`4`<br>↓<br>`1`<br>`▌4` | Delete this line and the next. |
| `:t.` Enter | On a line | `▌one`<br>`two`<br>↓<br>`one`<br>`▌one`<br>`two` | Copy the line below itself (`:t0` copies it to the top). |
| `:m0` Enter | On a line | `one`<br>`▌two`<br>↓<br>`▌two`<br>`one` | Move the line to the top (`:m$` to the bottom, `:m+1` down one). |

### Sort and filter

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:sort` Enter | Anywhere (or on a selection) | `▌b`<br>`c`<br>`a`<br>↓<br>`a`<br>`b`<br>`c` | Sort lines. On a selection, only those lines. |
| `:sort u` Enter | Anywhere | `▌b`<br>`a`<br>`b`<br>↓<br>`a`<br>`b` | Sort and remove duplicates. |
| `:sort n` Enter | Anywhere | `▌10`<br>`9`<br>`100`<br>↓<br>`9`<br>`10`<br>`100` | Sort by number, not alphabetically. |
| `:sort!` Enter | Anywhere | `▌a`<br>`c`<br>`b`<br>↓<br>`c`<br>`b`<br>`a` | Reverse order. |
| `:%!python3 -m json.tool` Enter | Anywhere | `▌{"a":1}`<br>↓<br>`{`<br>`····"a": 1`<br>`}` | Pipe the whole file through any shell command — here a JSON formatter. |
| `:'<,'>!tr a-z A-Z` Enter | With lines selected | `▌one`<br>`two`<br>`three`<br>↓<br>`ONE`<br>`TWO`<br>`three` | Pipe just the selection. |
| `:'<,'>w part.txt` Enter | With lines selected | Those lines are saved to a new file | Split out part of a file. |

### Typing commands faster

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `Ctrl-r` `Ctrl-w` | Typing a `:` command, with the cursor on a word in the file | `▌foo bar foo`<br>↓<br>`x bar x` | Insert the word under the cursor into the command — here into `:%s/…/x/g`. |
| `Tab` | Typing a `:` command or file name | Completes it; press again for the next option | Completion everywhere on the command line. |
| `Up` / `Down` | Typing a `:` command | `▌a`<br>`b`<br>↓<br>`a!`<br>`b!` | Earlier commands that start with what you've typed. Here `:s` + `Up` brings back `:s/$/!/`. |

### Options you'll toggle

`:set name!` flips an on/off option. These change the current session only; put permanent ones in `~/.vimrc.local`.

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:set wrap!` Enter | Anywhere | Long lines wrap / stop wrapping | Toggle line wrapping. |
| `:set list!` Enter | Anywhere | Tabs and line ends become visible | Spot stray whitespace. |
| `:set relativenumber!` Enter | Anywhere | Line numbers switch to plain / relative | Relative numbers make `5j`-style jumps easy. |
| `:set ft=json` Enter | Anywhere | The file is treated as JSON (highlighting, indent, comments) | Fix the language when Vim guesses wrong. |

### Finding your way around Vim

| Keys | Cursor starts | Before ↓ after | What happens |
| --- | --- | --- | --- |
| `:Maps` Enter | Anywhere | A searchable list of every shortcut that's set up | Forgot a key? Search for it. |
| `:Commands` Enter | Anywhere | A searchable list of every command | Same, for `:` commands. |
| `:source ~/.vimrc` Enter | Anywhere | Your config reloads without restarting | After editing `~/.vimrc` or `~/.vimrc.local`. |
| `:PlugStatus` Enter | Anywhere | The state of every plugin | `:PlugUpdate` updates them, `:PlugClean` removes ones you switched off. |
| `:PlugUpdate` Enter | Anywhere | Downloads the latest version of every plugin | Do it now and then. †*Not checked automatically: Downloads from the internet.* |

## When a key doesn't work

| Problem | Fix |
| --- | --- |
| A key does nothing | Press `Esc` twice and try again — you were probably in another mode. Then `:verbose map <key>` shows what the key is set to. |
| `Ctrl-s` freezes the terminal | Press `Ctrl-q` to unfreeze. The installer adds `stty -ixon` to your shell config so `Ctrl-s` reaches Vim; open a new terminal. |
| `Alt-…` keys type odd characters on a Mac | Make Option send Esc: iTerm2 → Profiles → Keys → Left Option key: Esc+; Terminal.app → Settings → Profiles → Keyboard → Use Option as Meta key. |
| `F2` / `F12` don't work on a Mac | Hold `Fn`, or use `Space lr` and `gd`. |
| Copy/paste doesn't reach other apps | Your Vim lacks clipboard support: `vim --version \| grep clipboard` should show `+clipboard`. Homebrew's Vim has it. |
| `gd`, `K`, completion do nothing | Run `:LspStatus`. If no server is listed, open a file of that language and run `:LspInstallServer`. |
| Copilot shows nothing | `:Copilot status`; if not signed in, `:Copilot setup`. |
| Something looks wrong after editing the config | `:source ~/.vimrc` reloads it; `tests/run.sh` checks every shortcut in this guide. |

