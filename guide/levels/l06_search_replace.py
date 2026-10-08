from kit import E, UI, section, level

LEVEL = level(6, "Search and replace", """\
Searching is also the fastest way to *move*: `/word` Enter jumps straight
there. This config ignores case unless you type a capital letter, and
highlights matches as you type.""", [

section("Search in the file", "", [
    E("`/foo` Enter", "Anywhere", "▌a foo b foo", "a ▌foo b foo", "Jump to the next `foo`.", feed="/foo<CR>"),
    E("`?foo` Enter", "Anywhere", "a foo b foo▌.", "a foo b ▌foo.", "Search backwards.", feed="?foo<CR>"),
    E("`n` / `N`", "After a search", "▌a foo b foo", "a foo b ▌foo", "Next / previous match (here `n` after `/foo`).", feed="/foo<CR>n"),
    E("`*`", "On a word", "▌foo bar foo", "foo bar ▌foo", "Search for the word under the cursor, forwards. No typing needed."),
    E("`#`", "On a word", "foo bar ▌foo", "▌foo bar foo", "Same, backwards."),
    E("`/\\<is\\>` Enter", "Anywhere", "▌this is", "this ▌is", "`\\<` and `\\>` mark word edges: finds `is`, not the `is` inside `this`.", feed="/\\<is\\><CR>"),
    E("`/foo` finds `Foo`", "Anywhere", "▌x Foo", "x ▌Foo", "Lowercase searches ignore case.", feed="/foo<CR>"),
    E("`/Foo` Enter", "Anywhere", "▌foo Foo", "foo ▌Foo", "A capital letter makes the search match case exactly.", feed="/Foo<CR>"),
    E("`/foo\\C` Enter", "Anywhere", "▌x Foo foo", "x Foo ▌foo", "`\\C` anywhere in the search forces exact case.", feed="/foo\\C<CR>"),
    E("`/` then `Up`", "Anywhere", "▌x foo", "x ▌foo", "Browse earlier searches with the arrow keys. Here: searched `foo`, went back to the start, then `/` `Up` Enter.", feed="/foo<CR>0/<Up><CR>"),
    UI("`Space h`", "After searching", "The match highlighting disappears", "Clear the highlight (until the next search).",
       ["!v:hlsearch"], before="▌a foo", feed="/foo<CR><Space>h"),
]),

section("Change every match, one at a time", "Faster than `:s` when you want to check each one.", [
    E("`cgn` then `.`", "After searching (here `*` on `foo`, then `N` back to the first)", "▌foo x foo x foo", "bar x bar x bar",
      "`cgn` changes the next match; each `.` changes the one after. Press `n` to skip one.",
      feed="*Ncgnbar<Esc>..", check_cursor=False),
]),

section("Substitute: :s", """\
`:s/old/new/` replaces text. `%` means every line; `g` every match on a line,
not just the first; `c` asks before each one.""", [
    E("`:s/a/b/` Enter", "On the line", "▌a a\na", "b a\na", "First match on this line.", feed=":s/a/b/<CR>", check_cursor=False),
    E("`:s/a/b/g` Enter", "On the line", "▌a a\na", "b b\na", "Every match on this line.", feed=":s/a/b/g<CR>", check_cursor=False),
    E("`:%s/a/b/g` Enter", "Anywhere", "▌a a\na", "b b\nb", "Every match in the file.", feed=":%s/a/b/g<CR>", check_cursor=False),
    E("`:%s/a/b/gc` Enter, then `y` `n` `y`", "Anywhere", "▌a a a", "b a b",
      "Ask before each one: `y` yes, `n` no, `a` all the rest, `q` stop.", feed=":%s/a/b/gc<CR>yny", check_cursor=False),
    E("`:%s//new/g` Enter", "After a search", "▌old x old", "new x new", "An empty search part reuses your last search.", feed="/old<CR>:%s//new/g<CR>", check_cursor=False),
    E("`:%s/\\s\\+$//e` Enter", "Anywhere", "▌a  \nb ", "a\nb", "Remove trailing spaces. `e` means don't complain if there are none.", feed=":%s/\\s\\+$//e<CR>", check_cursor=False),
    E("`&`", "On another line, after a `:s`", "▌a a\na a", "b a\nb a", "Repeat the last `:s` on the current line.", feed=":s/a/b/<CR>j&", check_cursor=False),
    E("`g&`", "Anywhere, after a `:s`", "▌a a\na a", "b b\nb b", "Repeat the last `:s` on every line.", feed=":s/a/b/g<CR>g&", check_cursor=False),
    E("`:%s/\\v(\\w+) (\\w+)/\\2 \\1/` Enter", "Anywhere", "▌hello world", "world hello",
      "Groups: `\\v` lets you write `( )` plainly; `\\1`, `\\2` put back what each group matched. Here: swap two words.",
      feed=":%s/\\v(\\w+) (\\w+)/\\2 \\1/<CR>", check_cursor=False),
    E("`:s/, /\\r/g` Enter", "On the line", "▌a, b, c", "a\nb\nc", "`\\r` in the replacement starts a new line.", feed=":s/, /\\r/g<CR>", check_cursor=False),
]),

section("Act on matching lines: :g and :v", "", [
    E("`:g/x/d` Enter", "Anywhere", "▌keep\nx1\nkeep\nx2", "keep\nkeep", "Delete every line containing `x`.", feed=":g/x/d<CR>", check_cursor=False),
    E("`:v/x/d` Enter", "Anywhere", "▌keep\nx1\nkeep\nx2", "x1\nx2", "Delete every line **not** containing `x`.", feed=":v/x/d<CR>", check_cursor=False),
    E("`:g/x/normal A;` Enter", "Anywhere", "▌keep\nx1\nkeep\nx2", "keep\nx1;\nkeep\nx2;", "Run Normal-mode keys on every matching line.", feed=":g/x/normal A;<CR>", check_cursor=False),
]),

section("Search the whole project", """\
`Space s` searches every file (it uses ripgrep, so it's fast and skips
what's in `.gitignore` and your hidden list). The results can go to the
**quickfix list** — a list of places you can step through or edit all at once.""", [
    UI("`Space s`, type, `Enter`", "Anywhere in the project", "A search window; Enter opens the file at the match",
       "Type to filter the matching lines live; Enter jumps there.",
       ["expand('%:t') ==# 'util.py'", "getline('.') =~# 'import add'"],
       steps=[["<Space>s", 1500], ["import add", 1500], ["<CR>", 1500]], requires=["plugin:fzf.vim", "exe:rg"]),
    UI("`Space s`, type, `Alt-a`, `Enter`", "Anywhere in the project", "Every match goes into the quickfix list",
       "`Alt-a` selects all results, then `Enter`. On a Mac, Alt must be set to send Esc: iTerm2 → Profiles → Keys → Left Option key: Esc+; Terminal.app → Settings → Profiles → Keyboard → Use Option as Meta key.",
       ["QfLen() == 3"], steps=[["<Space>s", 1500], ["add(", 1500], ["<Esc>a", 800], ["<CR>", 1500]],
       requires=["plugin:fzf.vim", "exe:rg"]),
    UI("`:grep add` Enter", "Anywhere in the project", "Matches go into the quickfix list",
       "Project search without the popup (also uses ripgrep here). Then `:copen` to see them.",
       ["QfLen() >= 4"], feed=":grep! add<CR>", requires=["exe:rg"]),
    UI("`:cdo s/old/new/g | update` Enter", "After filling the quickfix list", "Every listed line is changed and saved",
       "Project-wide replace: search first, check the list, then run this.",
       ["Disk('util.py') =~# 'plus(3, 4)'", "Disk('app.py') =~# 'def plus'"],
       feed=":grep! add<CR>:cdo s/add/plus/g | update<CR>", requires=["exe:rg"]),
    UI("`:copen` / `:cclose` Enter", "After a project search", "The quickfix list opens / closes at the bottom",
       "Enter on a line in the list jumps there.", ["index(WinFts(), 'qf') >= 0"],
       feed=":grep! add<CR>:copen<CR>", requires=["exe:rg"]),
    UI("`:cnext` / `:cprev` Enter", "After a project search", "Next / previous match, opening its file",
       "Step through the results. `:cfirst` and `:clast` jump to the ends.",
       ["getqflist({'idx': 0}).idx == 2"], feed=":grep! add<CR>:cfirst<CR>:cnext<CR>", requires=["exe:rg"]),
]),
])
