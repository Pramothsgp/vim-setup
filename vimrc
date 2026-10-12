" ============================================================
"  vim-setup — terminal Vim that works like VS Code (macOS + Linux)
"  Installed by install.sh, which links this file to ~/.vimrc.
"  The parts you chose during install are listed in ~/.vim-setup.conf;
"  rerun install.sh to change them.
"  Open a project like VS Code:   vim ~/projects/my-project
"  Machine-specific tweaks go in ~/.vimrc.local (loaded last).
" ============================================================

set nocompatible
set encoding=utf-8           " even on servers without a UTF-8 locale

" All autocommands live in this group; clearing it first makes it safe to
" reload the config with :source ~/.vimrc
augroup vimsetup
  autocmd!
augroup END

" ---------- Which parts are switched on ----------
" Everything is on unless ~/.vim-setup.conf says otherwise.
let g:vs = {'ui': 1, 'explorer': 1, 'finder': 1, 'editing': 1, 'git': 1,
      \ 'lsp': 1, 'copilot': 1, 'copilot_chat': 1, 'claude': 1, 'copilot_cli': 1}
if filereadable(expand('~/.vim-setup.conf'))
  for s:line in readfile(expand('~/.vim-setup.conf'))
    let s:m = matchlist(s:line, '^\s*VIM_SETUP_\(\w\+\)\s*=\s*["'']\?\([01]\)')
    if !empty(s:m) | let g:vs[tolower(s:m[1])] = str2nr(s:m[2]) | endif
  endfor
endif
function! VS(part) abort
  return get(g:vs, a:part, 0)
endfunction

" ---------- Finding programs wherever they were installed ----------
" claude, copilot and node can live in many places: Homebrew, the native
" installers, npm under nvm/fnm/volta/asdf/mise, pnpm, bun, or only as a
" shell alias. Order: your override (g:vim_setup_<name>_path in
" ~/.vimrc.local), PATH, known folders, then ask your login shell.
let s:tool_cache_file = expand('~/.vim/.tool-paths')
let s:tool_cache = {}
if filereadable(s:tool_cache_file)
  for s:line in readfile(s:tool_cache_file)
    let s:kv = split(s:line, '=', 1)
    if len(s:kv) >= 2 | let s:tool_cache[s:kv[0]] = join(s:kv[1:], '=') | endif
  endfor
endif

function! s:VersionCmp(a, b) abort
  let a = map(split(matchstr(a:a, '\d\+\(\.\d\+\)*'), '\.'), 'str2nr(v:val)')
  let b = map(split(matchstr(a:b, '\d\+\(\.\d\+\)*'), '\.'), 'str2nr(v:val)')
  for i in range(max([len(a), len(b)]))
    let x = get(a, i, 0) | let y = get(b, i, 0)
    if x != y | return x > y ? -1 : 1 | endif
  endfor
  return 0
endfunction

function! s:ToolCandidates(name) abort
  let h = expand('~')
  let dirs = [h . '/.local/bin', h . '/bin', '/opt/homebrew/bin', '/usr/local/bin',
        \ '/home/linuxbrew/.linuxbrew/bin', h . '/.linuxbrew/bin', '/usr/bin', '/snap/bin',
        \ h . '/.npm-global/bin', h . '/.npm/bin', h . '/.volta/bin', h . '/.bun/bin',
        \ h . '/.yarn/bin', h . '/.config/yarn/global/node_modules/.bin',
        \ h . '/Library/pnpm', h . '/.local/share/pnpm', h . '/.asdf/shims',
        \ h . '/.local/share/mise/shims', h . '/.nodenv/shims', h . '/n/bin']
  let paths = map(dirs, 'v:val . "/" . a:name')
  if a:name ==# 'claude'
    call extend(paths, [h . '/.claude/local/claude', h . '/.claude/local/node_modules/.bin/claude'])
  endif
  " Node version managers keep a bin folder per Node version: newest first
  for pat in [h . '/.nvm/versions/node/*/bin/',
        \ h . '/.local/share/fnm/node-versions/*/installation/bin/',
        \ h . '/Library/Application Support/fnm/node-versions/*/installation/bin/',
        \ h . '/.fnm/node-versions/*/installation/bin/',
        \ h . '/.asdf/installs/nodejs/*/bin/', h . '/.local/share/mise/installs/node/*/bin/',
        \ h . '/.volta/tools/image/node/*/bin/']
    call extend(paths, sort(glob(pat . a:name, 1, 1), function('s:VersionCmp')))
  endfor
  return paths
endfunction

