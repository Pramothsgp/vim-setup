from kit import E, UI, section, level

LONG = "\n".join(f"line {n}" for n in range(1, 101))

LEVEL = level(1, "Moving around", """\
In Normal mode you move with keys instead of the mouse or arrow keys. Start
with `h j k l`, then learn word and line jumps — they're what makes Vim fast.
Every motion takes a count: `3w` moves three words.""", [

section("Characters and lines", "", [
    E("`h` / `l`", "On the `c`", "ab▌cd", "a▌bcd", "Left / right one character. (`l` would land on `d`.)", feed="h"),
    E("`j` / `k`", "On the `b` of `abc`", "a▌bc\nxyz", "abc\nx▌yz",
      "Down / up one line, keeping the column.", feed="j"),
    E("`3l`", "On the `a`", "▌abcdef", "abc▌def", "A count repeats the motion: 3 characters right."),
    E("`2j`", "On line 1", "▌one\ntwo\nthree", "one\ntwo\n▌three", "Down 2 lines."),
]),

section("Words", """\
A **word** is letters, digits and `_`; punctuation counts as its own word. A
**WORD** (capital keys) is anything between spaces.""", [
    E("`w`", "On the `f`", "▌foo.bar baz", "foo▌.bar baz", "Start of the next word: `.` counts as a word."),
    E("`W`", "On the `f`", "▌foo.bar baz", "foo.bar ▌baz", "Start of the next WORD: skips to after the space."),
    E("`b`", "On the `b` of `baz`", "foo.bar ▌baz", "foo.▌bar baz", "Back to the start of the previous word."),
    E("`B`", "On the `b` of `baz`", "foo.bar ▌baz", "▌foo.bar baz", "Back to the start of the previous WORD."),
    E("`e`", "On the `f`", "▌foo bar", "fo▌o bar", "To the end of the word."),
    E("`E`", "On the `f`", "▌foo.bar baz", "foo.ba▌r baz", "To the end of the WORD."),
    E("`ge`", "On the `r` of `bar`", "foo ba▌r", "fo▌o bar", "Back to the end of the previous word."),
]),

section("Within the line", "", [
    E("`0`", "Anywhere on the line", "    hello wor▌ld", "▌    hello world", "Very start of the line, even before the indent."),
    E("`^`", "Anywhere on the line", "    hello wor▌ld", "    ▌hello world", "First non-blank character: where the code starts."),
    E("`$`", "Anywhere on the line", "▌hello world", "hello worl▌d", "Last character of the line."),
    E("`f,`", "At the start", "▌call(a, b, c)", "call(a▌, b, c)", "**f**ind: jump onto the next `,` on this line. Works with any character."),
    E("`;`", "After `f,`", "▌call(a, b, c)", "call(a, b▌, c)", "Repeats the last `f`/`t`/`F`/`T` — on to the next `,`.", feed="f,;"),
    E("`,`", "After `f,` `;`", "▌call(a, b, c)", "call(a▌, b, c)", "Repeats it the other way.", feed="f,;,"),
    E("`t,`", "At the start", "▌call(a, b, c)", "call(▌a, b, c)", "**t**ill: jump to just before the next `,`. Great with `d` and `c` later."),
    E("`F(`", "At the end", "call(a, b, ▌c)", "call▌(a, b, c)", "Like `f`, but backwards."),
    E("`T(`", "At the end", "call(a, b, ▌c)", "call(▌a, b, c)", "Like `t`, but backwards: stops just after the `(`."),
]),

section("Whole file", "", [
    E("`gg`", "Anywhere", "one\ntwo\nth▌ree", "▌one\ntwo\nthree", "First line."),
    E("`G`", "Anywhere", "o▌ne\ntwo\nthree", "one\ntwo\n▌three", "Last line."),
    E("`2G`  or  `:2` Enter", "Anywhere", "▌one\ntwo\nthree", "one\n▌two\nthree",
      "Go to line 2. Line numbers are on the left; relative numbers show how far other lines are, for `5j`-style jumps.",
      feed="2G"),
    E("`50%`", "Anywhere", "▌1\n2\n3\n4", "1\n▌2\n3\n4", "Jump to a percentage of the file: halfway."),
    E("`{` / `}`", "In the first paragraph", "o▌ne\ntwo\n\nthree", "one\ntwo\n▌\nthree",
      "Previous / next blank line — jumps between paragraphs or blocks of code.", feed="}"),
    E("`%`", "On a bracket", "if ▌(a and (b or c)):", "if (a and (b or c)▌):",
      "Jumps to the matching bracket: `()`, `[]`, `{}`."),
    E("`[(`", "Inside the parentheses", "f(a, ▌b)", "f▌(a, b)", "Back to the `(` that encloses the cursor. `])` goes to its `)`; `[{` and `]}` do the same for braces."),
    E("`]}`", "Inside a `{ }` block", "if x {\n  y = ▌1\n}", "if x {\n  y = 1\n▌}", "Forward to the enclosing `}`."),
    E("`)` / `(`", "In a sentence", "▌One. Two. Three.", "One. ▌Two. Three.", "Next / previous sentence.", feed=")"),
]),

section("Screen", """\
This config keeps 8 lines visible above and below the cursor, so the screen
scrolls before you reach the edge.""", [
    UI("`Ctrl-d` / `Ctrl-u`", "Anywhere in a long file", "The view and cursor move half a screen down / up",
       "Half-page scrolling — the quickest way to read through a file.",
       ["line('.') > 1", "line('w0') > 1"], before=LONG, feed="<C-d>"),
    UI("`Ctrl-f` / `Ctrl-b`", "Anywhere in a long file", "A full screen down / up", "Page down / page up.",
       ["line('w0') > winheight(0) - 5"], before=LONG, feed="<C-f>"),
    UI("`Ctrl-e` / `Ctrl-y`", "Anywhere in a long file", "The view scrolls one line; the cursor stays on its line",
       "Scroll without moving the cursor (until it would leave the screen).",
       ["line('w0') == 2", "line('.') == 15"], before=LONG, setup=["15"], feed="<C-e>"),
    UI("`zz`", "Anywhere", "The cursor's line moves to the middle of the window",
       "Centre the screen on the cursor. `zt` puts it at the top, `zb` at the bottom (keeping the 8-line margin).",
       ["abs(winline() - (winheight(0) + 1) / 2) <= 1"], before=LONG, setup=["60"], feed="zz"),
    UI("`H` / `M` / `L`", "Anywhere", "Cursor to the top / middle / bottom of the window",
       "Jump to the screen's top, middle or bottom (8 lines from the edge, because of the margin).",
       ["line('.') == line('w0') + 8"], before=LONG, setup=["40", "normal! zz"], feed="H"),
]),
])
