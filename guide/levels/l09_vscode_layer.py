from kit import E, UI, M, section, level

P = ["plugin:nerdtree"]
F = ["plugin:fzf.vim"]

LEVEL = level(9, "This setup's VS Code layer", """\
Everything in this level comes from this repo's config: an explorer sidebar,
a fuzzy file finder, file tabs, comments, surround and multiple cursors. Open
a project with `vim ~/projects/name` to get the VS Code layout.""", [

section("Explorer sidebar", """\
Inside the explorer, keys act on the file or folder under the cursor. Move
with `j`/`k` or search with `/`, like in any buffer.""", [
    UI("`Space e`", "Anywhere", "The explorer opens on the left (press again to close)", "Toggle the explorer.",
       ["TreeOpen()", "&filetype ==# 'nerdtree'"], feed="<Space>e", requires=P),
    UI("`Space E`", "In a file", "The explorer opens with that file highlighted", "Reveal the current file in the explorer.",
       ["&filetype ==# 'nerdtree'", "getline('.') =~# 'a.py'"], setup=["edit src/a.py"], feed="<Space>E", requires=P),
    M("Click", "On a file or folder in the explorer", "Opens the file / expands the folder", "A single click works, like VS Code.",
      "Needs a mouse."),
    UI("`o`  or  `Enter`", "On a file", "The file opens in the editor on the right", "Open.",
       ["expand('%:t') ==# 'notes.txt'", "&filetype !=# 'nerdtree'", "TreeOpen()"],
       steps=[["<Space>e", 300], ["/notes<CR>o", 500]], requires=P),
    UI("`o`  or  `Enter`", "On a folder", "The folder expands (press again to collapse)", "Open or close a folder.",
       ["TreeText() =~# 'a.py'"], steps=[["<Space>e", 300], ["/src<CR>o", 500]], requires=P),
    UI("`go`", "On a file", "The file opens, but the cursor stays in the explorer", "Preview without leaving the explorer.",
       ["&filetype ==# 'nerdtree'", "index(Listed(), 'notes.txt') >= 0"], steps=[["<Space>e", 300], ["/notes<CR>go", 500]], requires=P),
    UI("`s` / `i`", "On a file", "Opens it in a new split beside / below", "Open in a split.",
       ["winnr('$') == 3", "expand('%:t') ==# 'notes.txt'"], before="▌x", steps=[["<Space>e", 300], ["/notes<CR>s", 500]], requires=P),
    UI("`t`", "On a file", "Opens it in a new tab page", "Open in a tab page.",
       ["tabpagenr('$') == 2"], steps=[["<Space>e", 300], ["/notes<CR>t", 500]], requires=P),
    UI("`O`", "On a folder (or the top line)", "Everything inside opens, all levels down", "Expand all.",
       ["TreeText() =~# 'index.js'"], steps=[["<Space>e", 300], ["ggO", 800]], requires=P),
    UI("`X`", "On a folder (or the top line)", "Everything inside collapses", "Collapse all.",
       ["TreeText() !~# 'index.js'"], steps=[["<Space>e", 300], ["ggO", 800], ["ggX", 500]], requires=P),
    UI("`x`", "On a file inside an open folder", "Its folder collapses", "Close the parent folder.",
       ["TreeText() !~# 'a.py'"], steps=[["<Space>e", 300], ["/src<CR>o", 300], ["/a.py<CR>x", 500]], requires=P),
    UI("`p` / `P`", "On a file inside a folder", "The cursor jumps to its folder / to the top", "Go to parent / root.",
       ["getline('.') =~# 'src'"], steps=[["<Space>e", 300], ["/src<CR>o", 300], ["/a.py<CR>p", 300]], requires=P),
    UI("`C`", "On a folder", "The explorer shows only that folder", "Make it the explorer's top. `u` goes back up a level.",
       ["TreeText() =~# 'b.py'", "TreeText() !~# 'notes.txt'"], steps=[["<Space>e", 300], ["/src<CR>C", 500]], requires=P),
    UI("`u`", "Anywhere in the explorer", "The explorer's top moves up one folder", "Go up a level.",
       ["TreeText() =~# 'notes.txt'"], steps=[["<Space>e", 300], ["/src<CR>C", 500], ["u", 500]], requires=P),
    UI("`m` `a`, name, Enter", "On a folder", "A new file (or folder, if the name ends with `/`) is created there",
       "The `m` menu adds, renames/moves, copies and deletes files.",
       ["filereadable('src/new.py')"], steps=[["<Space>e", 300], ["/src<CR>", 300], ["manew.py<CR>", 800]], requires=P),
    UI("`m` `d`, `y`", "On a file", "The file is deleted", "Delete (asks to confirm).",
       ["!filereadable('notes.txt')"], steps=[["<Space>e", 300], ["/notes<CR>", 300], ["mdy", 800]], requires=P),
    UI("`I`", "Anywhere in the explorer", "Files starting with `.` appear (press again to hide)", "Show hidden files.",
       ["TreeText() =~# '.github'"], steps=[["<Space>e", 300], ["I", 500]], requires=P),
    UI("`R`", "Anywhere in the explorer", "New files made outside Vim appear", "Refresh. (`r` refreshes just the folder under the cursor.)",
       ["TreeText() =~# 'fresh.txt'"], steps=[["<Space>e", 300], [":call writefile([], 'fresh.txt')<CR>", 200], ["R", 500]], requires=P),
    UI("`cd`", "On a folder", "That folder becomes Vim's project folder", "Searches and the file finder now start there.",
       ["getcwd() =~# 'src$'"], steps=[["<Space>e", 300], ["/src<CR>cd", 500]], requires=P),
    UI("`q`", "In the explorer", "The explorer closes", "Close it (same as `Space e`).",
       ["!TreeOpen()"], steps=[["<Space>e", 300], ["q", 300]], requires=P),
    UI("`?`", "In the explorer", "A list of every explorer key appears at the top", "Help; `?` again hides it.",
       ["TreeText() =~? 'quickhelp'"], steps=[["<Space>e", 300], ["?", 300]], requires=P),
]),

section("Find files and text", """\
These open a search window: type part of a name (letters don't need to be
next to each other), move with `Ctrl-j`/`Ctrl-k`, open with `Enter`.""", [
    UI("`Ctrl-p`  or  `Space p`", "Anywhere", "Search window of every file in the project", "Open any file by typing part of its name — like Cmd-P.",
       ["expand('%:t') ==# 'notes.txt'"], steps=[["<C-p>", 1500], ["notes", 1000], ["<CR>", 1000]], requires=F),
    UI("`Space f`", "In a file", "Same, but only the current file's folder and below", "Narrow the search to where you are.",
       ["expand('%:p') =~# 'src/b.py$'"], setup=["edit src/a.py"], steps=[["<Space>f", 1500], ["b.py", 1000], ["<CR>", 1000]], requires=F),
    UI("`Space b`", "With several files open", "Search window of the open files", "Switch to an open file.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"],
       steps=[["<Space>b", 1500], ["notes", 1000], ["<CR>", 1000]], requires=F),
    UI("`Space r`", "Anywhere", "Search window of recently opened files", "Reopen something you had open earlier.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"],
       steps=[["<Space>r", 1500], ["notes", 1000], ["<CR>", 1000]], requires=F),
    UI("`Space /`", "In a file", "Search window of this file's lines", "Jump to a line by typing part of it.",
       ["line('.') == 3"], before="▌alpha\nbeta\ngamma", steps=[["<Space>/", 1500], ["gam", 1000], ["<CR>", 1000]], requires=F),
    UI("`Space s`", "Anywhere", "Search window of every line in the project", "Search text in all files (see Level 6).",
       ["expand('%:t') ==# 'util.py'"], steps=[["<Space>s", 1500], ["import add", 1500], ["<CR>", 1000]], requires=F + ["exe:rg"]),
    UI("`Ctrl-v` / `Ctrl-x` / `Ctrl-t`", "In a search window, on a result", "Opens it in a split beside / below, or a new tab page", "Open in a split instead of the current window.",
       ["winnr('$') == 2", "winlayout()[0] ==# 'row'", "expand('%:t') ==# 'notes.txt'"], before="▌x",
       steps=[["<C-p>", 1500], ["notes", 1000], ["<C-v>", 1000]], requires=F),
    UI("`Alt-a`, `Enter`", "In the project search window (`Space s`)", "All results go to the quickfix list", "Select everything (see Level 6 for the Alt key on a Mac).",
       ["QfLen() == 3"], steps=[["<Space>s", 1500], ["add(", 1500], ["<Esc>a", 800], ["<CR>", 1500]], requires=F + ["exe:rg"]),
    UI("`Esc`", "In a search window", "It closes, nothing opens", "Cancel.",
       ["empty(TermWins())", "Popups() == 0"], steps=[["<C-p>", 1500], ["<Esc>", 800]], requires=F),
    UI("`^src b`", "Typing in the file search", "Opens src/b.py", "Search syntax: `^` start of path, `$` end, `'word` exact, `!word` exclude.",
       ["expand('%:p') =~# 'src/b.py$'"], steps=[["<C-p>", 1500], ["^src b", 1000], ["<CR>", 1000]], requires=F),
]),