" Ask the user's own shell (zsh, bash, fish, nu, ...) where the command is.
" Catches aliases and PATH changes made in .zshrc/.bashrc/config.fish.
function! s:AskShell(name) abort
  let sh = empty($SHELL) ? '/bin/sh' : $SHELL
  let shname = fnamemodify(sh, ':t')
  if shname =~# '^fish'
    let cmd = [sh, '-l', '-i', '-c', 'command -v ' . a:name . '; or functions ' . a:name]
  elseif shname =~# '^nu'
    let cmd = [sh, '-l', '-c', 'which ' . a:name . ' | to text']
  elseif shname ==# 'bash'
    " login bash skips ~/.bashrc, where aliases usually live
    let cmd = [sh, '-l', '-i', '-c', '[ -f ~/.bashrc ] && . ~/.bashrc >/dev/null 2>&1; alias ' . a:name . ' 2>/dev/null; command -v ' . a:name]
  elseif shname =~# '\v^(zsh|ksh|mksh|yash)$'
    let cmd = [sh, '-l', '-i', '-c', 'alias ' . a:name . ' 2>/dev/null; command -v ' . a:name]
  else
    let cmd = [sh, '-l', '-c', 'command -v ' . a:name]
  endif
  let out = tempname()
  try
    let job = job_start(cmd, {'in_io': 'null', 'err_io': 'null', 'out_io': 'file',
          \ 'out_name': out, 'env': {'TERM': 'dumb', 'POWERLEVEL9K_INSTANT_PROMPT': 'off'}})
  catch
    return ''
  endtry
  let waited = 0
  while job_status(job) ==# 'run' && waited < 5000
    sleep 50m
    let waited += 50
  endwhile
  if job_status(job) ==# 'run' | call job_stop(job, 'kill') | endif
  let text = filereadable(out) ? join(readfile(out), "\n") : ''
  call delete(out)
  " Any path ending in /<name> (from `command -v`, an alias, or a fish function)
  let text = substitute(text, '\e\[[0-9;?]*[A-Za-z]', '', 'g')
  for tok in split(text, '[[:space:]''"=;]\+')
    let p = expand(tok)
    if p =~# '/' . a:name . '$' && executable(p) | return p | endif
  endfor
  return ''
endfunction

" FindTool(name)         full search, may ask the shell (used when you press a key)
" FindTool(name, 1)      quick search only (used at startup)
function! FindTool(name, ...) abort
  let quick = a:0 && a:1
  let override = expand(get(g:, 'vim_setup_' . a:name . '_path', ''))
  if !empty(override) && executable(override) | return override | endif
  let p = exepath(a:name)
  if !empty(p) | return p | endif
  if has_key(s:tool_cache, a:name) && executable(s:tool_cache[a:name])
    return s:tool_cache[a:name]
  endif
  for p in s:ToolCandidates(a:name)
    if executable(p) | return s:RememberTool(a:name, p) | endif
  endfor
  if !quick
    let p = s:AskShell(a:name)
    if !empty(p) | return s:RememberTool(a:name, p) | endif
  endif
  return ''
endfunction

function! s:RememberTool(name, path) abort
  let s:tool_cache[a:name] = a:path
  silent! call mkdir(fnamemodify(s:tool_cache_file, ':h'), 'p')
  silent! call writefile(map(items(s:tool_cache), 'v:val[0] . "=" . v:val[1]'), s:tool_cache_file)
  return a:path
endfunction

" Copilot needs Node.js, which may only be on PATH inside your shell (nvm etc.)
let s:node = (VS('copilot') || VS('lsp')) ? FindTool('node', 1) : ''
if !empty(s:node) && empty(exepath('node'))
  let g:copilot_node_command = s:node
  let $PATH = fnamemodify(s:node, ':h') . ':' . $PATH   " for language servers too
endif

" ---------- Plugins (only the parts you chose) ----------
let s:want_plugins = VS('ui') || VS('explorer') || VS('finder') || VS('editing')
      \ || VS('git') || VS('lsp') || VS('copilot') || VS('copilot_chat')
let s:have_plug = filereadable(expand('~/.vim/autoload/plug.vim'))
if s:want_plugins && !s:have_plug && executable('curl')
  silent execute '!curl -fsSLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  let s:have_plug = filereadable(expand('~/.vim/autoload/plug.vim'))
endif

