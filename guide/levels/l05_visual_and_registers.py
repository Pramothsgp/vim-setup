from kit import E, UI, M, section, level

LEVEL = level(5, "Visual mode, copy and paste", """\
Visual mode is for when you want to *see* what you're about to change: select
first, then apply an operator. Then the **registers**: Vim's clipboards. Every
delete and copy lands in one; you can also name your own.""", [

section("Selecting", "Move with any motion to grow the selection. `Esc` cancels.", [
    E("`v` … `d`", "On the `a`", "▌abcdef", "▌def", "Select characters (here 3 with `ll`), then delete them.", feed="vlld"),
    E("`V` … `d`", "Anywhere on line 1", "▌1\n2\n3", "▌3", "Select whole lines (here 2 with `j`), then delete.", feed="Vjd"),
    E("`Ctrl-v` … `d`", "On the first `x`", "a▌xb\naxb\naxb", "a▌b\nab\nab", "Select a block — a rectangle, column by column. Here the column of `x`s.", feed="<C-v>jjd"),
    E("`gv`", "After a selection ended", "▌abcd", "a▌bcd", "Reselect the last selection.", feed="vl<Esc>gv", mode="v", sel="ab"),
    E("`o`", "In a selection", "▌abcd", "▌abcd", "Jump to the other end of the selection, to grow it from that side.", feed="vllo", mode="v", sel="abc"),
    E("`vip`", "Anywhere in the paragraph", "a\n▌b\n\nc", "a\n▌b\n\nc", "Select a paragraph (any text object works: `vi\"`, `va(`...).", feed="vip", mode="V", sel="a\nb", check_cursor=False),
    E("`vi\"`", "Inside the quotes", "x = \"he▌llo\"", "x = \"hell▌o\"", "Select inside quotes.", feed="vi\"", mode="v", sel="hello"),
]),

section("Acting on a selection", "", [
    E("`U` / `u` / `~`", "After selecting", "▌hello there", "▌HELLO there", "Uppercase / lowercase / toggle case of the selection.", feed="veU"),
    E("`>` / `<`", "After selecting lines", "▌a\nb", "    a\n▌    b", "Indent / unindent. This config keeps the selection, so press `>` again to indent more.", feed="Vj>", mode="V", sel="    a\n    b"),
    E("`J` / `K`", "After selecting lines", "▌1\n2\n3", "2\n▌1\n3", "Move the selected lines down / up (this config). Keeps the selection.", feed="VJ", mode="V", sel="1"),
    E("`c`", "After selecting", "▌hello there", "bye▌ there", "Change the selection.", feed="vecbye<Esc>", check_cursor=False),
    E("`y` then `P`", "After selecting", "▌ab cd", "a▌bab cd", "Copy the selection, then paste.", feed="vly0P", check_cursor=False),
    E("`:` with a selection", "After selecting lines", "▌a1\na2\nb3", "▌b1\nb2\nb3", "Vim fills in `:'<,'>` — the command runs only on the selected lines. Here `s/a/b/`.", feed="Vj:s/a/b/<CR>", check_cursor=False),
]),

section("Block selection (columns)", "Edit many lines at once: select a column with `Ctrl-v`, then type once.", [
    E("`Ctrl-v` … `I`", "On the first character of the first line", "▌abc\nabc\nabc", "▌# abc\n# abc\n# abc", "Insert at the start of every selected line. The text appears on all lines after `Esc`.", feed="<C-v>jjI# <Esc>"),
    E("`Ctrl-v` … `A`", "On the first character", "▌ab\nab", "a▌b;\nab;", "Append after the block on every line.", feed="<C-v>jlA;<Esc>", check_cursor=False),
    E("`Ctrl-v` … `$A`", "On the first character", "▌ab\nabcd", "ab;\nabcd;", "Append at the end of lines of different lengths.", feed="<C-v>j$A;<Esc>", check_cursor=False),
    E("`Ctrl-v` … `c`", "On the `x` of line 1", "a▌x1\nax2", "aY1\naY2", "Change the block on every line.", feed="<C-v>jcY<Esc>", check_cursor=False),
    E("`g Ctrl-a`", "After selecting lines of zeros", "▌0\n0\n0", "▌1\n2\n3", "Make a numbered sequence: each line gets 1 more than the one above.", feed="VGg<C-a>", check_cursor=False),
]),

section("Registers: Vim's clipboards", """\
`p` pastes the unnamed register: whatever you last deleted or copied. With
this config, copying also puts the text on your system clipboard (when Vim
supports it — Homebrew's Vim does).""", [
    E("`p` / `P`", "On a line, after copying a line", "▌one\ntwo", "one\n▌one\ntwo", "Paste after / before. Whole lines go below / above the cursor's line.", feed="yyp"),
    E("`gp`", "After copying a line", "▌one\ntwo", "one\none\n▌two", "Paste, then put the cursor just after what was pasted.", feed="yygp"),
    E("`\"0p`", "After copying, then deleting something else", "▌keep\ndelete me", "keep\n▌keep", "Register 0 always holds your last *copy*, even after deletes replaced the normal paste.", feed="yyjdd\"0p"),
    E("`\"_dd`", "On a line you want gone", "▌one\ntwo", "one\n▌one", "The `_` register is a black hole: delete without losing what you copied. Here: copy `one`, delete `two` into the hole, paste `one`.", feed="yyj\"_ddp", check_cursor=False),
    E("`\"ayy` / `\"ap`", "On a line", "▌one\ntwo", "one\ntwo\n▌one", "Copy into register `a` (any letter), paste from it later — even after other copies.", feed="\"ayyj\"ap"),
    E("`\"Ayy`", "On another line", "▌one\ntwo", "one\ntwo\n▌one\ntwo", "Capital letter **adds** to register `a` instead of replacing it.", feed="\"ayyj\"Ayy\"ap"),
    UI("`:reg` Enter", "Anywhere", "A list of every register and what's in it", "See what you can paste. `:reg a` shows just `a`.",
       ["execute('registers a') =~# 'one'"], before="▌one", feed="\"ayy:reg a<CR><CR>"),
    E("`Ctrl-r` `\"`", "In Insert mode", "▌one", "one on▌e", "Paste a register while typing (`\"` = last copy; any register letter works).", feed="yiwA <C-r>\"<Esc>"),
    M("`y` → `Cmd-V` elsewhere", "After copying in Vim", "The text pastes into other Mac apps",
      "Copies go to the macOS clipboard, and `p` pastes what you copied in other apps.",
      "Needs Vim built with clipboard support on your Mac (Homebrew's is); this test machine's Vim has none."),
]),
])
