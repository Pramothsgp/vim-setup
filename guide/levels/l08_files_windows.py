from kit import E, UI, M, section, level

LEVEL = level(8, "Files, windows, tabs and the terminal", """\
An open file is a **buffer**. A **window** is a view onto a buffer — split
the screen and you have several windows. A **tab page** holds a whole layout
of windows. (The file tabs along the top in this setup are buffers; Level 9
covers them.)""", [

section("Opening and saving files", "Press `Tab` while typing a file name to complete it.", [
    UI("`:e notes.txt` Enter", "Anywhere", "notes.txt opens", "**E**dit (open) a file. Paths work: `:e src/a.py`.",
       ["expand('%:t') ==# 'notes.txt'"], feed=":e notes.txt<CR>"),
    UI("`:enew` Enter", "Anywhere", "A new empty, unnamed file", "Save it later with `:w name`.",
       ["expand('%') ==# '' && line('$') == 1"], feed=":enew<CR>"),
    UI("`:w copy.txt` Enter", "In a file", "copy.txt is written; you keep editing the original",
       "Save a copy under another name.", ["Disk('copy.txt') ==# 'hello'", "expand('%:t') ==# 'sample.txt'"],
       before="▌hello", feed=":w copy.txt<CR>"),
    UI("`:saveas other.txt` Enter", "In a file", "Saved as other.txt, and you're now editing other.txt",
       "Save As.", ["Disk('other.txt') ==# 'hello'", "expand('%:t') ==# 'other.txt'"],
       before="▌hello", feed=":saveas other.txt<CR>"),
    UI("`:wa` Enter", "With several changed files", "All of them are saved", "**W**rite **a**ll.",
       ["Disk('notes.txt') ==# \"beta\\ngamma\"", "Disk('README.md') ==# ''"],
       setup=["edit notes.txt", "normal! dd", "edit README.md", "normal! dd"], feed=":wa<CR>"),
    UI("`gf`", "On a file name in the text", "That file opens", "**G**o to **f**ile.",
       ["expand('%:t') ==# 'notes.txt'"], before="see ▌notes.txt", feed="gf"),
    UI("`Ctrl-^`", "Anywhere", "Back to the file you had open before", "Flip between the last two files.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"], feed="<C-^>"),
    UI("`Ctrl-g`", "Anywhere", "The file's name, line count and position appear at the bottom", "Where am I?",
       ["execute(\"normal! \\<C-g>\") =~# 'sample.txt'"], before="▌x", feed="<C-g>"),
    E("`:r notes.txt` Enter", "On the line to insert below", "▌top", "top\n▌alpha\nbeta\ngamma", "**R**ead another file into this one, below the cursor.", feed=":r notes.txt<CR>"),
]),

section("Leaving for a moment", "", [
    M("`Ctrl-z`, then `fg`", "Anywhere in Normal mode", "Vim pauses and you're back in the shell; `fg` returns to Vim exactly as you left it",
      "Quick trip to the shell. (In other editors `Ctrl-z` is undo — in Vim, undo is `u`.)", "Suspends the test's own Vim; try it in your terminal."),
    M("Mouse", "Anywhere", "Click to place the cursor, drag to select, scroll with the wheel", "The mouse works in all modes in this setup.", "Needs a mouse."),
]),

section("Buffers (open files)", "", [
    UI("`:ls` Enter", "Anywhere", "A numbered list of open files", "`%` marks the current one, `#` the previous one.",
       ["execute('ls') =~# 'notes.txt' && execute('ls') =~# 'README.md'"],
       setup=["edit notes.txt", "edit README.md"], feed=":ls<CR><CR>"),
    UI("`:b notes` Enter", "Anywhere", "Switches to notes.txt", "Switch by part of the name; `Tab` completes.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"], feed=":b notes<CR>"),
    UI("`:bd` Enter", "In a file", "The file is closed (and its window, if it had its own)", "**B**uffer **d**elete. In this setup `Space c` does it without closing the window.",
       ["Listed() == ['notes.txt']"], setup=["edit notes.txt", "edit README.md"], feed=":bd<CR>"),
    UI("`:%bd` Enter", "Anywhere", "Every file is closed", "Close all files at once.",
       ["Listed() == []"], setup=["edit notes.txt", "edit README.md"], feed=":%bd<CR>"),
]),

