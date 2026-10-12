from kit import E, UI, M, section, level

CHAT = ["plugin:copilot-chat.vim"]
COP = ["plugin:copilot.vim"]

LEVEL = level(12, "AI", """\
Three ways to use AI, each optional at install: **Copilot suggestions**
(grey text as you type), **Copilot Chat** (a chat window), and **agent
panels** for Claude Code and the Copilot CLI that can read and edit your
project. AI keys live under `Space a`. Signing in happens the first time you
use each one, so the sign-in steps can't be tested automatically.""", [

section("Agent panels: Claude Code and Copilot CLI", "", [
    UI("`Space aa`", "Anywhere", "Claude Code opens in a panel on the right", "Toggle the Claude panel; it keeps running when hidden.",
       ["len(TermWins()) == 1", "winlayout()[0] ==# 'row'", "TermText() =~# 'claude stand-in ready'"], feed="<Space>aa", wait=1000, requires=["part:claude"]),
    UI("`Space aa` (again)", "With the panel open", "The panel hides; Claude keeps running", "Hide it.",
       ["empty(TermWins())", "len(term_list()) == 1"], steps=[["<Space>aa", 1000], ["<C-w>h", 300], ["<Space>aa", 300]], requires=["part:claude"]),
    UI("`Space ag`", "Anywhere", "The GitHub Copilot CLI opens in a panel on the right", "Toggle the Copilot CLI panel. Type `/login` in it the first time.",
       ["len(TermWins()) == 1", "TermText() =~# 'copilot stand-in ready'"], feed="<Space>ag", wait=1000, requires=["part:copilot_cli"]),
    UI("`Space af`", "In a file", "The panel opens with `@your/file` typed in, ready for your question", "Give the agent this file as context.",
       ["TermText() =~# '@sample.txt'"], before="▌x", feed="<Space>af", wait=2500, requires=["part:claude"]),
    UI("`Space af` (with lines selected)", "With lines selected", "Types `@your/file lines 2-3`", "Point the agent at exact lines.",
       ["TermText() =~# '@sample.txt lines 2-3'"], before="a\n▌b\nc", feed="Vj<Space>af", wait=2500, requires=["part:claude"]),
    UI("`Ctrl-w h` / `Ctrl-w l`", "In a panel / in the editor", "Moves between the panel and your code", "The panel keeps running while you edit.",
       ["&buftype ==# ''", "len(term_list()) == 1"], steps=[["<Space>aa", 1000], ["<C-w>h", 300]], requires=["part:claude"]),
    UI("(edits appear)", "Any file you have open, when an agent changes it", "The file reloads by itself within a second", "No need to reopen files after Claude or Copilot edits them. (Checked every second while a panel or terminal is open, and whenever you switch windows.)",
       [r"""Child(['notes.txt'], [[':term ++hidden sh<CR>', 1000], {'run': "call writefile(['changed by the agent'], 'notes.txt')"}, ['', 2500], ':call writefile([getline(1)], ''seen.txt'')<CR>', ':qa!<CR>'], 4000).status ==# 'dead'""",
        "Disk('seen.txt') ==# 'changed by the agent'"]),
    M("`Esc`, `Shift-Tab`, `/`…", "Inside the Claude panel", "Claude's own keys: interrupt, change permission mode, commands",
      "Everything Claude Code does in a terminal works in the panel.", "These belong to Claude Code itself and need your Claude account."),
]),

section("Copilot Chat", "", [
    M("`Space ai`", "Anywhere", "A chat window opens (it asks you to sign in with GitHub the first time)", "Ask Copilot anything: type, then `Enter` sends (`Ctrl-j` adds a new line instead).",
      "Opening the chat starts a GitHub sign-in, so it needs your account."),
    M("`Space ai` (with code selected)", "With lines selected", "The chat opens with your code pasted in", "Ask about specific code.",
      "Needs a GitHub sign-in, like the chat itself."),
    M("`#file:` in the chat", "Typing in the chat", "Attaches a project file; `Tab` completes the name", "Give the chat more context.", "Needs a Copilot sign-in to get an answer."),
    M("`Space am`", "Anywhere", "Pick which AI model the chat uses", "Choose a model.", "Needs a Copilot sign-in to list models."),
]),

section("Copilot suggestions as you type", "Run `:Copilot setup` once and follow the steps to sign in.", [
    UI("`Space ac`", "Anywhere", "Suggestions turn off (or back on); a message says which", "Toggle suggestions — handy when they get in the way.",
       ["!copilot#Enabled()"], feed="<Space>ac", requires=COP),
    M("`Tab`", "When grey suggestion text appears", "The suggestion is inserted", "Accept. (If the completion menu is open, `Tab` moves in the menu; `Ctrl-e` closes it.)", "Needs a Copilot sign-in to get suggestions."),
    M("`Ctrl-]`", "When a suggestion shows", "The suggestion disappears", "Dismiss.", "Needs a Copilot sign-in."),
    M("`Ctrl-j` / `Ctrl-k`", "When a suggestion shows", "Next / previous alternative suggestion", "Cycle.", "Needs a Copilot sign-in."),
    M("`Ctrl-l`", "When a suggestion shows", "Only the next word of it is inserted", "Accept part of a suggestion.", "Needs a Copilot sign-in."),
    M("`Space ap`", "Anywhere", "A window with up to 10 suggestions for where you are", "Browse options.", "Needs a Copilot sign-in."),
    M("`:Copilot status` Enter", "Anywhere", "Says whether you're signed in and suggestions work", "Check this when nothing appears.", "Depends on your GitHub account."),
]),
])