section("Hiding files per project", """\
Hidden items disappear from the explorer, the file finder and project search.
Each project keeps its own list in a `.ignore` file at its top folder (one
name or pattern per line; the installer keeps it out of Git).""", [
    UI("`Space x`", "On a file or folder in the explorer (or in any file)", "It disappears from the explorer and searches", "Hide it in this project.",
       ["Disk('.ignore') ==# 'node_modules'", "TreeText() !~# 'node_modules'", "Sh('rg --files') !~# 'node_modules'"],
       steps=[["<Space>e", 300], ["/node_modules<CR>", 300], ["<Space>x", 500]], requires=P),
    UI("`:Hide name` Enter", "Anywhere", "Those names or patterns are hidden", "Hide by name, e.g. `:Hide dist *.log`.",
       ["Disk('.ignore') ==# \"node_modules\\n*.log\""], feed=":Hide node_modules *.log<CR>"),
    UI("`:Unhide name` Enter", "Anywhere", "It's shown again", "`Tab` completes from what's hidden.",
       ["Disk('.ignore') ==# '*.log'"], feed=":Hide node_modules *.log<CR>:Unhide node_modules<CR>"),
    UI("`Space X`", "Anywhere", "The project's `.ignore` list opens; save it to apply", "Edit the list by hand.",
       ["expand('%:t') ==# '.ignore'"], feed="<Space>X"),
]),

