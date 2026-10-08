" ============================================================
"  vim-setup — terminal Vim that works like VS Code (macOS + Linux)
"  Installed by install.sh, which links this file to ~/.vimrc.
"  Plugins install automatically the first time you open vim.
"  Open a project like VS Code:   vim ~/projects/my-project
"  Machine-specific tweaks go in ~/.vimrc.local (loaded last).
" ============================================================

set nocompatible

" ---------- Auto-install vim-plug ----------
let data_dir = '~/.vim'
if empty(glob(data_dir . '/autoload/plug.vim'))
  silent execute '!curl -fLo ' . data_dir . '/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC
endif

" ---------- Plugins ----------
let g:plug_timeout = 300            " big plugins (Copilot) on slow networks
call plug#begin('~/.vim/plugged')
  " Look
  Plug 'morhetz/gruvbox'                    " colour scheme
  Plug 'itchyny/lightline.vim'              " status line
  Plug 'ap/vim-buftabline'                  " open files as tabs along the top

  " Sidebar explorer
  Plug 'preservim/nerdtree'
  Plug 'Xuyuanp/nerdtree-git-plugin'        " git status markers in the tree

  " Finding things
  Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
  Plug 'junegunn/fzf.vim'                   " fuzzy files / grep / buffers

  " Editing
  Plug 'tpope/vim-commentary'               " gcc / Ctrl-/ = toggle comment
  Plug 'tpope/vim-surround'                 " cs"' = change surrounding quotes
  Plug 'tpope/vim-repeat'                   " makes . work with the above
  Plug 'jiangmiao/auto-pairs'               " auto-close brackets and quotes
  Plug 'mg979/vim-visual-multi'             " multiple cursors (Ctrl-n = Cmd-D)
  Plug 'moll/vim-bbye'                      " close a file, keep the layout

  " Git
  Plug 'tpope/vim-fugitive'                 " :Git status/blame/diff
  Plug 'airblade/vim-gitgutter'             " +/-/~ markers in the gutter

  " Language support: autocomplete, go-to-definition, errors
  Plug 'prabirshrestha/vim-lsp'
  Plug 'mattn/vim-lsp-settings'             " :LspInstallServer per language
  Plug 'prabirshrestha/asyncomplete.vim'
  Plug 'prabirshrestha/asyncomplete-lsp.vim'

  " AI: GitHub Copilot inline suggestions (needs Node.js; run :Copilot setup once)
  if executable('node')
    Plug 'github/copilot.vim'
  endif
call plug#end()

" Install any plugin added to the list above that isn't downloaded yet
autocmd VimEnter * if len(filter(values(g:plugs), '!isdirectory(v:val.dir)'))
      \ | PlugInstall --sync | close | source $MYVIMRC | endif

syntax on
filetype plugin indent on

" ---------- Look ----------
set number relativenumber
set cursorline
set showcmd
set noshowmode              " lightline already shows the mode
set laststatus=2
set showtabline=2           " always show the file tabs
set scrolloff=8
set signcolumn=yes
set updatetime=300          " faster git markers and diagnostics

if $COLORTERM ==# 'truecolor' || $COLORTERM ==# '24bit'
  set termguicolors
endif
set background=dark
try
  colorscheme gruvbox
catch
  colorscheme habamax       " fallback before plugins are installed
endtry
let g:lightline = { 'colorscheme': 'gruvbox',
      \ 'enable': { 'statusline': 1, 'tabline': 0 } }   " tabs come from buftabline
let g:buftabline_numbers = 2      " tab numbers for Space 1..9
let g:buftabline_indicators = 1   " mark unsaved files

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
let g:AutoPairsMapCR = 0              " keep Enter for autocomplete
let g:AutoPairsMultilineClose = 0