if s:want_plugins && s:have_plug
  let g:plug_timeout = 300            " big plugins (Copilot) on slow networks
  call plug#begin('~/.vim/plugged')
  if VS('ui')
    Plug 'morhetz/gruvbox'                    " colour scheme
    Plug 'itchyny/lightline.vim'              " status line
    Plug 'ap/vim-buftabline'                  " open files as tabs along the top
  endif
  if VS('explorer')
    Plug 'preservim/nerdtree'                 " sidebar explorer
    if VS('git')
      Plug 'Xuyuanp/nerdtree-git-plugin'
    endif
  endif
  if VS('finder')
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'                   " fuzzy files / grep / buffers
  endif
  if VS('editing')
    Plug 'tpope/vim-commentary'               " gcc / Ctrl-/ = toggle comment
    Plug 'tpope/vim-surround'                 " cs"' = change surrounding quotes
    Plug 'tpope/vim-repeat'                   " makes . work with the above
    Plug 'jiangmiao/auto-pairs'               " auto-close brackets and quotes
    Plug 'mg979/vim-visual-multi'             " multiple cursors (Ctrl-n = Cmd-D)
    Plug 'moll/vim-bbye'                      " close a file, keep the layout
  endif
  if VS('git')
    Plug 'tpope/vim-fugitive'                 " :Git status/blame/diff
    Plug 'airblade/vim-gitgutter'             " +/-/~ markers in the gutter
  endif
  if VS('lsp')
    Plug 'prabirshrestha/vim-lsp'
    Plug 'mattn/vim-lsp-settings'             " :LspInstallServer per language
    Plug 'prabirshrestha/asyncomplete.vim'
    Plug 'prabirshrestha/asyncomplete-lsp.vim'
  endif
  if VS('copilot') && !empty(s:node)
    Plug 'github/copilot.vim'                 " grey suggestions; :Copilot setup once
  endif
  if VS('copilot_chat') && v:version >= 900
    " Copilot Chat window. Loaded on first use, so it only asks you to sign
    " in when you open the chat, not every time Vim starts.
    Plug 'DanBradbury/copilot-chat.vim', { 'on': ['CopilotChatOpen', 'CopilotChat',
          \ 'CopilotChatFocus', 'CopilotChatToggle', 'CopilotChatModels', 'CopilotChatReset',
          \ 'CopilotChatSave', 'CopilotChatLoad', 'CopilotChatList', 'CopilotChatUsage',
          \ '<Plug>CopilotChatAddSelection'] }
  endif
  call plug#end()

  " Install any plugin that isn't downloaded yet
  autocmd vimsetup VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
        \ | PlugInstall --sync | close | source $MYVIMRC | endif
endif
function! s:Has(plugin) abort
  return exists('g:plugs') && has_key(g:plugs, a:plugin) && isdirectory(g:plugs[a:plugin].dir)
endfunction

syntax on
filetype plugin indent on

" ---------- Look ----------
set number relativenumber
set cursorline
set showcmd
set laststatus=2
set scrolloff=8
set signcolumn=yes
set updatetime=300          " faster git markers and diagnostics
set timeoutlen=500 ttimeoutlen=10

" True colour in terminals that support it (iTerm2, Ghostty, WezTerm, kitty,
" Alacritty, VS Code, tmux). Plain macOS Terminal.app stays on 256 colours.
if $COLORTERM =~# '\v^(truecolor|24bit)$'
      \ || $TERM_PROGRAM =~# '\v^(iTerm\.app|WezTerm|ghostty|vscode|Hyper|Tabby)$'
      \ || $TERM =~# '\v(kitty|alacritty|ghostty|wezterm|foot)'
  if &term =~# '^\(tmux\|screen\)'
    let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
    let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
  endif
  set termguicolors
endif
set background=dark
if s:Has('gruvbox')
  colorscheme gruvbox
else
  silent! colorscheme habamax
endif
if s:Has('lightline.vim')
  set noshowmode
  let g:lightline = { 'colorscheme': s:Has('gruvbox') ? 'gruvbox' : 'default',
        \ 'enable': { 'statusline': 1, 'tabline': 0 } }   " tabs come from buftabline
endif
if s:Has('vim-buftabline')
  set showtabline=2
  let g:buftabline_numbers = 2      " tab numbers for Space 1..9
  let g:buftabline_indicators = 1   " mark unsaved files
endif

" Thin cursor in insert mode, block in normal mode
let &t_SI = "\e[6 q"
let &t_EI = "\e[2 q"

" ---------- Editing ----------
set tabstop=4 shiftwidth=4 softtabstop=4 expandtab
set autoindent smartindent
set backspace=indent,eol,start
set clipboard=unnamed,unnamedplus
set mouse=a
set hidden                  " switch files without saving first
set autoread                " reload files changed outside Vim
set undofile
set undodir=~/.vim/undo//
silent! call mkdir(expand('~/.vim/undo'), 'p')
set noswapfile
set splitright splitbelow   " new splits open right / below
set diffopt+=vertical,algorithm:histogram,indent-heuristic   " diffs side by side, VS Code style
let g:AutoPairsMapCR = 0              " keep Enter for autocomplete
let g:AutoPairsMultilineClose = 0

