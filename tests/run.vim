" vim-setup test runner. Started by tests/run.sh inside a real terminal, after
" your normal ~/.vimrc has loaded. Runs every case in $VS_CASES and appends
" one JSON result per line to $VS_RESULTS.
"
" A case types keys exactly as you would, then checks the buffer text, the
" cursor position, the mode, and any extra conditions it lists.

set encoding=utf-8
scriptencoding utf-8
set nomore
set shortmess+=F
let s:cases   = json_decode(join(readfile($VS_CASES), "\n"))
let s:fixture = $VS_FIXTURE
let s:work    = $VS_WORK
let s:out     = $VS_RESULTS
let s:only    = $VS_ONLY
let s:probe   = {}
let s:opts = {}
for s:o in ['wrap', 'list', 'spell', 'foldmethod', 'foldlevel', 'textwidth', 'paste',
      \ 'hlsearch', 'incsearch', 'ignorecase', 'smartcase', 'number', 'relativenumber']
  let s:opts[s:o] = eval('&' . s:o)
endfor

" Never start the real AI tools: use the stand-ins run.sh created
let g:vim_setup_claude_path  = $VS_STUBS . '/claude'
let g:vim_setup_copilot_path = $VS_STUBS . '/copilot'

" ---------- helpers usable in a case's checks ----------
" Filetypes of all windows, left to right / top to bottom
function! WinFts() abort
  return map(range(1, winnr('$')), {_, w -> getbufvar(winbufnr(w), '&filetype')})
