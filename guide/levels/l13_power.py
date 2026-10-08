from kit import E, UI, M, section, level

LEVEL = level(13, "Command-line power", """\
The `:` command line can act on any range of lines and pipe text through
shell tools. A **range** goes before the command: `%` is every line, `2,5`
lines 2 to 5, `.` the current line, `.,+2` this line and the next two,
`'<,'>` the selection.""", [

section("Ranges", "", [
    E("`:2,3d` Enter", "Anywhere", "▌1\n2\n3\n4", "1\n▌4", "Delete lines 2 to 3.", feed=":2,3d<CR>"),
    E("`:.,+1d` Enter", "On a line", "1\n▌2\n3\n4", "1\n▌4", "Delete this line and the next.", feed=":.,+1d<CR>"),
    E("`:t.` Enter", "On a line", "▌one\ntwo", "one\n▌one\ntwo", "Copy the line below itself (`:t0` copies it to the top).", feed=":t.<CR>"),
    E("`:m0` Enter", "On a line", "one\n▌two", "▌two\none", "Move the line to the top (`:m$` to the bottom, `:m+1` down one).", feed=":m0<CR>"),
]),

section("Sort and filter", "", [
    E("`:sort` Enter", "Anywhere (or on a selection)", "▌b\nc\na", "a\nb\nc", "Sort lines. On a selection, only those lines.", feed=":sort<CR>", check_cursor=False),
    E("`:sort u` Enter", "Anywhere", "▌b\na\nb", "a\nb", "Sort and remove duplicates.", feed=":sort u<CR>", check_cursor=False),
    E("`:sort n` Enter", "Anywhere", "▌10\n9\n100", "9\n10\n100", "Sort by number, not alphabetically.", feed=":sort n<CR>", check_cursor=False),
    E("`:sort!` Enter", "Anywhere", "▌a\nc\nb", "c\nb\na", "Reverse order.", feed=":sort!<CR>", check_cursor=False),
    E("`:%!python3 -m json.tool` Enter", "Anywhere", "▌{\"a\":1}", "{\n    \"a\": 1\n}", "Pipe the whole file through any shell command — here a JSON formatter.",
      feed=":%!python3 -m json.tool<CR>", check_cursor=False, requires=["exe:python3"]),
    E("`:'<,'>!tr a-z A-Z` Enter", "With lines selected", "▌one\ntwo\nthree", "ONE\nTWO\nthree", "Pipe just the selection.",
      feed="Vj:!tr a-z A-Z<CR>", check_cursor=False),
    UI("`:'<,'>w part.txt` Enter", "With lines selected", "Those lines are saved to a new file", "Split out part of a file.",
       ["Disk('part.txt') ==# \"one\\ntwo\""], before="▌one\ntwo\nthree", feed="Vj:w part.txt<CR>"),
]),

section("Typing commands faster", "", [
    E("`Ctrl-r` `Ctrl-w`", "Typing a `:` command, with the cursor on a word in the file", "▌foo bar foo", "x bar x",
      "Insert the word under the cursor into the command — here into `:%s/…/x/g`.", feed=":%s/<C-r><C-w>/x/g<CR>", check_cursor=False),
    UI("`Tab`", "Typing a `:` command or file name", "Completes it; press again for the next option", "Completion everywhere on the command line.",
       ["expand('%:t') ==# 'notes.txt'"], feed=":e not<Tab><CR>"),
    E("`Up` / `Down`", "Typing a `:` command", "▌a\nb", "a!\nb!", "Earlier commands that start with what you've typed. Here `:s` + `Up` brings back `:s/$/!/`.",
      feed=":s/$/!/<CR>j:s<Up><CR>", check_cursor=False),
]),

section("Options you'll toggle", "`:set name!` flips an on/off option. These change the current session only; put permanent ones in `~/.vimrc.local`.", [
    UI("`:set wrap!` Enter", "Anywhere", "Long lines wrap / stop wrapping", "Toggle line wrapping.", ["!&wrap"], feed=":set wrap!<CR>"),
    UI("`:set list!` Enter", "Anywhere", "Tabs and line ends become visible", "Spot stray whitespace.", ["&list"], feed=":set list!<CR>"),
    UI("`:set relativenumber!` Enter", "Anywhere", "Line numbers switch to plain / relative", "Relative numbers make `5j`-style jumps easy.", ["!&relativenumber"], feed=":set relativenumber!<CR>"),
    UI("`:set ft=json` Enter", "Anywhere", "The file is treated as JSON (highlighting, indent, comments)", "Fix the language when Vim guesses wrong.", ["&filetype ==# 'json'"], feed=":set ft=json<CR>"),
]),

section("Finding your way around Vim", "", [
    UI("`:Maps` Enter", "Anywhere", "A searchable list of every shortcut that's set up", "Forgot a key? Search for it.",
       ["Popups() >= 1 || len(TermWins()) >= 1"], feed=":Maps<CR>", wait=1500, requires=["plugin:fzf.vim"]),
    UI("`:Commands` Enter", "Anywhere", "A searchable list of every command", "Same, for `:` commands.",
       ["Popups() >= 1 || len(TermWins()) >= 1"], feed=":Commands<CR>", wait=1500, requires=["plugin:fzf.vim"]),
    UI("`:source ~/.vimrc` Enter", "Anywhere", "Your config reloads without restarting", "After editing `~/.vimrc` or `~/.vimrc.local`.",
       ["exists(':Hide') == 2"], feed=":source $MYVIMRC<CR>"),
    UI("`:PlugStatus` Enter", "Anywhere", "The state of every plugin", "`:PlugUpdate` updates them, `:PlugClean` removes ones you switched off.",
       ["&filetype ==# 'vim-plug'"], feed=":PlugStatus<CR>", wait=800, requires=["cmd:PlugStatus"]),
    M("`:PlugUpdate` Enter", "Anywhere", "Downloads the latest version of every plugin", "Do it now and then.", "Downloads from the internet."),
]),
])
