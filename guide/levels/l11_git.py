from kit import E, UI, section, level

G = ["plugin:vim-fugitive"]
GG = ["plugin:vim-gitgutter"]

# app.py has an unsaved change on line 5 for the change-marker cases
CHANGED = ["edit app.py", "call setline(5, 'def greet(person):')", "GitGutter",
           "call WaitFor('len(gitgutter#hunk#hunks(bufnr())) >= 1', 5000)"]
SAVED_CHANGE = ["edit app.py", "call setline(5, 'def greet(person):')", "write"]
CONFLICT = ["call system('printf \"alpha\\\\nBETA from main\\\\ngamma\\\\n\" > notes.txt && git commit -qam main-beta && git merge feature')",
            "edit notes.txt"]

LEVEL = level(11, "Git", """\
Diff, blame, history, staging, commits and conflicts, without leaving Vim.
Git keys live under `Space g`. Any Git command also works as `:Git <command>`.""", [

section("Changes in the file you're editing", """\
Changed lines are marked in the left column: `+` added, `~` changed, `-`
removed. A changed block of lines is called a **hunk**.""", [
    UI("`]c` / `[c`", "Anywhere in a changed file", "Cursor jumps to the next / previous changed block", "Jump between changes.",
       ["line('.') == 5"], setup=CHANGED + ["1"], feed="]c", requires=GG),
    UI("`Space gp`", "On a changed line", "A popup shows what the line was before", "Preview the change.",
       ["Popups() >= 1 || index(WinFts(), 'diff') >= 0"], setup=CHANGED + ["5"], feed="<Space>gp", wait=800, requires=GG),
    UI("`Space ga`", "On a changed line", "Just that change is staged for the next commit", "Stage this hunk (not the whole file).",
       ["Sh('git diff --cached --name-only') ==# 'app.py'"], setup=SAVED_CHANGE + ["GitGutter", "call WaitFor('len(gitgutter#hunk#hunks(bufnr())) >= 1', 5000)", "5"],
       feed="<Space>ga", wait=800, requires=GG),
    UI("`Space gu`", "On a changed line", "The change is undone, back to the last commit", "Undo this hunk.",
       ["getline(5) ==# 'def greet(name):'"], setup=CHANGED + ["5"], feed="<Space>gu", wait=500, requires=GG),
    UI("`dic`  /  `vic`", "On a changed line", "Deletes / selects the changed lines", "`ic` is the changed block as a text object (`ac` includes a blank line after).",
       ["getline(5) =~# 'return \"Hello'"], setup=CHANGED + ["5"], feed="dic", requires=GG),
    UI("`:GitGutterFold` Enter", "In a changed file", "Everything except the changes folds away", "Review just what you changed. Run it again to unfold.",
       ["foldclosed(1) != -1"], setup=CHANGED, feed=":GitGutterFold<CR>", requires=GG),
]),

section("Diff", "", [
    UI("`Space gd`", "In a changed file", "Side by side: the committed version on the left, your file on the right", "Diff this file against what Git has.",
       ["winnr('$') == 2", "winlayout()[0] ==# 'row'", "getwinvar(1, '&diff') && getwinvar(2, '&diff')", "bufname(winbufnr(1)) =~# 'fugitive://'", "bufname(winbufnr(2)) ==# 'app.py'"], setup=SAVED_CHANGE, feed="<Space>gd", requires=G),
    UI("`:Gdiffsplit HEAD~1` Enter", "In a file", "Your file on the left, that version on the right", "Diff against any commit or branch: `HEAD~1`, `main`...",
       ["winnr('$') == 2", "bufname(winbufnr(2)) =~# 'fugitive://'"], setup=["edit app.py"], feed=":Gdiffsplit HEAD~1<CR>", requires=G),
    UI("`]c` / `[c` in a diff", "In either side of a diff", "Jumps to the next / previous difference", "Same keys as for change markers.",
       ["line('.') == 5"], setup=SAVED_CHANGE + ["Gdiffsplit", "wincmd l", "1"], feed="]c", requires=G),
    UI("`do` / `dp`", "On a difference, in your file (the right side)", "**d**iff **o**btain: take the other side's text here / **d**iff **p**ut: send yours across",
       "Copy one difference between the sides.",
       ["getline(5) ==# 'def greet(name):'"], setup=SAVED_CHANGE + ["Gdiffsplit", "wincmd l", "5"], feed="do", requires=G),
    UI("`:diffoff` Enter", "In a diff", "The diff highlighting stops", "Turn it off (`:only` also closes the other side).",
       ["!&diff"], setup=SAVED_CHANGE + ["Gdiffsplit"], feed=":diffoff<CR>", requires=G),
    UI("`:Git diff` Enter", "Anywhere", "The full diff of all your unstaged changes", "`:Git diff --staged` shows what you're about to commit.",
       ["index(WinFts(), 'git') >= 0"], setup=SAVED_CHANGE, feed=":Git diff<CR>", wait=800, requires=G),
    UI("`:Git difftool -y main` Enter", "On a branch", "One tab page per changed file, each as a side-by-side diff", "Review a whole branch before a pull request.",
       ["tabpagenr('$') >= 2"], setup=["call system('git checkout -q feature')", "edit notes.txt"], feed=":Git difftool -y main<CR>", wait=800, requires=G),
]),

section("Who wrote this", "", [
    UI("`Space gb`", "In a file", "A column beside the file with the commit, author and date of every line", "Blame. `q` closes it.",
       ["index(WinFts(), 'fugitiveblame') >= 0"], setup=["edit app.py"], feed="<Space>gb", wait=500, requires=G),
    UI("`Enter` in blame", "On a line in the blame column", "Opens the commit that last changed that line", "See why a line changed.",
       ["&filetype ==# 'git'", "search('Explain add', 'nw') > 0"], setup=["edit app.py", "Git blame", "2"], feed="<CR>", wait=500, requires=G),
    UI("`g?` in blame", "In the blame column", "The list of blame keys", "Help.",
       ["&filetype ==# 'help'"], setup=["edit app.py", "Git blame"], feed="g?", requires=G),
    UI("`:Git shortlog -sn HEAD -- %` Enter", "In a file", "Everyone who has changed this file, most commits first", "Find who knows a file best. `%` is the current file.",
       ["search('Test User', 'nw') > 0"], setup=["edit app.py"], feed=":Git shortlog -sn HEAD -- %<CR>", wait=800, requires=G),
    UI("`:Git log -L 2,2:%` Enter", "In a file", "Every commit that changed line 2, with its diff", "The history of specific lines. Use your own line numbers.",
       ["search('Explain add', 'nw') > 0"], setup=["edit app.py"], feed=":Git log -L 2,2:%<CR>", wait=800, requires=G),
    UI("`:e .github/CODEOWNERS` Enter", "In a repo that has one", "The file that says who owns which paths", "`/` then a path to find its owners.",
       ["expand('%:t') ==# 'CODEOWNERS'", "getline(2) =~# '@python-team'"], feed=":e .github/CODEOWNERS<CR>"),
]),

section("History", "", [
    UI("`Space gl`", "In a file", "Every version of this file goes into the quickfix list", "File history; `:cnext` / `:cprev` step through the versions.",
       ["QfLen() == 2"], setup=["edit app.py"], feed="<Space>gl", wait=800, requires=G),
    UI("`:Gclog` Enter", "Anywhere", "The project's commits in the quickfix list", "Project history.",
       ["QfLen() >= 2"], feed=":Gclog<CR>", wait=800, requires=G),
    UI("`:Git log --oneline --graph` Enter", "Anywhere", "A compact log with the branch graph", "Overview of history.",
       ["search('Explain add', 'nw') > 0"], feed=":Git log --oneline --graph<CR>", wait=800, requires=G),
    UI("`:Gedit main:%` Enter", "In a file", "This file as it is on `main` (read-only)", "Look at another branch's version.",
       ["bufname('%') =~# 'fugitive://'", "getline(2) =~# '# sum'"], setup=["call system('git checkout -q feature')", "edit app.py"], feed=":Gedit main:%<CR>", requires=G),
]),

section("Status, staging and commits", """\
`Space gs` opens Git status. In it, put the cursor on a file and use the keys
below. `g?` lists them all.""", [
    UI("`Space gs`", "Anywhere in a repo", "The Git status window", "Staged, unstaged and untracked files.",
       ["&filetype ==# 'fugitive'"], setup=SAVED_CHANGE, feed="<Space>gs", requires=G),
    UI("`s`", "On a file in status", "The file is staged", "Stage.",
       ["Sh('git diff --cached --name-only') ==# 'app.py'"], setup=SAVED_CHANGE + ["Git", "call search('app.py')"], feed="s", wait=300, requires=G),
    UI("`u`", "On a staged file", "Unstaged", "Unstage.",
       ["Sh('git diff --cached --name-only') ==# ''"], setup=SAVED_CHANGE + ["call system('git add app.py')", "Git", "call search('app.py')"], feed="u", wait=300, requires=G),
    UI("`=`", "On a file in status", "Its diff opens inline, under the file name", "Peek at the change; `=` again folds it.",
       ["search('^+def greet(person)', 'nw') > 0"], setup=SAVED_CHANGE + ["Git", "call search('app.py')"], feed="=", requires=G),
    UI("`dv`", "On a file in status", "A side-by-side diff of that file", "Full diff view.",
       ["len(filter(range(1, winnr('$')), 'getwinvar(v:val, \"&diff\")')) == 2"], setup=SAVED_CHANGE + ["Git", "call search('app.py')"], feed="dv", wait=500, requires=G),
    UI("`X`", "On a changed file in status", "Its changes are thrown away", "Discard (fugitive tells you how to undo it).",
       ["Disk('app.py') !~# 'person'"], setup=SAVED_CHANGE + ["Git", "call search('app.py')"], feed="X", wait=300, requires=G),
    UI("`cc`, message, `:wq`", "In status, after staging", "A commit-message window; saving it makes the commit", "Commit. `ca` amends the last commit, `ce` amends without changing its message.",
       ["Child(['app.py'], [[':Git<CR>', 1500], ['cc', 2500], 'iRename the greet argument<Esc>', [':wq<CR>', 2500], ':qa!<CR>'], 4000).status ==# 'dead'",
        "Sh('git log -1 --format=%s') ==# 'Rename the greet argument'"],
       setup=SAVED_CHANGE + ["call system('git add app.py')"], requires=G),
    UI("`czz` / `czp`", "In status", "Your changes are stashed away / brought back", "Stash and pop.",
       ["Sh('git stash list') =~# 'stash@{0}'", "Disk('app.py') !~# 'person'"], setup=SAVED_CHANGE + ["Git"], feed="czz", wait=500, requires=G),
    UI("`:Gwrite` Enter", "In a file", "Saves and stages the file", "Stage the whole file.",
       ["Sh('git diff --cached --name-only') ==# 'app.py'"], setup=["edit app.py", "call setline(5, 'def greet(person):')"], feed=":Gwrite<CR>", wait=300, requires=G),
    UI("`:Gread` Enter", "In a changed file", "The file goes back to the last commit (undo with `u`)", "Revert the file in the editor.",
       ["getline(5) ==# 'def greet(name):'"], setup=["edit app.py", "call setline(5, 'def greet(person):')"], feed=":Gread<CR>", wait=300, requires=G),
    UI("`:Git push` Enter", "After committing", "Your commits go to the remote", "`:Git pull` brings others' commits in.",
       ["Sh('git ls-remote origin main') =~# Sh('git rev-parse HEAD')"],
       setup=["call system('git commit -q --allow-empty -m pushed')"], feed=":Git push<CR>", wait=1500, requires=G),
    UI("`:Git pull` Enter", "When the remote has new commits", "They're merged into your branch", "Update from the remote.",
       ["Sh('git log -1 --format=%s') ==# 'from-elsewhere'"],
       setup=["call system('cd .. && rm -rf other && git clone -q ' . shellescape(Sh('git remote get-url origin')) . ' other && cd other && git -c user.name=T -c user.email=t@example.com commit -q --allow-empty -m from-elsewhere && git push -q origin main && cd .. && rm -rf other')"],
       feed=":Git pull<CR>", wait=1500, requires=G),
    UI("`:Git switch -c new-branch` Enter", "Anywhere", "A new branch, checked out", "Any `git` command works after `:Git`.",
       ["Sh('git branch --show-current') ==# 'new-branch'"], feed=":Git switch -c new-branch<CR>", wait=300, requires=G),
    UI("`:GMove newname.txt` Enter", "In a tracked file", "Renamed on disk and in Git; the buffer follows", "Rename. `:GDelete` deletes the file the same way.",
       ["expand('%:t') ==# 'newname.txt'", "Sh('git status --short') =~# 'R'"], setup=["edit notes.txt"], feed=":GMove newname.txt<CR>", wait=300, requires=G),
]),

section("Merge conflicts", """\
After a merge stops with conflicts, open the conflicted file and use a
three-way diff: your version on the left, the result in the middle, theirs on
the right.""", [
    UI("`:Gvdiffsplit!` Enter", "In a file with conflicts", "Three columns: yours, the result, theirs", "Three-way merge view.",
       ["winnr('$') == 3"], setup=CONFLICT, feed=":Gvdiffsplit!<CR>", wait=500, requires=G),
    UI("`:diffget //2` Enter", "In the middle column, on a conflict", "Takes **your** side (left) for that conflict", "`:diffget //3` takes **theirs** (right).",
       ["getline(2) ==# 'BETA from main'", "search('<<<<<<<', 'nw') == 0"], setup=CONFLICT + ["Gvdiffsplit!", "wincmd t", "wincmd l", "2"],
       feed=":diffget //2<CR>", wait=300, requires=G),
    UI("`:Gwrite` Enter", "In the middle column, when done", "Saves the result and marks the conflict resolved", "Then commit as usual.",
       ["Sh('git diff --name-only --diff-filter=U') ==# ''"], setup=CONFLICT + ["Gvdiffsplit!", "wincmd t", "wincmd l", "2", "diffget //3"],
       feed=":Gwrite<CR>", wait=500, requires=G),
]),

section("Interactive rebase", "`git rebase -i` opens its list of commits in Vim. Edit the words, save with `:x`, or cancel with `:cq`.", [
    E("`ciw` `s` `Esc`", "On `pick`", "▌pick 1a2b3c4 First\npick 5d6e7f8 Second", "▌s 1a2b3c4 First\npick 5d6e7f8 Second", "Change `pick` to `s` (squash into the commit above).",
      file="git-rebase-todo", feed="ciws<Esc>"),
    E("`j` `.`", "After changing one line", "▌pick 1a2b3c4 First\npick 5d6e7f8 Second", "s 1a2b3c4 First\n▌s 5d6e7f8 Second", "Repeat the same change on the next line.",
      file="git-rebase-todo", feed="ciws<Esc>j."),
    E("`:Squash` Enter", "On a line", "▌pick 1a2b3c4 First\npick 5d6e7f8 Second", "▌squash 1a2b3c4 First\npick 5d6e7f8 Second", "Built-in commands: `:Squash`, `:Fixup`, `:Reword`, `:Edit`, `:Drop`, `:Pick`.",
      file="git-rebase-todo", feed=":Squash<CR>", check_cursor=False),
    E("`dd` / `ddp`", "On a line", "▌pick 1a2b3c4 First\npick 5d6e7f8 Second", "pick 5d6e7f8 Second\n▌pick 1a2b3c4 First", "Drop a commit / move it down (`ddkP` moves it up).",
      file="git-rebase-todo", feed="ddp"),
]),
])
