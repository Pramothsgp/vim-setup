#!/usr/bin/env bash
# Checks every shortcut and command in CHEATSHEET.md against your own Vim
# and config. Nothing in your projects is touched: each check runs in a
# throwaway copy of a small sample project.
#
#   tests/run.sh                 run everything (takes a few minutes)
#   tests/run.sh 'git|explorer'  only cases whose id matches the pattern
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d "${TMPDIR:-/tmp}/vim-setup-test.XXXXXX")"
trap '[ -n "${VS_KEEP:-}" ] || rm -rf "$TMP"' EXIT
export VS_FIXTURE="$TMP/fixture" VS_WORK="$TMP/work" VS_STUBS="$TMP/stubs"
export VS_CASES="$TMP/cases.json" VS_RESULTS="$TMP/results.jsonl" VS_ONLY="${1:-}"

python3 "$REPO_DIR/guide/build.py" --cases "$VS_CASES" >/dev/null || exit 1

# ---------- sample project (a git repo with history, a branch and a remote)
F="$VS_FIXTURE"
mkdir -p "$F/src" "$F/web" "$F/node_modules/lib" "$F/.github"
cat > "$F/app.py" <<'EOF'
def add(a, b):
    return a + b


def greet(name):
    return "Hello, " + name


total = add(1, 2)
print(greet("Vim"), total)
EOF
cat > "$F/util.py" <<'EOF'
from app import add

result = add(3, 4)
EOF
cat > "$F/broken.py" <<'EOF'
count: int = "not a number"
value = undefined_name
EOF
cat > "$F/hello.py" <<'EOF'
open("ran.txt", "w").write("ran")
EOF
printf 'alpha\nbeta\ngamma\n' > "$F/notes.txt"
printf 'one\n' > "$F/src/a.py"
printf 'two\n' > "$F/src/b.py"
printf 'module.exports = 1\n' > "$F/node_modules/lib/index.js"
printf '<p>hi</p>\n' > "$F/web/index.html"
printf '* @team-lead\n/src/ @python-team\n' > "$F/.github/CODEOWNERS"
printf '# Sample project\n' > "$F/README.md"
cat > "$F/web/shapes.ts" <<'EOF'
interface Shape {
  area(): number;
}

class Square implements Shape {
  constructor(private side: number) {}
  area(): number {
    return this.side * this.side;
  }
}

const shape: Shape = new Square(2);
console.log(shape.area());
EOF
printf 'check:\n\t@echo "app.py:2:5: error: something is wrong"\n\t@false\n' > "$F/Makefile"
(
  cd "$F" || exit 1
  git init -q -b main
  git config user.name "Test User"; git config user.email "test@example.com"
  git config commit.gpgsign false
  git add -A; git commit -q -m "Initial commit"
  sed -i.bak 's/return a + b/return a + b  # sum/' app.py && rm -f app.py.bak
  git commit -qam "Explain add"
  git checkout -q -b feature
  printf 'alpha\nBETA from feature\ngamma\n' > notes.txt; git commit -qam "Change beta on feature"
  git checkout -q main
  git init -q --bare -b main "$TMP/remote.git"
  git remote add origin "$TMP/remote.git"; git push -q -u origin main 2>/dev/null
)
cp -a "$TMP/remote.git" "$TMP/remote.tpl"
export VS_REMOTE="$TMP/remote.git" VS_REMOTE_TPL="$TMP/remote.tpl"

# ---------- stand-ins for claude and copilot: they echo what they're sent
mkdir -p "$VS_STUBS"
for t in claude copilot; do
  # shellcheck disable=SC2016  # $line belongs to the stand-in script
  printf '#!/bin/sh\necho "%s stand-in ready"\nwhile IFS= read -r line; do echo "got: $line"; done\n' "$t" > "$VS_STUBS/$t"
  chmod +x "$VS_STUBS/$t"
done

export LANG="${LANG:-en_US.UTF-8}" LC_ALL="${LC_ALL:-C.UTF-8}"
# ---------- run Vim in a real terminal so it behaves as when you use it
VIMCMD="stty rows 40 cols 140; vim -N -i NONE -S \"$REPO_DIR/tests/run.vim\""
cd "$TMP" || exit 1
if [ "$(uname -s)" = Darwin ]; then
  TERM=xterm-256color script -q /dev/null sh -c "$VIMCMD" >/dev/null 2>&1 </dev/null &
else
  TERM=xterm-256color script -qec "$VIMCMD" "${VS_SCREEN:-/dev/null}" >/dev/null 2>&1 </dev/null &
fi
PID=$!
last=""; still=0
while kill -0 "$PID" 2>/dev/null; do
  sleep 2
  now="$(head -1 "$VS_RESULTS.progress" 2>/dev/null || true)"
  if [ "$now" = "$last" ]; then still=$((still + 2)); else still=0; last="$now"; fi
  if [ "$still" -ge 90 ]; then
    echo "Stuck on: $now — stopping."; kill "$PID" 2>/dev/null; break
  fi
done

python3 - "$VS_RESULTS" "$VS_CASES" "$VS_ONLY" <<'EOF'
import json, sys
results = [json.loads(l) for l in open(sys.argv[1])] if __import__('os').path.exists(sys.argv[1]) else []
cases = {c['id']: c for c in json.load(open(sys.argv[2]))}
passed = [r for r in results if not r['fails'] and 'skip' not in r]
failed = [r for r in results if r['fails']]
skipped = [r for r in results if 'skip' in r]
manual = [c for c in cases.values() if c.get('manual')]
for r in failed:
    c = cases.get(r['id'], {'keys': 'config check'})
    print(f"FAIL {r['id']}  ({c['keys']})")
    for f in r['fails']:
        print('     ' + f.replace('\n', '\n     '))
for r in skipped:
    print(f"skip {r['id']}: {r['skip']}")
ran = len(passed) + len(failed)
print(f"\n{len(passed)} passed, {len(failed)} failed, {len(skipped)} skipped "
      f"(not set up on this machine), {len(manual)} need a person (listed in CHEATSHEET.md)")
import re
want = [c for c in cases.values() if not c.get('manual') and re.search(sys.argv[3] or '', c['id'])]
print(f"{len([r for r in results if r['id'] in cases])} of {len(want)} automatic checks ran")
sys.exit(1 if failed else 0)
EOF