" 2-space indent for web files
autocmd FileType javascript,typescript,typescriptreact,javascriptreact,json,yaml,html,css setlocal ts=2 sw=2 sts=2
" Commit messages: spellcheck and wrap at 72
autocmd FileType gitcommit setlocal spell textwidth=72
" (also picks up edits Claude makes to open files)
autocmd FocusGained,BufEnter,CursorHold * silent! checktime

" ---------- Search ----------
set incsearch hlsearch
set ignorecase smartcase
set wildmenu
set wildmode=longest:full,full

" ---------- Sidebar explorer (NERDTree) ----------
let g:NERDTreeHijackNetrw = 0
let g:NERDTreeMinimalUI = 1
let g:NERDTreeWinSize = 32
let g:NERDTreeMouseMode = 3        " single click opens files and folders
let g:NERDTreeShowHidden = 0       " dotfiles hidden; I toggles
let g:NERDTreeQuitOnOpen = 0

" `vim some/folder` opens it like VS Code: folder becomes the project,
" explorer on the left, empty editor on the right
function! s:OpenProject() abort
  if argc() != 1 || !isdirectory(argv(0)) | return | endif
  let dirbuf = bufnr('%')
  execute 'cd' fnameescape(argv(0))
  enew
  silent! execute 'bwipeout' dirbuf
  if exists(':NERDTree') == 2
    NERDTree
    wincmd p
  endif
endfunction
autocmd VimEnter * nested call s:OpenProject()

" Quit Vim when the explorer is the only window left
autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | call feedkeys(":quit\<CR>:\<BS>") | endif

" ---------- Per-project hidden files ----------
" Each project keeps its own list in <project>/.ignore (one name or glob per
" line, e.g.  node_modules  or  *.log). Listed items disappear from the
" explorer, Ctrl-p / Space f and Space g.
"   Space x        hide the file/folder under the cursor (or the current file)
"   Space X        edit this project's list (saving it applies the change)
"   :Hide name     hide by name or glob      :Unhide name   show it again
if executable('rg')
  let $FZF_DEFAULT_COMMAND = 'rg --files'   " ripgrep reads .ignore by itself
endif

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
  " redraw an open explorer so the change shows straight away
  for win in getwininfo()
    if getbufvar(win.bufnr, '&filetype') ==# 'nerdtree'
      call win_execute(win.winid, 'silent! NERDTreeRefreshRoot')
    endif
  endfor
endfunction

function! s:SelectedNode() abort
  if &filetype !=# 'nerdtree' | return {} | endif
  return g:NERDTreeFileNode.GetSelected()
endfunction

function! s:NameUnderCursor() abort
  let node = s:SelectedNode()
  if &filetype ==# 'nerdtree'
    return empty(node) ? '' : node.path.getLastPathComponent(0)
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
    let node = s:SelectedNode()
    if empty(node) | return b:NERDTree.root.path.str() | endif
    return node.path.isDirectory ? node.path.str() : fnamemodify(node.path.str(), ':h')
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
    " Esc Esc leaves typing mode here only (Claude's panel needs its own Esc)
    tnoremap <buffer> <Esc><Esc> <C-\><C-n>
  endif
endfunction

" ---------- Claude Code panel (like the Claude sidebar in VS Code) ----------
function! s:ClaudeWidth() abort
  return max([60, &columns * 2 / 5])
endfunction

function! s:ClaudeBuf() abort
  let buf = get(g:, 'claude_term', -1)
  return bufexists(buf) && term_getstatus(buf) =~# 'running' ? buf : -1
endfunction

function! s:OpenClaude() abort
  if !executable('claude')
    echohl WarningMsg
    echo 'Claude Code is not installed. In a terminal: curl -fsSL https://claude.ai/install.sh | bash'
    echohl None
    return 0
  endif
  execute 'vertical botright terminal ++close ++kill=term ++cols=' . s:ClaudeWidth() . ' claude'
  let g:claude_term = bufnr('%')
  setlocal nobuflisted
  return 1
endfunction

