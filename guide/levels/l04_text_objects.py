from kit import E, section, level

LEVEL = level(4, "Text objects", """\
Text objects let an operator act on a *thing* — a word, the text inside
quotes, a function call's arguments — no matter where in it the cursor is.
They start with `i` (**inside**) or `a` (**around**, including the quotes,
brackets or surrounding space). Use them after `d`, `c`, `y`, `v`, `gU`...
`ci"` (change inside quotes) is the one you'll use daily.""", [

section("Words and sentences", "", [
    E("`diw`", "Anywhere in the word", "one tw▌o three", "one ▌ three", "Delete the word, leave the spaces."),
    E("`daw`", "Anywhere in the word", "one tw▌o three", "one ▌three", "Delete the word and one space."),
    E("`ciw`", "Anywhere in the word", "one tw▌o three", "one ne▌w three", "Change the word.", feed="ciwnew<Esc>"),
    E("`diW`", "Anywhere in the WORD", "a foo.b▌ar c", "a ▌ c", "A WORD includes punctuation: `foo.bar` goes as one."),
    E("`dis`", "Anywhere in the sentence", "One. T▌wo here. Three.", "One. ▌ Three.", "Delete the sentence, leaving the spaces around it. `das` takes a space with it."),
]),

section("Quotes", "Works from anywhere inside the quotes — or even before them on the same line.", [
    E("`ci\"`", "Inside the quotes", "say(\"hel▌lo there\")", "say(\"h▌i\")", "Change inside double quotes.", feed="ci\"hi<Esc>"),
    E("`ci\"`", "Before the quotes, on the same line", "▌x = \"old\"", "x = \"ne▌w\"", "Vim looks ahead for the next quotes.", feed="ci\"new<Esc>"),
    E("`di\"`", "Inside the quotes", "say(\"hel▌lo\")", "say(\"▌\")", "Delete inside double quotes."),
    E("`da\"`", "Inside the quotes", "x = \"a▌b\" + y", "x = ▌+ y", "Delete the quotes too, and the space after them."),
    E("`ci'`", "Inside the quotes", "name = 'B▌ob'", "name = 'Alic▌e'", "Same for single quotes.", feed="ci'Alice<Esc>"),
    E("`` di` ``", "Inside the backticks", "run `l▌s -l` now", "run `▌` now", "Same for backticks.", feed="di`"),
]),

section("Brackets", "`b` is short for `(`, and `B` for `{`.", [
    E("`di(`  or  `dib`", "Anywhere inside the parentheses", "f(a, ▌b)", "f(▌)", "Delete the arguments.", feed="di("),
    E("`ci(`", "Anywhere inside", "f(a, ▌b)", "f(▌x)", "Change the arguments.", feed="ci(x<Esc>"),
    E("`da(`  or  `dab`", "Anywhere inside", "f(a, ▌b)", "▌f", "Delete the parentheses and what's in them.", feed="da("),
    E("`di{`  or  `diB`", "Inside a `{ }` block", "if x {\n    a = 1\n    b▌ = 2\n}", "if x {\n▌}", "Delete everything inside the braces.", feed="di{"),
    E("`ci{`", "Inside a `{ }` block", "if x {\n    ▌a = 1\n}", "if x {\n    ▌y\n}", "Replace the block's contents.", feed="ci{y<Esc>"),
    E("`di[`", "Inside the square brackets", "x[▌1, 2]", "x[▌]", "Delete inside `[ ]`."),
    E("`di<`", "Inside the angle brackets", "List<Str▌ing>", "List<▌>", "Delete inside `< >`."),
]),

section("Tags and paragraphs", "", [
    E("`dit`", "Anywhere inside the tag's text", "<p>he▌llo</p>", "<p>▌</p>", "Delete inside an HTML/XML tag."),
    E("`cit`", "Anywhere inside", "<p>he▌llo</p>", "<p>by▌e</p>", "Change a tag's text.", feed="citbye<Esc>"),
    E("`dat`", "Anywhere inside", "x <b>b▌old</b> y", "x ▌ y", "Delete the whole element, tags included."),
    E("`dip`", "Anywhere in the paragraph", "a\n▌b\n\nc", "▌\nc", "Delete the paragraph (the lines up to a blank line)."),
    E("`dap`", "Anywhere in the paragraph", "a\n▌b\n\nc", "▌c", "Delete the paragraph and the blank line after it."),
    E("`yip` then `P`", "Anywhere in the paragraph", "▌a\nb\n\nc", "▌a\nb\na\nb\n\nc", "Copy a paragraph and paste it above.", feed="yipP"),
]),
])
