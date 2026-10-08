from kit import E, section, level

LEVEL = level(2, "Basic edits", """\
Ways into Insert mode, and single keys that change text without entering it.
The examples type `X` (or a word) and then press `Esc`; the result is what you
see after `Esc`, which steps the cursor back one character.""", [

section("Ways into Insert mode", "Each starts typing at a different place. Pick the one that saves a move.", [
    E("`i`", "On the `c`", "ab▌cd", "ab▌Xcd", "Insert **before** the cursor.", feed="iX<Esc>"),
    E("`a`", "On the `c`", "ab▌cd", "abc▌Xd", "**A**ppend after the cursor.", feed="aX<Esc>"),
    E("`I`", "Anywhere on the line", "    ab▌cd", "    ▌Xabcd", "Insert at the start of the text, after the indent.", feed="IX<Esc>"),
    E("`A`", "Anywhere on the line", "ab▌cd", "abcd▌X", "Append at the end of the line. The one you'll use most.", feed="AX<Esc>"),
    E("`o`", "Anywhere on the line", "ab▌c\nxyz", "abc\nne▌w\nxyz", "Open a new line **below** and start typing.", feed="onew<Esc>"),
    E("`O`", "Anywhere on the line", "abc\nx▌yz", "abc\nne▌w\nxyz", "Open a new line **above**.", feed="Onew<Esc>"),
    E("`s`", "On the `c`", "ab▌cd", "ab▌Xd", "**S**ubstitute: delete the character, then type.", feed="sX<Esc>"),
    E("`S`  or  `cc`", "Anywhere on the line", "    ab▌cd", "    ne▌w", "Replace the whole line's text, keeping its indent.", feed="Snew<Esc>"),
    E("`C`", "On the `c`", "ab▌cd", "ab▌X", "Change to the end of the line.", feed="CX<Esc>"),
    E("`gi`", "Anywhere, after you inserted text somewhere else", "▌abc\nxyz", "abcX▌Y\nxyz",
      "Go back to where you last typed and keep typing there. Here: typed `X` at the end of line 1, moved down, then `gi` + `Y`.",
      feed="AX<Esc>jgiY<Esc>"),
]),

section("While typing (Insert mode)", "Small fixes without leaving Insert mode.", [
    E("`Ctrl-w`", "While typing", "▌", "one ▌", "Delete the word before the cursor.", feed="ione two<C-w>", mode="i"),
    E("`Ctrl-u`", "While typing", "▌", "▌", "Delete everything typed on this line.", feed="ione two<C-u>", mode="i"),
    E("`Ctrl-o` + a command", "While typing", "▌", "X▌ab", "Run one Normal-mode command and keep typing. Here `Ctrl-o` `0` jumps to the line start, then `X` is typed.", feed="iab<C-o>0X", mode="i"),
    E("`Ctrl-t` / `Ctrl-d`", "While typing", "▌", "    x▌", "Indent / unindent the current line.", feed="ix<C-t>", mode="i"),
    E("`Ctrl-v` `Tab`", "While typing", "▌", "\tx▌", "Insert the next key literally — here a real Tab character instead of spaces.", feed="i<C-v><Tab>x", mode="i"),
]),

section("Single-key changes", "", [
    E("`x`", "On the `c`", "ab▌cd", "ab▌d", "Delete the character under the cursor."),
    E("`X`", "On the `c`", "ab▌cd", "a▌cd", "Delete the character before the cursor (like Backspace)."),
    E("`rz`", "On the `c`", "ab▌cd", "ab▌zd", "**R**eplace one character with `z` (or any key), without entering Insert mode."),
    E("`~`", "On the `a`", "▌abc", "A▌bc", "Toggle upper/lower case and move right. Hold it to change a run of letters."),
    E("`J`", "On line 1", "▌one\ntwo", "one▌ two", "**J**oin the next line onto this one, with a space between."),
    E("`gJ`", "On line 1", "▌one\ntwo", "one▌two", "Join without adding a space."),
    E("`D`", "On the `c`", "ab▌cd", "a▌b", "Delete from the cursor to the end of the line."),
    E("`dd`", "Anywhere on the line", "o▌ne\ntwo", "▌two", "Delete the whole line (it's kept for pasting with `p`)."),
    E("`3x`", "On the `a`", "▌abcdef", "▌def", "Counts work here too: delete 3 characters."),
    E("`2dd`", "On line 1", "▌one\ntwo\nthree", "▌three", "Delete 2 lines."),
]),

section("Numbers", "", [
    E("`Ctrl-a`", "Anywhere before or on the number", "▌x = 5", "x = ▌6", "Add 1 to the next number on the line — the cursor doesn't need to be on it.", feed="<C-a>"),
    E("`Ctrl-x`", "Anywhere before or on the number", "▌x = 10", "x = ▌9", "Subtract 1.", feed="<C-x>"),
    E("`5` `Ctrl-a`", "Anywhere before the number", "▌x = 5", "x = 1▌0", "Add 5.", feed="5<C-a>"),
]),

section("Quick fixes", "", [
    E("`xp`", "On the first of two swapped letters", "t▌eh", "th▌e", "Swap two characters: delete one, paste it after the next."),
    E("`ddp`", "On the upper line", "▌one\ntwo", "two\n▌one", "Swap a line with the one below."),
    E("`ddkP`", "On the lower line", "one\n▌two", "▌two\none", "Swap a line with the one above."),
]),

section("Repeat: the dot", """\
`.` repeats your last change, wherever the cursor is now. Make a change once,
then move and press `.` — this is how Vim users avoid typing anything twice.""", [
    E("`.`", "After any change", "▌a b c", "▌c", "Here `dw` deleted `a `, then `.` deleted `b ` too.", feed="dw."),
    E("`.` after Insert", "After typing something", "▌one\ntwo", "one;\ntwo▌;",
      "Repeats a whole insert: here `A;` `Esc` on line 1, then `j` and `.` on line 2.", feed="A;<Esc>j."),
]),
])