section("File tabs", "Every open file is a tab along the top, numbered for `Space 1`…`Space 9`.", [
    UI("(open files)", "Open two or more files", "Their names show as tabs along the top; `+` marks unsaved ones", "Like VS Code's tabs.",
       ["buftabline#render() =~# 'notes.txt'", "buftabline#render() =~# 'README.md'"],
       setup=["edit notes.txt", "edit README.md"], requires=["plugin:vim-buftabline"]),
    UI("`]b` / `[b`", "With several files open", "Next / previous tab", "Switch file tabs (like Ctrl-Tab).",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"], feed="[b"),
    UI("`Space 1` … `Space 9`", "With several files open", "Jumps to that numbered tab", "Like Cmd-1…9.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md", "edit util.py"], feed="<Space>1"),
    UI("`Space Tab`", "With several files open", "Back to the previous file", "Flip between the last two.",
       ["expand('%:t') ==# 'notes.txt'"], setup=["edit notes.txt", "edit README.md"], feed="<Space><Tab>"),
    UI("`Space c`", "In a file", "The file's tab closes; the window and layout stay", "Close the file — like Cmd-W.",
       ["Listed() == ['notes.txt']", "winnr('$') == 2"], setup=["edit notes.txt", "vsplit README.md"], feed="<Space>c"),
    UI("`Ctrl-s`  or  `Space w`", "In a file, in Normal or Insert mode", "Saved", "Save — like Cmd-S. (On macOS add `stty -ixon` to your shell config; the installer does.)",
       ["Disk('sample.txt') ==# 'xhello'"], before="▌hello", feed="ix<C-s>"),
]),

section("Comments", "Uses the right comment style for each language.", [
    E("`Ctrl-/`  or  `gcc`", "Anywhere on the line", "x = ▌1", "▌# x = 1", "Toggle the line's comment. Again to uncomment.", ext="py", feed="<C-_>", requires=["plugin:vim-commentary"]),
    E("`gcc` (again)", "On a commented line", "# x = ▌1", "▌x = 1", "Uncomment.", ext="py", feed="gcc"),
    E("`Ctrl-/`  or  `gc`", "With lines selected", "▌a = 1\nb = 2", "▌# a = 1\n# b = 2", "Toggle comments on the selection.", ext="py", feed="Vj<C-_>", requires=["plugin:vim-commentary"]),
    E("`gcip`", "Anywhere in the paragraph", "a = 1\n▌b = 2\n\nc = 3", "▌# a = 1\n# b = 2\n\nc = 3", "`gc` + any motion or text object: here a paragraph.", ext="py"),
    E("`Ctrl-/` while typing", "In Insert mode", "x = 1▌", "# x = 1▌", "Toggle the comment without leaving Insert mode.", ext="py", feed="A<C-_>", mode="i", requires=["plugin:vim-commentary"]),
], requires=["plugin:vim-commentary"]),

section("Surround", "Add, change or delete quotes, brackets and tags around text.", [
    E("`ysiw\"`", "Anywhere in the word", "say hel▌lo", "say ▌\"hello\"", "**Y**ou **s**urround the word (`iw`) with `\"`. Any text object works.", requires=["plugin:vim-surround"]),
    E("`yss)`", "Anywhere on the line", "a ▌b", "▌(a b)", "Surround the whole line."),
    E("`ysiw<em>` Enter", "Anywhere in the word", "▌hello", "▌<em>hello</em>", "Surround with a tag.", feed="ysiw<lt>em><CR>", requires=["plugin:vim-surround"]),
    E("`S\"`", "With text selected", "▌hello world", "▌\"hello\" world", "Surround the selection.", feed="veS\""),
    E("`cs\"'`", "Inside the quotes", "x = \"h▌i\"", "x = ▌'hi'", "**C**hange **s**urrounding `\"` to `'`.", requires=["plugin:vim-surround"]),
    E("`cs)]`", "Inside the brackets", "f(▌a)", "f▌[a]", "Change `( )` to `[ ]`. Typing the *opening* bracket instead (`cs)[`) adds spaces inside: `[ a ]`."),
    E("`ds\"`", "Inside the quotes", "x = \"h▌i\"", "x = ▌hi", "**D**elete **s**urrounding quotes.", requires=["plugin:vim-surround"]),
    E("`ds(`", "Inside the brackets", "f(▌a)", "f▌a", "Delete surrounding brackets."),
    E("`cst<div>` Enter", "Inside a tag", "<p>h▌i</p>", "▌<div>hi</div>", "Change the surrounding tag.", feed="cst<lt>div><CR>", requires=["plugin:vim-surround"]),
    E("`dst`", "Inside a tag", "<p>h▌i</p>", "▌hi", "Delete the surrounding tag."),
], requires=["plugin:vim-surround"]),

section("Brackets and quotes close themselves", "", [
    E("`(`", "Typing in Insert mode", "▌", "(▌)", "Typing an opening bracket or quote adds the closing one.", feed="i(", mode="i", requires=["plugin:auto-pairs"]),
    E("`)`", "Typing, just before an auto-added `)`", "▌", "(a)▌", "Typing the closer steps over it instead of adding another.", feed="i(a)", mode="i"),
    E("`Backspace`", "Between an empty pair", "▌", "▌", "Deletes both halves.", feed="i(<BS>", mode="i", requires=["plugin:auto-pairs"]),
    E("`\"`", "Typing in Insert mode", "▌", "\"▌\"", "Same for quotes.", feed="i\"", mode="i"),
], requires=["plugin:auto-pairs"]),

section("Multiple cursors", """\
Like Cmd-D in VS Code. While multiple cursors are active, normal Vim keys
(`c`, `i`, `A`, `d`...) act at every cursor; `Esc` twice to finish.""", [
    E("`Ctrl-n` … `c`", "On a word", "▌foo bar foo baz foo", "x bar x baz x",
      "`Ctrl-n` selects the word; each `Ctrl-n` adds the next match. Then `c` and type to change them all.",
      feed="<C-n><C-n><C-n>cx<Esc><Esc>", check_cursor=False, requires=["plugin:vim-visual-multi"]),
    E("`q`", "With several matches selected", "▌foo foo foo", "x foo x", "Skip this match and go to the next.",
      feed="<C-n><C-n>q<C-n>cx<Esc><Esc>", check_cursor=False, requires=["plugin:vim-visual-multi"]),
    E("`\\\\A`", "On a word", "▌foo bar foo", "x bar x", "Select every match in the file at once.",
      feed="\\\\Acx<Esc><Esc>", check_cursor=False, requires=["plugin:vim-visual-multi"]),
    E("`Ctrl-n` … `A`", "On a word", "▌foo\nfoo", "foo;\nfoo;", "Any insert key works at every cursor: here append `;`.",
      feed="<C-n><C-n>A;<Esc><Esc>", check_cursor=False, requires=["plugin:vim-visual-multi"]),
], requires=["plugin:vim-visual-multi"]),
])