function! s:ShowClaude(buf) abort
  let win = bufwinid(a:buf)
  if win != -1
    call win_gotoid(win)
  else
    execute 'vertical botright sbuffer' a:buf
    execute 'vertical resize' s:ClaudeWidth()
  endif
endfunction

function! s:ToggleClaude() abort
  let buf = s:ClaudeBuf()
  if buf == -1
    call s:OpenClaude()
  elseif bufwinid(buf) != -1
    execute win_id2win(bufwinid(buf)) . 'hide'
  else
    call s:ShowClaude(buf)
  endif
endfunction

" Type a reference to this file (and the selected lines) into Claude's
" prompt, so you only have to add the question
function! s:SendToClaude(line1, line2) abort
  if &buftype !=# '' || empty(expand('%'))
    echo 'Open a file first' | return
  endif
  let ref = '@' . expand('%:.') . ' '
  if a:line1 > 0
    let ref .= (a:line1 == a:line2 ? 'line ' . a:line1 : 'lines ' . a:line1 . '-' . a:line2) . ' '
  endif
  let buf = s:ClaudeBuf()
  if buf == -1
    if !s:OpenClaude() | return | endif
    let buf = g:claude_term
    call timer_start(2000, {-> term_sendkeys(buf, ref)})   " let Claude start first
  else
    call s:ShowClaude(buf)
    call term_sendkeys(buf, ref)
  endif
endfunction

" ---------- GitHub Copilot ----------
let g:copilot_no_tab_map = v:true     " Tab is shared with autocomplete below
function! s:ToggleCopilot() abort
  if !exists('g:loaded_copilot')
    echo 'Copilot is not installed (it needs Node.js)' | return
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

" Save / close
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>
nnoremap <leader>w :w<CR>
nnoremap <leader>c :Bdelete<CR>
nnoremap <leader>q :q<CR>
nnoremap <leader>h :nohlsearch<CR>

" Explorer
nnoremap <leader>e :NERDTreeToggle<CR>
nnoremap <leader>E :NERDTreeFind<CR>
nnoremap <leader>x :Hide<CR>
nnoremap <leader>X :execute 'split' fnameescape(<SID>IgnoreFile())<CR>

" Run a command in the editor window, never inside the explorer sidebar,
" so files always open on the right like VS Code
function! s:InEditor(cmd) abort
  if &filetype ==# 'nerdtree' | wincmd p | endif
  if &filetype ==# 'nerdtree' | botright vnew | endif
  execute a:cmd
endfunction
function! s:GoToTab(n) abort
  let bufs = buftabline#user_buffers()
  if a:n <= len(bufs) | call s:InEditor('buffer ' . bufs[a:n - 1]) | endif
endfunction

" Open files (Cmd-P, Cmd-Shift-F)
nnoremap <C-p> :call <SID>InEditor('Files')<CR>
nnoremap <leader>p :call <SID>InEditor('Files')<CR>
nnoremap <leader>f :call <SID>InEditor('Files ' . fnameescape(<SID>HereDir()))<CR>
nnoremap <leader>g :call <SID>InEditor('Rg')<CR>
nnoremap <leader>b :call <SID>InEditor('Buffers')<CR>
nnoremap <leader>/ :BLines<CR>
nnoremap <leader>r :call <SID>InEditor('History')<CR>

" Switch between open files (tabs along the top)
nnoremap <S-l> :call <SID>InEditor('bnext')<CR>
nnoremap <S-h> :call <SID>InEditor('bprevious')<CR>
nnoremap <leader><Tab> :call <SID>InEditor('buffer #')<CR>
for s:i in range(1, 9)
  execute 'nnoremap <leader>' . s:i . ' :call <SID>GoToTab(' . s:i . ')<CR>'
endfor

" Comment toggle with Ctrl-/ (terminals send it as Ctrl-_)
nmap <C-_> gcc
xmap <C-_> gc
imap <C-_> <Esc>gcca

