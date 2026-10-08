from kit import E, section, level

LEVEL = level(3, "The grammar: operator + motion", """\
This is the idea that makes Vim click. An **operator** (what to do) followed
by a **motion** (how far) is a complete command: `d` + `w` deletes a word,
`c` + `$` changes to the end of the line, `y` + `}` copies to the end of the
paragraph. Learn one new operator and it works with every motion you know;
learn one new motion and it works with every operator. Doubling an operator
(`dd`, `cc`, `yy`, `>>`, `gUU`) applies it to the whole line.""", [

section("Delete: d", "", [
    E("`dw`", "On the first letter of `one`", "▌one two", "▌two", "Delete to the start of the next word (the space goes too)."),
    E("`de`", "On the first letter of `one`", "▌one two", "▌ two", "Delete to the end of the word (the space stays)."),
    E("`d$`  (same as `D`)", "On the `e` of `one`", "on▌e two", "o▌n", "Delete to the end of the line.", feed="d$"),
    E("`d0`", "On the `w` of `two`", "one t▌wo", "▌wo", "Delete back to the start of the line."),
    E("`dt)`", "On the `a`", "f(▌a, b)", "f(▌)", "Delete **till** the `)`: everything up to, not including, it."),
    E("`df,`", "On the `a`", "▌a, b", "▌ b", "Delete up to and **including** the `,`."),
    E("`dj`", "On line 1", "▌1\n2\n3", "▌3", "Delete this line and the one below (vertical motions delete whole lines)."),
    E("`dG`", "On line 2", "1\n▌2\n3", "▌1", "Delete to the end of the file."),
    E("`dgg`", "On line 2", "1\n▌2\n3", "▌3", "Delete to the start of the file."),
    E("`d}`", "On line 1", "▌a\nb\n\nc", "▌\nc", "Delete to the end of the paragraph."),
    E("`d2w`  or  `2dw`", "On the `a`", "▌a b c", "▌c", "A count can go before the operator or the motion.", feed="d2w"),
]),

section("Change: c", "`c` deletes like `d`, then leaves you in Insert mode to type the replacement.", [
    E("`cw`", "On the first letter of `one`", "▌one two", "ne▌w two", "Change the word. (`cw` stops at the end of the word, like `ce`.)", feed="cwnew<Esc>"),
    E("`c$`  (same as `C`)", "On the `t`", "one ▌two", "one ▌X", "Change to the end of the line.", feed="c$X<Esc>"),
    E("`ct)`", "On the `a`", "f(▌a, b)", "f(▌x)", "Change everything up to the `)`.", feed="ct)x<Esc>"),
    E("`cc`", "Anywhere on the line", "    ▌hello", "    ▌X", "Change the whole line, keeping the indent.", feed="ccX<Esc>"),
]),

section("Copy (yank): y — and paste: p", """\
Vim calls copying **yanking**. `p` pastes after the cursor (below the line,
for whole lines), `P` before (above).""", [
    E("`yw` then `P`", "On the first letter of `one`", "▌one two", "one▌ one two", "Copy a word, then paste it in front of the cursor.", feed="ywP"),
    E("`yy` then `p`", "Anywhere on line 1", "▌one\ntwo", "one\n▌one\ntwo", "Copy the line, paste it below.", feed="yyp"),
    E("`yy` then `P`", "Anywhere on line 2", "one\n▌two", "one\n▌two\ntwo", "Copy the line, paste it above.", feed="yyP"),
    E("`y$` then `$p`", "On the `t` of `two`", "one ▌two", "one twotw▌o", "Copy to the end of the line, then paste it at the end. The cursor lands on the last pasted character.", feed="y$$p"),
]),

section("Indent: > and <", "This config indents by 4 spaces (2 for web files).", [
    E("`>>`", "Anywhere on the line", "▌if x:", "    ▌if x:", "Indent the line."),
    E("`<<`", "Anywhere on the line", "    ▌x", "▌x", "Remove one level of indent."),
    E("`>j`", "On line 1", "▌a\nb", "    ▌a\n    b", "Indent this line and the next."),
    E("`>ip`", "Anywhere in the paragraph", "a\n▌b\n\nc", "    ▌a\n    b\n\nc", "Indent the paragraph (`ip` is a text object — next level)."),
]),

section("Case: gU, gu, g~", "", [
    E("`gUiw`", "Anywhere in the word", "hel▌lo world", "▌HELLO world", "Uppercase the word."),
    E("`guu`", "Anywhere on the line", "HELLO ▌World", "▌hello world", "Lowercase the whole line."),
    E("`gUU`", "Anywhere on the line", "hello ▌world", "▌HELLO WORLD", "Uppercase the whole line."),
    E("`g~w`", "On the first letter", "▌Hello world", "▌hELLO world", "Toggle the case of a word."),
]),

section("Format and filter", "", [
    E("`gqq`", "Anywhere on a long line (here with the width set to 20)", "▌one two three four five six seven",
      "one two three four\n▌five six seven", "Re-wrap the line to the text width. `gqip` re-wraps a paragraph.",
      setup=["setlocal textwidth=20"]),
    E("`!ip` `sort` Enter", "Anywhere in the paragraph", "c\n▌b\na", "▌a\nb\nc",
      "Send the paragraph through a shell command and replace it with the output. Here `sort`.",
      feed="!ipsort<CR>"),
]),
])
