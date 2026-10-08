from kit import E, UI, M, section, level

PY = ["plugin:vim-lsp", "lsp:python"]
TS = ["plugin:vim-lsp", "lsp:typescript"]
WAIT = ["call LspReady()"]

APP = """\
def add(a, b):
    return a + b


def greet(name):
    return "Hello, " + name


total = {cur}add(1, 2)
print(greet("Vim"), total)"""

LEVEL = level(10, "Code: navigation, completion, folding, spelling", """\
Go-to-definition, find references, rename and error markers come from a
**language server** — the same engines VS Code uses. Install one per language
once: open a file of that language and run `:LspInstallServer`. Language keys
live under `Space l`.""", [

section("Navigate code", "", [
    E("`gd`  or  `F12`", "On a name where it's used", APP.format(cur="▌"),
      APP.format(cur="").replace("def add", "def ▌add"),
      "Go to where it's defined — even in another file. `Ctrl-o` comes back.",
      file="app.py", setup=WAIT, feed="gd", wait=1500, requires=PY),
    UI("`gr`  or  `Shift-F12`", "On a name", "A list of every place it's used",
       "Find all references. Enter on a line in the list jumps there.",
       ["QfLen() + LocLen() >= 2"], before=APP.format(cur="▌"), file="app.py", setup=WAIT, feed="gr", wait=2500, requires=PY),
    UI("`K`", "On a name", "A popup with its type and documentation", "Hover info. Move the cursor to close it.",
       ["Popups() >= 1"], before=APP.format(cur="▌"), file="app.py", setup=WAIT, feed="K", wait=2500, requires=PY),
    UI("`Space lp`", "On a name", "The definition in a popup, without leaving your place", "Peek definition.",
       ["Popups() >= 1"], before=APP.format(cur="▌"), file="app.py", setup=WAIT, feed="<Space>lp", wait=2500, requires=PY),
    UI("`Space li`", "On an interface or method", "Jumps to the code that implements it", "Go to implementation (languages with interfaces: TypeScript, Go, Java...).",
       ["getline('.') =~# 'area(): number {'"], setup=["edit web/shapes.ts", "2", "normal! ^"] + WAIT,
       feed="<Space>li", wait=2500, requires=TS),
    UI("`Space lt`", "On a variable", "Jumps to the definition of its type", "Go to type definition.",
       ["getline('.') =~# 'interface Shape'"], setup=["edit web/shapes.ts", "12", "normal! w"] + WAIT,
       feed="<Space>lt", wait=2500, requires=TS),
    UI("`Space lo`, type, Enter", "In a file", "A searchable list of the file's functions and classes", "Go to a symbol in this file (like Cmd-Shift-O).",
       ["line('.') == 5"], before=APP.format(cur="▌"), file="app.py", setup=WAIT,
       steps=[["<Space>lo", 2500, "xt!"], ["greet", 800, "xt!"], ["<CR>", 1000]], requires=PY),
    UI("`Space ls`, type, Enter", "Anywhere", "Search symbols across the whole project", "Go to a symbol anywhere (like Cmd-T).",
       ["expand('%:t') ==# 'app.py'", "line('.') == 5"], before="x", file="util.py", setup=WAIT,
       steps=[["<Space>ls", 2500, "xt!"], ["greet", 3000, "xt!"], ["<CR>", 1500]], requires=PY),
    M("`Ctrl`-click", "On a name", "Goes to its definition", "Like Cmd-click in VS Code.", "Needs a mouse."),
]),

section("Change code", "", [
    E("`Space lr`  or  `F2`, new name, Enter", "On a name", APP.format(cur="▌"),
      APP.format(cur="▌").replace("add", "plus"),
      "Rename everywhere it's used (in every file). The old name is pre-filled: `Ctrl-u` clears it.",
      file="app.py", setup=WAIT, steps=[["<Space>lr", 0], ["<C-u>plus<CR>", 3000, "t"]], requires=PY, check_cursor=False),
    E("`Space lf`", "Anywhere in the file", "▌const   x=1", "const x = 1", "Format the file with the language's formatter.",
      file="web/fmt.ts", setup=WAIT, feed="<Space>lf", wait=2500, requires=TS, check_cursor=False),
    UI("`Space la`", "On code with a problem or a possible refactor", "A list of fixes and refactors to pick from", "Code actions (like Cmd-.). Pick with `j`/`k` and Enter.",
       ["Popups() >= 1 || index(WinFts(), 'lsp-quickpick-filter') >= 0"], before="const x = ▌1 + 2;\nconsole.log(x);", file="web/act.ts", setup=WAIT,
       steps=[["<Space>la", 3000, "xt!"]], requires=TS),
]),

section("Errors and warnings", "Problems are marked in the left column and shown at the end of the line.", [
    E("`]g` / `[g`", "Anywhere", "▌count: int = \"not a number\"\nvalue = undefined_name", "count: int = ▌\"not a number\"\nvalue = undefined_name",
      "Next / previous problem. Here the first is the text that isn't a number.", file="broken.py", setup=WAIT, feed="gg]g", wait=500, requires=PY),
    UI("`Space ld`", "In a file", "A list of every problem in the file", "All problems at once (like VS Code's Problems panel).",
       ["LocLen() + QfLen() >= 2"], before="count: int = \"not a number\"\nvalue = undefined_name", file="broken.py", setup=WAIT,
       feed="<Space>ld", wait=1500, requires=PY),
    UI("`:LspStatus` Enter", "In a code file", "Shows whether the language server is running", "Check this first when `gd` does nothing.",
       ["execute('LspStatus') =~# 'running'"], before="x = 1", file="app.py", setup=WAIT, requires=PY),
    M("`:LspInstallServer` Enter", "In a file of the language", "Downloads and sets up that language's server", "Run once per language.",
      "Downloads from the internet; this test machine installed its servers this way beforehand."),
]),

section("Completion", """\
Suggestions appear as you type in files with a language server. `Ctrl-n` /
`Ctrl-p` complete from words already in your open files, in any file.""", [
    E("`Ctrl-n` / `Ctrl-p`", "While typing a word", "alphabet\n▌", "alphabet\nalphabet▌", "Complete from words in open files. With one match it's filled straight in.",
      feed="Aalph<C-n>", mode="i"),
    E("`Tab` / `Shift-Tab`, then `Enter`", "While the suggestion menu is open", APP.format(cur="▌"),
      APP.format(cur="").replace("total = add(1, 2)", "total = add(1, 2)\ngreet▌"),
      "Move down / up the menu, then accept with `Enter`. (When the menu is closed, `Tab` takes Copilot's suggestion or indents.)",
      file="app.py", setup=WAIT, steps=[["ogre", 6000, "xt!"], ["<Tab>", 400], ["<CR>", 400]], mode="i", requires=PY),
    E("`Ctrl-e`", "While the suggestion menu is open", "alphabet\nalphas\n▌", "alphabet\nalphas\nalph▌", "Close the menu and keep what you typed.",
      feed="Aalph<C-n><C-e>", mode="i"),
]),

section("Indentation", "", [
    E("`gg=G`", "Anywhere", "▌function f() {\nreturn 1;\n}", "▌function f() {\n  return 1;\n}", "Re-indent the whole file. `=ip` does a paragraph, `==` a line.", file="code.js", check_cursor=False),
    E("`:retab` Enter", "Anywhere", "▌\tx", "▌    x", "Turn Tab characters into spaces.", feed=":retab<CR>", check_cursor=False),
]),

section("Folding", """\
Fold (collapse) blocks of code. Here folding follows indentation; to make that
the default, put `set foldmethod=indent` in `~/.vimrc.local`.""", [
    UI("`zc` / `zo`", "Inside an indented block", "The block collapses into one line / opens again", "Close / open a fold.",
       ["foldclosed(2) == 2"], before="def f():\n    ▌a = 1\n    b = 2\nx = 3", file="fold.py",
       setup=["setlocal foldmethod=indent foldlevel=99"], feed="zc"),
    UI("`za`", "On a fold", "Toggles it", "Open if closed, close if open.",
       ["foldclosed(2) == -1"], before="def f():\n    ▌a = 1\n    b = 2\nx = 3", file="fold.py",
       setup=["setlocal foldmethod=indent foldlevel=99"], feed="zcza"),
    UI("`zM` / `zR`", "Anywhere", "Every fold closes / opens", "Overview of a long file, then back.",
       ["string(map(range(1, 7), 'foldclosed(v:val)')) ==# '[-1, 2, 2, -1, -1, 6, 6]'"], before="def f():\n    ▌a = 1\n    a = 2\n\ndef g():\n    b = 1\n    b = 2", file="fold.py",
       setup=["setlocal foldmethod=indent foldlevel=99"], feed="zM"),
    UI("`zj` / `zk`", "Anywhere", "The cursor moves to the next / previous fold", "Jump between folds. (A fold needs at least 2 lines to close.)",
       ["line('.') == 2"], before="▌x = 1\n    a = 1\n    b = 2", file="fold.py",
       setup=["setlocal foldmethod=indent foldlevel=99"], feed="zj"),
    UI("`zfj`", "Anywhere (with manual folding)", "This line and the next become a closed fold", "`zf` + any motion makes a fold by hand.",
       ["foldclosed(1) == 1"], before="▌a\nb\nc", setup=["setlocal foldmethod=manual"], feed="zfj"),
]),

section("Spelling", "Commit messages get spell checking automatically.", [
    UI("`:setlocal spell` Enter", "Anywhere", "Misspelled words are underlined", "`:setlocal nospell` turns it off.",
       ["&spell"], before="▌wrnog", feed=":setlocal spell<CR>"),
    E("`]s` / `[s`", "With spelling on", "▌This is wrnog text", "This is ▌wrnog text", "Next / previous misspelled word.",
      setup=["setlocal spell"], feed="]s"),
    E("`z=`, number, Enter", "On a misspelled word", "This is ▌wrnog", "This is ▌wrong", "Pick a suggestion from the list.",
      setup=["setlocal spell"], feed="z=1<CR>"),
    UI("`zg`", "On a correctly spelled word Vim doesn't know", "It's no longer marked", "Add the word to your dictionary. `zw` marks one as wrong.",
       ["spellbadword('vimsetupword')[0] ==# ''"], before="▌vimsetupword",
       setup=["setlocal spell", "let &l:spellfile = tempname() . '.utf-8.add'"], feed="zg"),
]),

section("Run code and commands", "", [
    UI("`:!python3 %` Enter", "In a Python file", "The file runs; its output shows, press Enter to return", "`:!` runs any shell command; `%` is the current file.",
       ["filereadable('ran.txt')"], setup=["edit hello.py"], feed=":!python3 %<CR><CR>", requires=["exe:python3"]),
    E("`:r !echo hi` Enter", "On the line to insert below", "▌top", "top\n▌hi", "Insert a command's output into the file.", feed=":r !echo hi<CR>"),
    UI("`:make` Enter", "In a project with a Makefile", "Errors go to the quickfix list, and Vim jumps to the first",
       "Build and jump straight to the errors. `:make check` runs the `check` target.",
       ["QfLen() >= 1", "expand('%:t') ==# 'app.py'", "line('.') == 2"], feed=":make check<CR><CR>", requires=["exe:make"]),
]),
])