" Terminal panel
nnoremap <C-t> :call <SID>ToggleTerminal()<CR>
nnoremap <leader>t :call <SID>ToggleTerminal()<CR>
tnoremap <C-t> <C-\><C-n>:call <SID>ToggleTerminal()<CR>

" AI: Claude panel and Copilot
nnoremap <leader>aa :call <SID>ToggleClaude()<CR>
nnoremap <leader>af :call <SID>SendToClaude(0, 0)<CR>
xnoremap <leader>af :<C-u>call <SID>SendToClaude(line("'<"), line("'>"))<CR>
nnoremap <leader>ac :call <SID>ToggleCopilot()<CR>
nnoremap <leader>ap :Copilot panel<CR>
if executable('node')
  " Alternatives to Copilot's Alt keys, which macOS terminals don't send by default
  imap <C-j> <Plug>(copilot-next)
  imap <C-k> <Plug>(copilot-previous)
  imap <C-l> <Plug>(copilot-accept-word)
endif

" Git
nnoremap <leader>gs :Git<CR>
nnoremap <leader>gb :Git blame<CR>
nnoremap <leader>gd :Gdiffsplit<CR>

" Splits
nnoremap <leader>\ :vsplit<CR>
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Move selected lines up/down, keep selection when indenting
vnoremap J :m '>+1<CR>gv=gv
vnoremap K :m '<-2<CR>gv=gv
vnoremap < <gv
vnoremap > >gv

" ---------- Code navigation (LSP) ----------
function! s:on_lsp_buffer_enabled() abort
  setlocal omnifunc=lsp#complete
  nmap <buffer> gd <plug>(lsp-definition)
  nmap <buffer> gp <plug>(lsp-peek-definition)
  nmap <buffer> gr <plug>(lsp-references)
  nmap <buffer> gi <plug>(lsp-implementation)
  nmap <buffer> gt <plug>(lsp-type-definition)
  nmap <buffer> K  <plug>(lsp-hover)
  nmap <buffer> <F12>   <plug>(lsp-definition)
  nmap <buffer> <S-F12> <plug>(lsp-references)
  nmap <buffer> <F2>    <plug>(lsp-rename)
  nmap <buffer> <C-LeftMouse> <LeftMouse><plug>(lsp-definition)
  nmap <buffer> [g <plug>(lsp-previous-diagnostic)
  nmap <buffer> ]g <plug>(lsp-next-diagnostic)
  nmap <buffer> <leader>rn <plug>(lsp-rename)
  nmap <buffer> <leader>ca <plug>(lsp-code-action)
  nmap <buffer> <leader>F  <plug>(lsp-document-format)
  nmap <buffer> <leader>o  :LspDocumentSymbolSearch<CR>
  nmap <buffer> <leader>s  :LspWorkspaceSymbolSearch<CR>
  nmap <buffer> <leader>d  :LspDocumentDiagnostics<CR>
endfunction
augroup lsp_install
  autocmd!
  autocmd User lsp_buffer_enabled call s:on_lsp_buffer_enabled()
augroup END
let g:lsp_diagnostics_virtual_text_enabled = 1

" Tab: move through the autocomplete menu when it's open, otherwise accept
" Copilot's grey suggestion, otherwise insert a normal Tab
" Shift-Tab moves back through the menu, Enter accepts from the menu
imap <silent><script><expr> <Tab> pumvisible() ? "\<C-n>"
      \ : exists('g:loaded_copilot') ? copilot#Accept("\<Tab>") : "\<Tab>"
inoremap <expr> <S-Tab> pumvisible() ? "\<C-p>" : "\<S-Tab>"
inoremap <expr> <CR>    pumvisible() ? asyncomplete#close_popup() : "\<CR>"

" ---------- Machine-specific overrides ----------
if filereadable(expand('~/.vimrc.local'))
  source ~/.vimrc.local
endif