section("Windows (splits)", "Several views side by side — of different files or the same one.", [
    UI("`Space \\`", "Anywhere", "The window splits side by side", "Split vertically (this config). Built in: `Ctrl-w v`.",
       ["winnr('$') == 2", "winlayout()[0] ==# 'row'"], before="▌x", feed="<Space>\\"),
    UI("`:sp notes.txt` / `:vsp notes.txt` Enter", "Anywhere", "notes.txt opens in a new window, below / beside",
       "Split and open a file. Without a name, both windows show the current file. `Ctrl-w s` / `Ctrl-w v` also split.",
       ["winnr('$') == 2", "expand('%:t') ==# 'notes.txt'", "winlayout()[0] ==# 'col'"], before="▌x", feed=":sp notes.txt<CR>"),
    UI("`Ctrl-h` / `Ctrl-j` / `Ctrl-k` / `Ctrl-l`", "With two or more windows", "The cursor moves to the window on the left / below / above / right",
       "Move between windows (this config; built in: `Ctrl-w` then `h` `j` `k` `l`).",
       ["winnr() == 1"], before="▌x", setup=["vsplit notes.txt"], feed="<C-l><C-h>"),
    UI("`Ctrl-w w`", "With two or more windows", "The cursor goes to the next window", "Cycle through windows, wrapping around at the end.",
       ["winnr() == 1"], before="▌x", setup=["vsplit notes.txt"], feed="<C-w>w"),
    UI("`Ctrl-w =`", "After resizing", "All windows get equal size", "Even them out.",
       ["abs(winwidth(1) - winwidth(2)) <= 1"], before="▌x", setup=["vsplit notes.txt", "vertical resize 20"], feed="<C-w>="),
    UI("`Ctrl-w _` / `Ctrl-w |`", "In a split", "This window takes all the height / width", "Maximise for a moment; `Ctrl-w =` to restore.",
       ["winheight(0) > 30"], before="▌x", setup=["split notes.txt"], feed="<C-w>_"),
    UI("`5 Ctrl-w +` / `-` / `>` / `<`", "In a split", "5 lines taller / shorter, or 5 columns wider / narrower", "Resize by steps.",
       ["winheight(0) == g:h0 + 5"], before="▌x", setup=["split notes.txt", "let g:h0 = winheight(0)"], feed="5<C-w>+"),
    UI("`Ctrl-w H` / `J` / `K` / `L`", "In a split", "The window moves to the far left / bottom / top / right", "Rearrange the layout: here a top/bottom split becomes side by side.",
       ["winlayout()[0] ==# 'row'"], before="▌x", setup=["split notes.txt"], feed="<C-w>H"),
    UI("`Ctrl-w o`", "In one of several windows", "Only this window is left", "Close all **o**ther windows (files stay open).",
       ["winnr('$') == 1"], before="▌x", setup=["split notes.txt", "vsplit README.md"], feed="<C-w>o"),
    UI("`Ctrl-w q`  or  `Space q`", "In a split", "This window closes", "Close the window.",
       ["winnr('$') == 1"], before="▌x", setup=["split notes.txt"], feed="<Space>q"),
]),

section("Tab pages", "Each tab page is a separate layout of windows. Most people only need splits.", [
    UI("`:tabnew` Enter", "Anywhere", "A new tab page with an empty window", "Also `:tabnew file`.",
       ["tabpagenr('$') == 2"], feed=":tabnew<CR>"),
    UI("`gt` / `gT`", "With several tab pages", "Next / previous tab page", "Switch tab pages.",
       ["tabpagenr() == 1"], setup=["tabnew"], feed="gt"),
    UI("`Ctrl-w T`", "In a split", "That window moves to its own tab page", "Pull a window out into a tab.",
       ["tabpagenr('$') == 2"], before="▌x", setup=["split notes.txt"], feed="<C-w>T"),
    UI("`:tabclose` Enter", "In a tab page", "The tab page closes", "Close it (the files stay open).",
       ["tabpagenr('$') == 1"], setup=["tabnew"], feed=":tabclose<CR>"),
]),

section("Terminal panel", """\
A shell inside Vim, like VS Code's terminal. While you're typing in it, keys
go to the shell; `Ctrl-w` then `h`/`j`/`k`/`l` moves to another window.""", [
    UI("`Ctrl-t`  or  `Space t`", "Anywhere", "A terminal opens at the bottom, ready to type",
       "Toggle the terminal panel (this config). It keeps running when hidden.",
       ["len(TermWins()) == 1", "winnr() == winnr('$')", "mode() ==# 't'"], feed="<C-t>", wait=500),
    UI("`Ctrl-t` (in the panel)", "While typing in the terminal", "The panel hides; the shell keeps running", "Toggle it off again.",
       ["empty(TermWins())", "len(term_list()) == 1"], steps=[["<C-t>", 800], ["<C-t>", 500]]),
    UI("Type a command, Enter", "In the terminal panel", "The command runs in your shell", "It's a normal shell.",
       ["TermText() =~# 'hello-from-the-panel'"], steps=[["<C-t>", 800], ["echo hello-from-the-panel<CR>", 1000]]),
    UI("`Esc` `Esc`", "In the terminal panel", "You can scroll and copy the output with Vim keys",
       "Leave typing mode (this config, only in this panel). `i` goes back to typing.",
       [], steps=[["<C-t>", 800], ["<Esc><Esc>", 300]], mode="n"),
    UI("`i`", "In the panel, after `Esc` `Esc`", "Typing goes to the shell again", "Back to typing.",
       [], steps=[["<C-t>", 800], ["<Esc><Esc>", 300], ["i", 300]], mode="t"),
    UI("`Ctrl-w k`", "Typing in the terminal panel", "The cursor moves to the editor above", "Leave the terminal without closing it.",
       ["&buftype ==# ''"], steps=[["<C-t>", 800], ["<C-w>k", 300]]),
    UI("`:term` / `:vert term` Enter", "Anywhere", "An extra terminal opens below / beside", "As many terminals as you like; `exit` closes one.",
       ["len(TermWins()) == 1", "winlayout()[0] ==# 'row'"], feed=":vert term<CR>", wait=500),
]),
])
