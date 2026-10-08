from kit import E, UI, section, level

LEVEL = level(7, "Marks, jumps and macros", """\
Marks are bookmarks. Jumps are Vim's own history of where you've been. Macros
record keystrokes and replay them — the tool for any edit you need to repeat
on many lines.""", [

section("Marks", "", [
    E("`ma` … `` `a ``", "Set it anywhere, jump from anywhere", "one ▌two\nthree", "one ▌two\nthree",
      "`ma` puts mark `a` at the cursor (any letter); `` `a `` jumps back to that exact spot. Here: set, go down, jump back.",
      feed="maj0`a"),
    E("`'a`", "Anywhere, after setting mark `a`", "one ▌two\nthree", "▌one two\nthree",
      "Jump to the *line* of mark `a` (its first non-blank character).", feed="maj'a"),
    UI("`mA` … `` `A ``", "In any file", "Jumps to the other file, at the mark",
       "Capital marks work across files — bookmark a file you keep coming back to.",
       ["expand('%:t') ==# 'notes.txt'", "line('.') == 2"],
       setup=["edit notes.txt", "2"], feed="mA:edit README.md<CR>`A"),
    UI("`:marks` Enter", "Anywhere", "A list of your marks", "See what's set.",
       ["execute('marks') =~# ' a '"], before="▌x", feed="ma:marks<CR><CR>"),
]),

section("Jumping back", """\
Big moves (search, `G`, `%`, `gd`, opening another file...) are remembered,
so you can always get back.""", [
    E("`Ctrl-o` / `Ctrl-i`", "After a jump", "▌1\n2\n3", "▌1\n2\n3", "Back / forward through the places you jumped from. Here: `G`, then `Ctrl-o` back.", feed="G<C-o>"),
    E("`Ctrl-i`", "After `Ctrl-o`", "▌1\n2\n3", "1\n2\n▌3", "Forward again.", feed="G<C-o><C-i>"),
    E("`` `` ``", "After a jump", "▌1\n2\n3", "▌1\n2\n3", "Toggle between here and where you jumped from. `''` does it by line.", feed="G``"),
    E("`` `. ``", "Anywhere", "▌abc\nxyz", "abc\n▌yz", "Jump to where you last changed something.", feed="jxgg`."),
    E("`g;` / `g,`", "Anywhere", "▌a\nb\nc", "a\nb▌!\nc!",
      "Step back / forward through the places you changed. Here: changed lines 2 and 3, then `g;` `g;` back to line 2's change.",
      feed="jA!<Esc>jA!<Esc>gg g;g;".replace(" ", "")),
    UI("`:jumps` / `:changes` Enter", "Anywhere", "Lists of your jumps / your changes", "See the history.",
       ["execute('jumps') =~# 'jump'"], before="▌1\n2", feed="G:jumps<CR><CR>"),
]),

section("Macros: record and replay", """\
`qa` starts recording into register `a` (any letter); `q` stops. `@a`
replays. End the recording by moving to the next line, so each replay
continues where the last one stopped.""", [
    E("`qa` … `q` then `@a`", "On the first line", "▌a\nb\nc", "a;\nb;\n▌c",
      "Record: `A;` `Esc` `j` (add `;`, go down). Replay once on line 2.", feed="qaA;<Esc>jq@a"),
    E("`@@`", "After playing a macro", "▌a\nb\nc", "a;\nb;\nc▌;", "Play the last macro again.", feed="qaA;<Esc>jq@a@@"),
    E("`3@a`", "After recording", "▌1\n2\n3\n4\n5", "1;\n2;\n3;\n4;\n▌5", "Play it 3 times.", feed="qaA;<Esc>jq3@a"),
    E("`:'<,'>normal @a` Enter", "With lines selected", "▌a\nb\nc", "a;\nb;\nc;",
      "Play the macro on every selected line (no need to end it with `j`). Here: recorded on line 1, then selected lines 2–3.",
      feed="qaA;<Esc>qjVj:normal @a<CR>", check_cursor=False),
    E("`:%normal A;` Enter", "Anywhere", "▌a\nb", "a;\nb;", "Run the same keys on every line — often quicker than a macro.", feed=":%normal A;<CR>", check_cursor=False),
    E("`@:`", "After any `:` command", "▌a\nb", "a!\nb!", "Repeat the last command-line command. Here `:s/$/!/` on line 1, then `j` `@:`.", feed=":s/$/!/<CR>j@:", check_cursor=False),
    UI("`q:`", "Anywhere", "A window listing your past commands; edit one and press Enter to run it",
       "Command history you can edit like text. `:q` closes it.", ["g:probe.cmdwin ==# ':'"], feed="q:"),
]),
])