endfunction
function! TermWins() abort
  return filter(range(1, winnr('$')), {_, w -> getbufvar(winbufnr(w), '&buftype') ==# 'terminal'})
endfunction
function! TermText(...) abort
  let wins = TermWins()
  if empty(wins) | return '' | endif
  let buf = winbufnr(wins[a:0 ? a:1 : 0])
  return join(getbufline(buf, 1, '$'), "\n")
endfunction
function! TreeOpen() abort
  return index(WinFts(), 'nerdtree') >= 0
endfunction
function! TreeText() abort
  for w in range(1, winnr('$'))
    if getbufvar(winbufnr(w), '&filetype') ==# 'nerdtree'
      return join(getbufline(winbufnr(w), 1, '$'), "\n")
    endif
  endfor
  return ''
endfunction
function! Listed() abort
  return map(filter(getbufinfo({'buflisted': 1}), 'v:val.name !=# ""'), 'fnamemodify(v:val.name, ":t")')
endfunction
function! Disk(path) abort
  return filereadable(a:path) ? join(readfile(a:path), "\n") : '<missing>'
endfunction
function! Sh(cmd) abort
  return trim(system(a:cmd))
endfunction
function! Popups() abort
  return len(filter(popup_list(), 'popup_getpos(v:val).visible'))
endfunction
function! QfLen() abort
  return len(getqflist())
endfunction
function! LocLen() abort
  return len(getloclist(0))
endfunction
function! WaitFor(expr, ms) abort
  let waited = 0
  while !eval(a:expr) && waited < a:ms
    sleep 50m
    let waited += 50
  endwhile
  return eval(a:expr)
endfunction

" Wait until this file's language server is running and has read the file
function! LspReady(...) abort
  if !WaitFor('!empty(lsp#get_allowed_servers())', 3000)
    let g:vs_skip = 'no language server for ' . &filetype . ' files (run :LspInstallServer in one)'
    return 0
  endif
  let servers = lsp#get_allowed_servers()
  let ms = a:0 ? a:1 : 30000
  call writefile(['lsp: waiting for ' . servers[0] . ' (' . lsp#get_server_status(servers[0]) . ')'], s:out . '.progress', 'a')
  call WaitFor('lsp#get_server_status(' . string(servers[0]) . ') ==# "running"', ms)
  call writefile(['lsp: status ' . lsp#get_server_status(servers[0]) . ', waiting for keys'], s:out . '.progress', 'a')
  " the server has attached to this file once its keys are mapped here
  call WaitFor('get(maparg("gd", "n", 0, 1), "buffer", 0)', ms)
  call writefile(['lsp: keys mapped=' . get(maparg('gd', 'n', 0, 1), 'buffer', 0)], s:out . '.progress', 'a')
  sleep 2000m
  return get(maparg('gd', 'n', 0, 1), 'buffer', 0)
endfunction

" Run a separate Vim in a hidden terminal, type keys into it, and report
" whether it exited and with which code. Used for the quit commands.
function! Child(args, keys, ...) abort
  let wait = a:0 ? a:1 : 2000
  let buf = term_start(['vim', '-N', '-i', 'NONE'] + a:args, {'hidden': 1, 'term_finish': 'open'})
  call s:Settle(buf, 800)
  for k in a:keys
    " each item is keys, [keys, milliseconds to wait after them], or
    " {'run': 'command'} to do something here meanwhile (e.g. change a file)
    if type(k) == v:t_dict
      execute k.run
      continue
    endif
    let [keys, ms] = type(k) == v:t_list ? k : [k, 300]
    call term_sendkeys(buf, s:K(keys))
    call s:Settle(buf, ms)
  endfor
  let job = term_getjob(buf)
  let waited = 0
  while job_status(job) ==# 'run' && waited < wait
    sleep 50m
    let waited += 50
  endwhile
  let r = {'status': job_status(job), 'exit': job_info(job).exitval}
  if r.status ==# 'run' | call job_stop(job, 'kill') | endif
  silent! execute 'bwipeout!' buf
  return r
endfunction

" Start a separate Vim with your config and report eval(expr) after wait ms
function! ChildEval(args, expr, ...) abort
  let wait = a:0 ? a:1 : 2500
  let f = tempname()
  let cmd = printf('call timer_start(%d, {-> [writefile([string(eval(%s))], %s), execute("qa!")]})',
        \ wait, string(a:expr), string(f))
  let buf = term_start(['vim', '-N', '-i', 'NONE'] + a:args + ['-c', cmd],
        \ {'hidden': 1, 'term_finish': 'open', 'term_rows': 40, 'term_cols': 140})
  let job = term_getjob(buf)
  let waited = 0
  while job_status(job) ==# 'run' && waited < wait + 6000
    sleep 50m
    let waited += 50
  endwhile
  if job_status(job) ==# 'run' | call job_stop(job, 'kill') | endif
  silent! execute 'bwipeout!' buf
  return filereadable(f) ? join(readfile(f), "\n") : '<no result>'
endfunction

function! s:Settle(buf, ms) abort
  call term_wait(a:buf, a:ms)
endfunction

" ---------- key notation: '<Esc>' -> real key ----------
function! s:Key(k) abort
  try
    return eval('"\' . a:k . '"')
  catch
    return a:k
  endtry
endfunction
function! s:K(str) abort
  return substitute(a:str, '<\%(\%([CSMADcsmad]-\)\+[^<> ]\+\|[A-Za-z][A-Za-z0-9]*\)>', '\=s:Key(submatch(0))', 'g')
endfunction

" ---------- '▌' marks the cursor: it sits on the character after it ----------
function! s:Parse(text) abort
  let lines = split(a:text, "\n", 1)
  let cur = [1, 1]
  for i in range(len(lines))
    let p = stridx(lines[i], '▌')
    if p >= 0
      let cur = [i + 1, p + 1]
      let lines[i] = strpart(lines[i], 0, p) . strpart(lines[i], p + strlen('▌'))
    endif
  endfor
  return [lines, cur]
endfunction

function! TestProbe() abort
  let s:probe = {'lines': getline(1, '$'), 'cur': [line('.'), col('.')],
        \ 'mode': mode(), 'buf': bufname('%'), 'cmdwin': getcmdwintype(),
        \ 'pum': pumvisible(), 'items': map(complete_info(['items']).items, 'v:val.word')}
  let g:probe = s:probe
  if mode() =~# "^[vV\<C-v>]"
    let s:probe.sel = s:Selection(getpos('v'), getpos('.'), mode())
  endif
endfunction

" The selected text, worked out from the two ends of the selection
function! s:Selection(a, b, mode) abort
  let [l1, c1] = [a:a[1], a:a[2]]
  let [l2, c2] = [a:b[1], a:b[2]]
  if [l1, c1] == [l2, c2] || l1 < l2 || (l1 == l2 && c1 < c2)
    let [s, e] = [[l1, c1], [l2, c2]]
  else
    let [s, e] = [[l2, c2], [l1, c1]]
  endif
  if a:mode ==# 'V'
    return join(getline(s[0], e[0]), "\n")
  elseif a:mode ==# 'v'
    let lines = getline(s[0], e[0])
    let last = lines[-1]
    let endbyte = e[1] - 1 + max([strlen(matchstr(last, '.', e[1] - 1)), 1])
    let lines[-1] = strpart(last, 0, endbyte)
    let lines[0] = strpart(lines[0], s[1] - 1)
    return join(lines, "\n")
  endif
  let [left, right] = [min([c1, c2]), max([c1, c2])]
  return join(map(getline(min([l1, l2]), max([l1, l2])), 'strpart(v:val, left - 1, right - left + 1)'), "\n")
endfunction

function! s:Show(lines, cur) abort
  let l = copy(a:lines)
  if a:cur[0] >= 1 && a:cur[0] <= len(l)
    let s = l[a:cur[0] - 1]
    let l[a:cur[0] - 1] = strpart(s, 0, a:cur[1] - 1) . '▌' . strpart(s, a:cur[1] - 1)
  endif
  return join(l, "\n")
endfunction

" ---------- fresh state before every case ----------
function! s:Reset() abort
  " Redraw like Vim does between your keystrokes; without it, output from an
  " earlier command (like :reg) leaves the screen scrolled and the next
  " message waits for a key press
  redraw!
  if mode() !=# 'n' | call feedkeys("\<C-\>\<C-n>\<Esc>", 'xt') | endif
  silent! call popup_clear(1)
  if getcmdwintype() !=# '' | call feedkeys("\<C-c>\<C-c>", 'xt') | endif
  silent! NERDTreeClose
  silent! unlet t:NERDTreeBufName
  silent! tabonly!
  silent! only!
  silent! diffoff!
  for b in term_list()
    silent! call job_stop(term_getjob(b), 'kill')
    silent! execute 'bwipeout!' b
  endfor

  enew!
  silent! %bwipeout!
  silent! lclose
  silent! cclose
  call system('rm -rf ' . shellescape(s:work) . ' && cp -a ' . shellescape(s:fixture) . ' ' . shellescape(s:work))
  if !empty($VS_REMOTE)
    call system('rm -rf ' . shellescape($VS_REMOTE) . ' && cp -a ' . shellescape($VS_REMOTE_TPL) . ' ' . shellescape($VS_REMOTE))
  endif
  execute 'cd' fnameescape(s:work)
  let @/ = ''
  nohlsearch
  clearjumps
  for r in split('abcdefghijklmnopqrstuvwxyz0123456789-"', '\zs')
    call setreg(r, [])
  endfor
  call setqflist([])
  delmarks A-Z
  for [name, val] in items(s:opts)
    execute 'let &' . name . ' = ' . string(val)
  endfor
  let v:errmsg = ''
  let g:copilot_enabled = 1
endfunction

" ---------- typing in steps, with pauses for slow things (searches, servers) ----------
" A step flagged 'xt!' stays in Insert mode (pickers, completion menus): the
" steps after it are typed from timers while Vim keeps running, then the
" result is recorded and Insert mode is left.
function! s:FeedLater(keys, timer) abort
  call feedkeys(a:keys, 't')
endfunction
function! s:Steps(steps) abort
  let i = 0
  while i < len(a:steps)
    let st = a:steps[i]
    let flags = get(st, 2, 'xt')
    if flags =~# '!'
      let delay = get(st, 1, 0)
      for rest in a:steps[i + 1 :]
        call timer_start(delay, function('s:FeedLater', [s:K(rest[0])]))
        let delay += get(rest, 1, 0)
      endfor
      call timer_start(delay, function('s:FeedLater', ["\<Cmd>call TestProbe()\<CR>\<C-\>\<C-n>"]))
      let start = reltime()
      call feedkeys(s:K(st[0]), 'xt!')
      let left = delay + 300 - float2nr(reltimefloat(reltime(start)) * 1000)
      if left > 0 | execute 'sleep' left . 'm' | endif
      call feedkeys('', 'xt')
      return
    endif
    call feedkeys(s:K(st[0]), flags)
    if get(st, 1, 0) > 0 | execute 'sleep' st[1] . 'm' | endif
    let i += 1
  endwhile
  call feedkeys("\<Cmd>call TestProbe()\<CR>", 'xt')
endfunction

" ---------- run one case ----------
function! s:Run(c) abort
  let res = {'id': a:c.id, 'fails': []}
  let reqs = get(a:c, 'requires', [])
  for r in reqs
    let missing = s:Missing(r)
    if !empty(missing)
      let res.skip = missing
      return res
    endif
  endfor
  try
    call s:Reset()
    for [path, content] in items(get(a:c, 'files', {}))
      if fnamemodify(path, ':h') !=# '.' | call mkdir(fnamemodify(path, ':h'), 'p') | endif
      call writefile(split(content, "\n", 1), path)
    endfor
    if has_key(a:c, 'before')
      let [lines, cur] = s:Parse(a:c.before)
      let fname = get(a:c, 'file', 'sample.' . get(a:c, 'ext', 'txt'))
      call writefile(lines, fname)
      execute 'edit' fnameescape(fname)
      call cursor(cur)
    endif
    let g:vs_skip = ''
    for cmd in get(a:c, 'setup', [])
      execute cmd
      if g:vs_skip !=# '' | let res.skip = g:vs_skip | return res | endif
    endfor
    let v:errmsg = ''
    messages clear
    let s:probe = {}
    if has_key(a:c, 'steps')
      call s:Steps(a:c.steps)
    elseif get(a:c, 'wait', 0) > 0
      " slow results (language servers, terminals): look after they arrive
      call feedkeys(s:K(get(a:c, 'feed', '')), 'xt')
      execute 'sleep' a:c.wait . 'm'
      call feedkeys("\<Cmd>call TestProbe()\<CR>", 'xt')
    else
      call feedkeys(s:K(get(a:c, 'feed', '')) . "\<Cmd>call TestProbe()\<CR>", 'xt')
    endif

    if has_key(a:c, 'after')
      let [elines, ecur] = s:Parse(a:c.after)
      let got = get(s:probe, 'lines', [])
      let gcur = get(s:probe, 'cur', [0, 0])
      if got !=# elines || (get(a:c, 'check_cursor', 1) && gcur != ecur)
        call add(res.fails, "text/cursor\n  expected: " . s:Show(elines, ecur)
              \ . "\n  got:      " . s:Show(got, gcur))
      endif
    endif
    if has_key(s:probe, 'mode')
      let emode = s:K(get(a:c, 'mode', has_key(a:c, 'after') ? 'n' : ''))
      if emode !=# '' && s:probe.mode !=# emode
        call add(res.fails, 'mode: expected ' . strtrans(emode) . ', got ' . strtrans(s:probe.mode))
      endif
    endif
    if has_key(a:c, 'sel') && get(s:probe, 'sel', '<none>') !=# a:c.sel
      call add(res.fails, 'selection: expected ' . string(a:c.sel) . ', got ' . string(get(s:probe, 'sel', '<none>')))
    endif
    for chk in get(a:c, 'checks', [])
      let ok = 0
      try
        let ok = eval(chk)
      catch
        call add(res.fails, 'check ' . chk . ' raised ' . v:exception)
        continue
      endtry
      if !ok
        let msg = 'check failed: ' . chk
        let lhs = matchstr(chk, '^.\{-}\ze\s*\%([=!]=\|[<>]=\?\|=\~\)[#?]\?\s')
        if !empty(lhs)
          try | let msg .= '   (left side was ' . string(eval(lhs)) . ')' | catch | endtry
        endif
        call add(res.fails, msg)
      endif
    endfor
    for [path, content] in items(get(a:c, 'disk', {}))
      if Disk(path) !=# content
        call add(res.fails, 'file ' . path . ': expected ' . string(content) . ', got ' . string(Disk(path)))
      endif
    endfor
    " Errors you'd actually see (plugins' silenced internal errors don't count)
    let shown = filter(split(execute('messages'), "\n"), {_, m -> m =~# '\v^E\d+:|^Error'})
    if !empty(shown) && !get(a:c, 'allow_error', 0)
      call add(res.fails, 'Vim showed an error: ' . join(shown, ' / '))
    endif
  catch
    call add(res.fails, 'runner error: ' . v:exception . ' @ ' . v:throwpoint)
  endtry
  return res
endfunction

function! s:Missing(req) abort
  let [kind, what] = split(a:req . ':', ':')[0:1]
  if kind ==# 'plugin'
    return exists('g:plugs') && has_key(g:plugs, what) && isdirectory(g:plugs[what].dir) ? '' : 'plugin ' . what . ' is not installed'
  elseif kind ==# 'exe'
    return executable(what) ? '' : what . ' is not installed'
  elseif kind ==# 'lsp'
    return ''   " checked by LspReady() once the case's file is open
  elseif kind ==# 'part'
    return VS(what) ? '' : 'the ' . what . ' part is switched off in your install'
  elseif kind ==# 'cmd'
    return exists(':' . what) == 2 ? '' : ':' . what . ' is not available'
  elseif kind ==# 'feature'
    return has(what) ? '' : 'this Vim has no +' . what
  endif
  return ''
endfunction

function! s:Main(...) abort
  for c in s:cases
    if !empty(s:only) && c.id !~# '\v' . s:only | continue | endif
    if get(c, 'manual', '') !=# '' | continue | endif
    call writefile(['start ' . c.id], s:out . '.progress')
    if !empty($VS_VERBOSE) | execute 'set verbose=15 verbosefile=' . $VS_VERBOSE | endif
    let r = s:Run(c)
    if !empty($VS_VERBOSE) | set verbose=0 verbosefile= | endif
    call writefile([json_encode(r)], s:out, 'a')
  endfor
  " Config check: no shortcut may be the start of a longer one (Vim would
  " pause and wait, or run the wrong one)
  if empty(s:only) || 'CONFIG' =~# '\v' . s:only
    call s:Reset()
    let lhs = map(filter(maplist(), {_, m -> m.mode =~# '[ n]' && !m.buffer && m.lhs !~# '<Plug>\|<SNR>'}), 'v:val.lhs')
    let clash = []
    for a in lhs
      for b in lhs
        if a !=# b && stridx(b, a) == 0 && a =~# '^<Space>'
          call add(clash, a . ' / ' . b)
        endif
      endfor
    endfor
    call writefile([json_encode({'id': 'CONFIG-no-overlapping-shortcuts',
          \ 'fails': empty(clash) ? [] : ['these shortcuts overlap: ' . join(clash, ', ')]})], s:out, 'a')
  endif
  call writefile(['done'], s:out . '.progress')
  qa!
endfunction

call timer_start(get(g:, 'vs_test_delay', 2500), function('s:Main'))