" 2-space indent for web files
autocmd vimsetup FileType javascript,typescript,typescriptreact,javascriptreact,json,yaml,html,css setlocal ts=2 sw=2 sts=2
" Commit messages: spellcheck and wrap at 72
autocmd vimsetup FileType gitcommit setlocal spell textwidth=72
" Reload files changed on disk (also picks up edits made by Claude or Copilot)
autocmd vimsetup FocusGained,BufEnter,CursorHold * silent! checktime
" While a terminal or AI panel is open, look for changed files every second,
" so edits made by Claude, Copilot or a shell command show up straight away
function! s:CheckForOutsideEdits(timer) abort
  if !empty(term_list()) && mode() =~# '^[nt]' && getcmdwintype() ==# ''
    silent! checktime
  endif
endfunction
if has('terminal') && !exists('s:outside_edits_timer')
  let s:outside_edits_timer = timer_start(1000, function('s:CheckForOutsideEdits'), {'repeat': -1})
endif

" ---------- Search ----------
set incsearch hlsearch
set ignorecase smartcase
set wildmenu
set wildmode=longest:full,full
set path=.,**               " :find searches the whole project
set wildignore+=*/node_modules/*,*/.git/*,*/dist/*,*/build/*,*/__pycache__/*
if executable('rg')
  set grepprg=rg\ --vimgrep\ --smart-case grepformat=%f:%l:%c:%m
  let $FZF_DEFAULT_COMMAND = 'rg --files'   " ripgrep reads .ignore by itself
endif

" ---------- Explorer ----------
let g:NERDTreeHijackNetrw = 0
let g:NERDTreeMinimalUI = 1
let g:NERDTreeWinSize = 32
let g:NERDTreeMouseMode = 3        " single click opens files and folders
let g:NERDTreeShowHidden = 0       " dotfiles hidden; I toggles
let g:gitgutter_map_keys = 0       " set up below without overlapping keys
let g:netrw_banner = 0             " built-in explorer, used when NERDTree is off
let g:netrw_liststyle = 3
let g:netrw_winsize = 25

" `vim some/folder` opens it like VS Code: folder becomes the project,
" explorer on the left, empty editor on the right
function! s:OpenProject() abort
  if argc() != 1 || !isdirectory(argv(0)) | return | endif
  execute 'cd' fnameescape(argv(0))
  if exists(':NERDTree') != 2 | return | endif    " built-in explorer shows the folder
  let dirbuf = bufnr('%')
  enew
  silent! execute 'bwipeout' dirbuf
  NERDTree
  wincmd p
endfunction
autocmd vimsetup VimEnter * nested call s:OpenProject()

" Quit Vim when the explorer is the only window left
autocmd vimsetup BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | call feedkeys(":quit\<CR>:\<BS>") | endif

" ---------- Per-project hidden files ----------
" Each project keeps its own list in <project>/.ignore (one name or glob per
" line, e.g.  node_modules  or  *.log). Listed items disappear from the
" explorer, the file finder and project search.
function! s:IgnoreFile() abort
  return getcwd() . '/.ignore'
endfunction

function! s:HiddenNames() abort
  if !filereadable(s:IgnoreFile()) | return [] | endif
  return filter(map(readfile(s:IgnoreFile()), 'trim(v:val)'),
        \ 'v:val !=# "" && v:val !~# "^#"')
endfunction

function! s:LoadHidden() abort
  let pats = []
  for name in s:HiddenNames()
    let name = substitute(name, '^/\|/$', '', 'g')
    if name ==# '' || name =~# '/' | continue | endif
    call add(pats, glob2regpat(name))
  endfor
  let g:NERDTreeIgnore = pats
  let g:netrw_list_hide = join(map(copy(pats), 'substitute(v:val, ''\$$'', '''', '''') . ''[/*@]\=$'''), ',')
  for win in getwininfo()
    if getbufvar(win.bufnr, '&filetype') ==# 'nerdtree'
      call win_execute(win.winid, 'silent! NERDTreeRefreshRoot')
    endif
  endfor
endfunction

function! s:NameUnderCursor() abort
  if &filetype ==# 'nerdtree'
    let node = g:NERDTreeFileNode.GetSelected()
    return empty(node) ? '' : node.path.getLastPathComponent(0)
  elseif &filetype ==# 'netrw'
    return fnamemodify(substitute(netrw#Call('NetrwGetWord'), '[/*@]$', '', ''), ':t')
  endif
  return expand('%:t')
endfunction

function! s:Hide(...) abort
  let names = a:0 ? copy(a:000) : [s:NameUnderCursor()]
  call filter(names, 'v:val !=# "" && v:val !=# "." && v:val !=# ".."')
  if empty(names) | echo 'Nothing to hide here' | return | endif
  let lines = filereadable(s:IgnoreFile()) ? readfile(s:IgnoreFile()) : []
  call extend(lines, filter(copy(names), 'index(lines, v:val) < 0'))
  call writefile(lines, s:IgnoreFile())
  call s:LoadHidden()
  echo 'Hidden in this project: ' . join(names, ', ')
endfunction

function! s:Unhide(...) abort
  let names = a:0 ? copy(a:000) : [s:NameUnderCursor()]
  if !filereadable(s:IgnoreFile()) | echo 'Nothing is hidden here' | return | endif
  call writefile(filter(readfile(s:IgnoreFile()),
        \ 'index(names, trim(v:val)) < 0'), s:IgnoreFile())
  call s:LoadHidden()
  echo 'Showing again: ' . join(names, ', ')
endfunction

function! s:CompleteHidden(...) abort
  return join(s:HiddenNames(), "\n")
endfunction

command! -nargs=* -complete=file Hide call s:Hide(<f-args>)
command! -nargs=* -complete=custom,s:CompleteHidden Unhide call s:Unhide(<f-args>)

augroup project_hide
  autocmd!
  autocmd VimEnter,DirChanged * call s:LoadHidden()
  autocmd BufWritePost .ignore call s:LoadHidden()
augroup END
call s:LoadHidden()

" Folder for Space f: the folder selected in the explorer, else the
" current file's folder, else the project
function! s:HereDir() abort
  if &filetype ==# 'nerdtree'
    let node = g:NERDTreeFileNode.GetSelected()
    if empty(node) | return b:NERDTree.root.path.str() | endif
    return node.path.isDirectory ? node.path.str() : fnamemodify(node.path.str(), ':h')
  elseif &filetype ==# 'netrw' && exists('b:netrw_curdir')
    return b:netrw_curdir
  endif
  return empty(expand('%')) ? getcwd() : expand('%:p:h')
endfunction

" ---------- Built-in terminal panel (like Ctrl-` in VS Code) ----------
function! s:ToggleTerminal() abort
  let buf = get(g:, 'panel_term', -1)
  let win = bufwinid(buf)
  if win != -1
    execute win_id2win(win) . 'hide'
  elseif bufexists(buf) && term_getstatus(buf) =~# 'running'
    execute 'botright sbuffer' buf
    resize 12
    startinsert
  else
    botright terminal ++rows=12 ++kill=term
    let g:panel_term = bufnr('%')
    setlocal nobuflisted
    " Only in this panel: Esc Esc to scroll/copy, Ctrl-t to hide it
    " (the AI panels keep their own Esc and Ctrl-t)
    tnoremap <buffer> <Esc><Esc> <C-\><C-n>
    tnoremap <buffer> <C-t> <C-\><C-n>:call <SID>ToggleTerminal()<CR>
  endif
endfunction

" ---------- AI agent panels: Claude Code and GitHub Copilot CLI ----------
let s:agents = {
      \ 'claude':  {'title': 'Claude Code', 'part': 'claude',
      \             'install': 'curl -fsSL https://claude.ai/install.sh | bash'},
      \ 'copilot': {'title': 'GitHub Copilot CLI', 'part': 'copilot_cli',
      \             'install': 'brew install --cask copilot-cli   (or: npm install -g @github/copilot)'},
      \ }
let s:panel_buf = {}
let s:last_agent = VS('claude') ? 'claude' : 'copilot'

function! s:PanelWidth() abort
  return max([60, &columns * 2 / 5])
endfunction

function! s:AgentBuf(name) abort
  let buf = get(s:panel_buf, a:name, -1)
  return bufexists(buf) && term_getstatus(buf) =~# 'running' ? buf : -1
endfunction

function! s:OpenAgent(name) abort
  let exe = FindTool(a:name)
  if empty(exe)
    echohl WarningMsg
    echo s:agents[a:name].title . ' was not found. Install it with:  ' . s:agents[a:name].install
          \ . '   (or set g:vim_setup_' . a:name . '_path in ~/.vimrc.local)'
    echohl None
    return 0
  endif
  " Run it with its own folder (and Node's) on PATH, so npm-installed
  " versions work even when Vim was started without your shell's PATH
  let path = fnamemodify(exe, ':h')
  let node = FindTool('node', 1)
  if !empty(node) | let path .= ':' . fnamemodify(node, ':h') | endif
  botright vertical new
  setlocal bufhidden=wipe
  let buf = term_start([exe], {'curwin': 1, 'term_finish': 'close', 'term_kill': 'term',
        \ 'term_name': s:agents[a:name].title, 'norestore': 1,
        \ 'env': {'PATH': path . ':' . $PATH}})
  execute 'vertical resize' s:PanelWidth()
  setlocal nobuflisted
  let s:panel_buf[a:name] = buf
  let s:last_agent = a:name
  return 1
endfunction

function! s:ShowAgent(name) abort
  let buf = s:AgentBuf(a:name)
  let win = bufwinid(buf)
  if win != -1
    call win_gotoid(win)
  else
    execute 'botright vertical sbuffer' buf
    execute 'vertical resize' s:PanelWidth()
  endif
  let s:last_agent = a:name
endfunction

function! s:ToggleAgent(name) abort
  let buf = s:AgentBuf(a:name)
  if buf == -1
    call s:OpenAgent(a:name)
  elseif bufwinid(buf) != -1
    execute win_id2win(bufwinid(buf)) . 'hide'
  else
    call s:ShowAgent(a:name)
  endif
endfunction

" Type a reference to this file (and the selected lines) into the prompt of
" the AI panel you used last, so you only have to add the question
function! s:SendToAgent(line1, line2) abort
  if &buftype !=# '' || empty(expand('%'))
    echo 'Open a file first' | return
  endif
  let ref = '@' . expand('%:.') . ' '
  if a:line1 > 0
    let ref .= (a:line1 == a:line2 ? 'line ' . a:line1 : 'lines ' . a:line1 . '-' . a:line2) . ' '
  endif
  let name = s:last_agent
  let buf = s:AgentBuf(name)
  if buf == -1
    if !s:OpenAgent(name) | return | endif
    let buf = s:panel_buf[name]
    call timer_start(2000, {-> term_sendkeys(buf, ref)})   " let it start first
  else
    call s:ShowAgent(name)
    call term_sendkeys(buf, ref)
  endif
endfunction

" ---------- GitHub Copilot (inline suggestions) ----------
let g:copilot_no_tab_map = v:true     " Tab is shared with autocomplete below
function! s:ToggleCopilot() abort
  if !exists('g:loaded_copilot')
    echo 'Copilot suggestions are not installed (they need Node.js)' | return
  endif
  if copilot#Enabled()
    Copilot disable
    echo 'Copilot suggestions off'
  else
    Copilot enable
    echo 'Copilot suggestions on'
  endif
endfunction

" ---------- Keymaps ----------
let mapleader = " "
inoremap jk <Esc>

" Run a command in the editor window, never inside the explorer sidebar,
" so files always open on the right like VS Code
function! s:InEditor(cmd) abort
  if &filetype =~# '^\(nerdtree\|netrw\)$' && winnr('$') > 1 | wincmd p | endif
  if &filetype ==# 'nerdtree' | botright vnew | endif
  execute a:cmd
endfunction

" Leader key layout (Space). No key here is the start of a longer one, so
" every shortcut fires at once instead of making Vim wait:
"   single keys   w q c h e E x X p f s b / r t 1-9 Tab \
"   ]b / [b       next / previous file tab
"   Space g...    Git           Space l...    language / code
"   Space a...    AI

" Save / close
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>
nnoremap <leader>w :w<CR>
nnoremap <leader>q :q<CR>
nnoremap <leader>h :nohlsearch<CR>
if s:Has('vim-bbye')
  nnoremap <leader>c :Bdelete<CR>
else
  nnoremap <leader>c :bprevious <Bar> bdelete #<CR>
endif

" Explorer
if s:Has('nerdtree')
  nnoremap <leader>e :NERDTreeToggle<CR>
  nnoremap <leader>E :NERDTreeFind<CR>
else
  nnoremap <leader>e :Lexplore<CR>
  nnoremap <leader>E :Lexplore %:p:h<CR>
endif
nnoremap <leader>x :Hide<CR>
nnoremap <leader>X :execute 'split' fnameescape(<SID>IgnoreFile())<CR>

" Find files and text (Cmd-P, Cmd-Shift-F)
if s:Has('fzf.vim')
  nnoremap <C-p> :call <SID>InEditor('Files')<CR>
  nnoremap <leader>p :call <SID>InEditor('Files')<CR>
  nnoremap <leader>f :call <SID>InEditor('Files ' . fnameescape(<SID>HereDir()))<CR>
  nnoremap <leader>s :call <SID>InEditor('Rg')<CR>
  nnoremap <leader>b :call <SID>InEditor('Buffers')<CR>
  nnoremap <leader>/ :BLines<CR>
  nnoremap <leader>r :call <SID>InEditor('History')<CR>
else
  " Built-in fallbacks: :find with Tab completion, :grep, :ls
  nnoremap <C-p> :find<Space>
  nnoremap <leader>p :find<Space>
  nnoremap <leader>f :find <C-r>=fnameescape(fnamemodify(<SID>HereDir(), ':.'))<CR>/
  nnoremap <leader>s :grep!<Space>
  nnoremap <leader>b :ls<CR>:buffer<Space>
  nnoremap <leader>/ /
  nnoremap <leader>r :browse oldfiles<CR>
  autocmd vimsetup QuickFixCmdPost grep cwindow
endif

" Switch between open files: ]b / [b (Shift-h / Shift-l are left alone:
" they're Vim's H and L, jump to the top / bottom of the screen)
nnoremap ]b :call <SID>InEditor('bnext')<CR>
nnoremap [b :call <SID>InEditor('bprevious')<CR>
nnoremap <leader><Tab> :call <SID>InEditor('buffer #')<CR>
function! s:GoToTab(n) abort
  let bufs = s:Has('vim-buftabline') ? buftabline#user_buffers()
        \ : map(filter(getbufinfo({'buflisted': 1}), 'v:val.name !=# ""'), 'v:val.bufnr')
  if a:n <= len(bufs) | call s:InEditor('buffer ' . bufs[a:n - 1]) | endif
endfunction
for s:i in range(1, 9)
  execute 'nnoremap <leader>' . s:i . ' :call <SID>GoToTab(' . s:i . ')<CR>'
endfor

" Comment toggle with Ctrl-/ (most terminals send it as Ctrl-_, some as Ctrl-/)
" (in Insert mode the cursor stays where you were typing)
function! s:CommentWhileTyping() abort
  let [len0, col0] = [strlen(getline('.')), col('.')]
  execute "normal \<Plug>CommentaryLine"
  call cursor(line('.'), max([1, col0 + strlen(getline('.')) - len0]))
endfunction
if s:Has('vim-commentary')
  for s:k in ['<C-_>', '<C-/>']
    execute 'nmap' s:k 'gcc'
    execute 'xmap' s:k 'gc'
    execute 'inoremap <silent>' s:k '<Cmd>call <SID>CommentWhileTyping()<CR>'
  endfor
endif

" Terminal panel (Ctrl-t inside the panel is set up where the panel opens,
" so it never steals Ctrl-t from Claude or Copilot)
nnoremap <C-t> :call <SID>ToggleTerminal()<CR>
nnoremap <leader>t :call <SID>ToggleTerminal()<CR>

" AI: Space a...
if VS('claude')
  nnoremap <leader>aa :call <SID>ToggleAgent('claude')<CR>
endif
if VS('copilot_cli')
  nnoremap <leader>ag :call <SID>ToggleAgent('copilot')<CR>
endif
if VS('claude') || VS('copilot_cli')
  nnoremap <leader>af :call <SID>SendToAgent(0, 0)<CR>
  xnoremap <leader>af :<C-u>call <SID>SendToAgent(line("'<"), line("'>"))<CR>
endif
if s:Has('copilot.vim')
  nnoremap <leader>ac :call <SID>ToggleCopilot()<CR>
  nnoremap <leader>ap :Copilot panel<CR>
  " Alternatives to Copilot's Alt keys, which macOS terminals don't send by default
  imap <C-j> <Plug>(copilot-next)
  imap <C-k> <Plug>(copilot-previous)
  imap <C-l> <Plug>(copilot-accept-word)
endif
" Copilot Chat with a selection: open the chat first, then add the selection
" (the plugin's own way of creating the chat from a selection fails in Vim 9)
function! s:ChatWithSelection() abort
  let here = win_getid()
  if empty(filter(range(1, winnr('$')), {_, w -> getbufvar(winbufnr(w), '&filetype') ==# 'copilot_chat'}))
    CopilotChatOpen
    call win_gotoid(here)
  endif
  call copilot_chat#buffer#AddSelection()
endfunction
if s:Has('copilot-chat.vim')
  nnoremap <leader>ai :CopilotChatOpen<CR>
  xnoremap <silent> <leader>ai :<C-u>call <SID>ChatWithSelection()<CR>
  nnoremap <leader>am :CopilotChatModels<CR>
  " In the chat, Enter sends while typing (like VS Code); Ctrl-j adds a new line
  autocmd vimsetup FileType copilot_chat
        \ inoremap <buffer><expr> <CR> pumvisible() ? "\<C-y>" : "\<Esc>\<Cmd>CopilotChatSubmit\<CR>"
        \ | inoremap <buffer> <C-j> <CR>
endif

" Git: Space g...
if s:Has('vim-fugitive')
  nnoremap <leader>gs :Git<CR>
  nnoremap <leader>gb :Git blame<CR>
  nnoremap <leader>gd :Gdiffsplit<CR>
  nnoremap <leader>gl :0Gclog<CR>
endif
if s:Has('vim-gitgutter')
  nnoremap <leader>gp :GitGutterPreviewHunk<CR>
  nnoremap <leader>ga :GitGutterStageHunk<CR>
  nnoremap <leader>gu :GitGutterUndoHunk<CR>
  " ]c / [c jump between changes (and keep working inside a diff)
  nmap <expr> ]c &diff ? ']c' : '<Plug>(GitGutterNextHunk)'
  nmap <expr> [c &diff ? '[c' : '<Plug>(GitGutterPrevHunk)'
  omap ic <Plug>(GitGutterTextObjectInnerPending)
  omap ac <Plug>(GitGutterTextObjectOuterPending)
  xmap ic <Plug>(GitGutterTextObjectInnerVisual)
  xmap ac <Plug>(GitGutterTextObjectOuterVisual)
endif

" Splits
nnoremap <leader>\ :vsplit<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Move selected lines up/down, keep selection when indenting
xnoremap J :m '>+1<CR>gv=gv
xnoremap K :m '<-2<CR>gv=gv
xnoremap < <gv
xnoremap > >gv

" ---------- Code navigation (LSP): Space l... ----------
" Only keys Vim doesn't already use are taken over (gd, gr, K, F2, F12),
" so built-ins like gi, gt and gp keep working.
function! s:on_lsp_buffer_enabled() abort
  setlocal omnifunc=lsp#complete
  if exists('*asyncomplete#enable_for_buffer') | call asyncomplete#enable_for_buffer() | endif
  nmap <buffer> gd <plug>(lsp-definition)
  nmap <buffer> gr <plug>(lsp-references)
  nmap <buffer> K  <plug>(lsp-hover)
  nmap <buffer> <F12>   <plug>(lsp-definition)
  nmap <buffer> <S-F12> <plug>(lsp-references)
  nmap <buffer> <F2>    <plug>(lsp-rename)
  nmap <buffer> <C-LeftMouse> <LeftMouse><plug>(lsp-definition)
  nmap <buffer> [g <plug>(lsp-previous-diagnostic)
  nmap <buffer> ]g <plug>(lsp-next-diagnostic)
  nmap <buffer> <leader>lp <plug>(lsp-peek-definition)
  nmap <buffer> <leader>li <plug>(lsp-implementation)
  nmap <buffer> <leader>lt <plug>(lsp-type-definition)
  nmap <buffer> <leader>lr <plug>(lsp-rename)
  nmap <buffer> <leader>la <plug>(lsp-code-action)
  nmap <buffer> <leader>lf <plug>(lsp-document-format)
  nmap <buffer> <leader>lo :LspDocumentSymbolSearch<CR>
  nmap <buffer> <leader>ls :LspWorkspaceSymbolSearch<CR>
  nmap <buffer> <leader>ld :LspDocumentDiagnostics<CR>
endfunction
augroup lsp_install
  autocmd!
  autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END
let g:lsp_diagnostics_virtual_text_enabled = 1
" TypeScript/JavaScript: use typescript-language-server. Left to itself the
" plugin prefers a global `tsc` if one is installed, which usually can't act
" as a language server, so go-to-definition silently does nothing.
for s:ft in ['typescript', 'typescriptreact', 'javascript', 'javascriptreact']
  let g:lsp_settings_filetype_{s:ft} = 'typescript-language-server'
endfor

" Suggestions pop up as you type only in files with a language server, so
" Vim's own Ctrl-n / Ctrl-p word completion works normally everywhere else.
" While Ctrl-n / Ctrl-p completion is open, the automatic menu waits.
let g:asyncomplete_enable_for_all = 0
function! s:BuiltinComplete(key) abort
  if !pumvisible() && get(b:, 'asyncomplete_enable', 0)
    let b:asyncomplete_enable = 0
    let b:vs_resume_asyncomplete = 1
  endif
  return a:key
endfunction
if s:Has('asyncomplete.vim')
  inoremap <expr> <C-n> <SID>BuiltinComplete("\<C-n>")
  inoremap <expr> <C-p> <SID>BuiltinComplete("\<C-p>")
  autocmd vimsetup CompleteDone,InsertLeave * if get(b:, 'vs_resume_asyncomplete', 0)
        \ | let b:asyncomplete_enable = 1 | unlet b:vs_resume_asyncomplete | endif
endif

" Tab: move through the autocomplete menu when it's open, otherwise accept
" Copilot's grey suggestion, otherwise insert a normal Tab.
" Shift-Tab moves back through the menu, Enter accepts from the menu.
imap <silent><script><expr> <Tab> pumvisible() ? "\<C-n>"
      \ : exists('g:loaded_copilot') ? copilot#Accept("\<Tab>") : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <CR>    pumvisible() ? "\<C-y>" : "\<CR>"

" ---------- Machine-specific overrides ----------
if filereadable(expand('~/.vimrc.local'))
  source ~/.vimrc.local
endif
