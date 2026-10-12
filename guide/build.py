#!/usr/bin/env python3
"""Turns guide/levels/*.py into CHEATSHEET.md and the test cases for
tests/run.sh. Run it after editing any level:

    python3 guide/build.py                 # rewrite CHEATSHEET.md
    python3 guide/build.py --cases x.json  # also write the test cases
"""
import argparse
import importlib.util
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO = HERE.parent


def load_levels():
    levels = []
    for path in sorted((HERE / "levels").glob("l*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        levels.append(mod.LEVEL)
    return sorted(levels, key=lambda l: l["number"])


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def gh_anchor(text):
    """The id GitHub gives a heading, for links inside the page."""
    return re.sub(r"[^\w\- ]", "", text.lower()).replace(" ", "-")


QUICK = [
    ("Files", [("`Ctrl-p` / `Space p`", "Find a file in the project"), ("`Space f`", "Find a file in this folder"),
               ("`Space s`", "Search text in the project"), ("`Space b` / `Space r`", "Open files / recent files"),
               ("`Space /`", "Search lines in this file"), ("`Space e` / `Space E`", "Explorer / reveal this file"),
               ("`]b` / `[b`", "Next / previous file tab"), ("`Space 1`…`9`, `Space Tab`", "Go to tab N / last file"),
               ("`Space c`", "Close the file"), ("`Ctrl-s` / `Space w`", "Save"), ("`Space x` / `Space X`", "Hide from explorer and search / edit the list")]),
    ("Windows", [("`Space \\`", "Split side by side"), ("`Ctrl-h/j/k/l`", "Move between windows"), ("`Space q`", "Close window"),
                 ("`Ctrl-t` / `Space t`", "Terminal panel"), ("`Space h`", "Clear search highlight")]),
    ("Code (`Space l`…)", [("`gd` / `F12`", "Go to definition"), ("`gr` / `Shift-F12`", "References"), ("`K`", "Hover docs"),
                         ("`Space lp` / `li` / `lt`", "Peek / implementation / type definition"),
                         ("`Space lr` / `F2`", "Rename"), ("`Space la` / `lf`", "Code action / format"),
                         ("`Space lo` / `ls`", "Symbol in file / project"), ("`]g` / `[g`, `Space ld`", "Next / previous problem, all problems"),
                         ("`Ctrl-/`", "Toggle comment"), ("`Ctrl-n`", "Multiple cursors (in Normal mode)")]),
    ("Git (`Space g`…)", [("`Space gs`", "Status"), ("`Space gd` / `gb` / `gl`", "Diff / blame / file history"),
                        ("`]c` / `[c`", "Next / previous change"), ("`Space gp` / `ga` / `gu`", "Preview / stage / undo a change")]),
    ("AI (`Space a`…)", [("`Space aa` / `ag`", "Claude Code / Copilot CLI panel"), ("`Space af`", "Send file or selection to the panel"),
                       ("`Space ai` / `am`", "Copilot Chat / pick model"), ("`Space ac` / `ap`", "Copilot suggestions on-off / panel"),
                       ("`Tab`", "Accept a Copilot suggestion")]),
]

TROUBLE = [
    ("A key does nothing", "Press `Esc` twice and try again — you were probably in another mode. Then `:verbose map <key>` shows what the key is set to."),
    ("`Ctrl-s` freezes the terminal", "Press `Ctrl-q` to unfreeze. The installer adds `stty -ixon` to your shell config so `Ctrl-s` reaches Vim; open a new terminal."),
    ("`Alt-…` keys type odd characters on a Mac", "Make Option send Esc: iTerm2 → Profiles → Keys → Left Option key: Esc+; Terminal.app → Settings → Profiles → Keyboard → Use Option as Meta key."),
    ("`F2` / `F12` don't work on a Mac", "Hold `Fn`, or use `Space lr` and `gd`."),
    ("Copy/paste doesn't reach other apps", "Your Vim lacks clipboard support: `vim --version \\| grep clipboard` should show `+clipboard`. Homebrew's Vim has it."),
    ("`gd`, `K`, completion do nothing", "Run `:LspStatus`. If no server is listed, open a file of that language and run `:LspInstallServer`."),
    ("Copilot shows nothing", "`:Copilot status`; if not signed in, `:Copilot setup`."),
    ("Something looks wrong after editing the config", "`:source ~/.vimrc` reloads it; `tests/run.sh` checks every shortcut in this guide."),
]


def with_ids(levels):
    for lv in levels:
        for sec in lv["sections"]:
            for n, e in enumerate(sec["entries"], 1):
                e["id"] = f"L{lv['number']:02d}-{slug(sec['title'])}-{n:02d}"
    return levels


# ---------- markdown ----------
def code(text):
    text = text.replace("|", "\\|")
    if "`" in text:
        return f"`` {text} ``"
    return f"`{text}`"


def show_text(text):
    """Text for a table cell: one code span per line, leading spaces as ·"""
    out = []
    for line in text.split("\n"):
        if line.replace("▌", "") == "":
            out.append(code(line) if "▌" in line else "*(empty line)*")
            continue
        mark = "▌" if line.startswith("▌") else ""
        body = line[len(mark):]
        stripped = body.lstrip(" ")
        line = mark + "·" * (len(body) - len(stripped)) + stripped
        line = line.replace("\t", "⇥")
        out.append(code(line))
    return "<br>".join(out)


def cell(text):
    return text.replace("\n", " ").replace("|", "\\|") if text else ""


def change_cell(e):
    if "before" in e and "after" in e:
        return f"{show_text(e['before'])}<br>↓<br>{show_text(e['after'])}"
    return cell(e.get("result", ""))


def render(levels):
    total = sum(len(s["entries"]) for l in levels for s in l["sections"])
    manual = sum(1 for l in levels for s in l["sections"] for e in s["entries"] if e.get("manual"))
    out = []
    w = out.append
    w("# Vim from 0 to 100\n")
    w("A complete path from opening Vim for the first time to working in it every day, "
      "with this repo's setup. Work through the levels in order; each builds on the last.\n")
    w("## How to read this guide\n")
    w("- **`▌` is the cursor.** It sits on the character right after it: in `ca▌t` the cursor is on `t`. "
      "In Insert mode it's a thin bar between the two characters.")
    w("- **Keys:** `Ctrl-r` means hold Ctrl and press r. `Space` is the leader key: `Space p` means press Space, "
      "then p. Keys are case-sensitive: `A` means Shift-a. Commands starting with `:` end with `Enter`.")
    w("- **Cursor starts** says where to put the cursor before pressing the keys. **Before ↓ after** shows "
      "the text before and after. `·` stands for a space at the start of a line, `⇥` for a Tab.")
    w("- **Counts:** almost every command takes a number first: `3dd` deletes 3 lines, `5j` moves down 5.")
    w(f"- **Tested:** all {total - manual} rows without † were run automatically in real Vim with this "
      f"setup's Full install and gave exactly the result shown. Run `tests/run.sh` to check them on "
      f"your own machine. The {manual} rows marked † need a person (a sign-in, a mouse, macOS); "
      "the reason is given.\n")
    w("## This setup's shortcuts at a glance\n")
    w("Space is the leader key. Each is explained, with an example, in the levels below.\n")
    w("| | Keys | Does |")
    w("| --- | --- | --- |")
    for group, rows in QUICK:
        for n, (keys, does) in enumerate(rows):
            w(f"| {('**' + group + '**') if n == 0 else ''} | {keys.replace('|', chr(92) + '|')} | {does} |")
    w("")
    w("## Levels\n")
    for lv in levels:
        title = f"Level {lv['number']}: {lv['title']}"
        w(f"- [{title}](#{gh_anchor(title)})")
    w("- [When a key doesn't work](#when-a-key-doesnt-work)")
    w("")
    for lv in levels:
        w(f"## Level {lv['number']}: {lv['title']}\n")
        w(lv["intro"].strip() + "\n")
        for sec in lv["sections"]:
            w(f"### {sec['title']}\n")
            if sec.get("intro"):
                w(sec["intro"].strip() + "\n")
            w("| Keys | Cursor starts | Before ↓ after | What happens |")
            w("| --- | --- | --- | --- |")
            for e in sec["entries"]:
                does = cell(e["does"])
                if e.get("manual"):
                    does += f" †*Not checked automatically: {cell(e['manual'])}*"
                keys = e["keys"].replace("|", "\\|")
                w(f"| {keys} | {cell(e['where'])} | {change_cell(e)} | {does} |")
            w("")
    w("## When a key doesn't work\n")
    w("| Problem | Fix |")
    w("| --- | --- |")
    for problem, fix in TROUBLE:
        w(f"| {problem} | {fix} |")
    w("")
    return "\n".join(out) + "\n"


# ---------- the same guide for a doc editor (no HTML in table cells) ----------
def doc_text(text):
    parts = []
    for line in text.split("\n"):
        if line.replace("▌", "") == "":
            parts.append(code(line) if "▌" in line else "*(empty)*")
            continue
        mark = "▌" if line.startswith("▌") else ""
        body = line[len(mark):]
        stripped = body.lstrip(" ")
        parts.append(code((mark + "·" * (len(body) - len(stripped)) + stripped).replace("\t", "⇥")))
    return " ⏎ ".join(parts)


def render_doc_parts(levels):
    parts = {}
    g = ["## This setup's shortcuts at a glance\n",
         "Space is the leader key. Each one is explained, with an example, in the levels below.\n",
         "| | Keys | Does |", "| --- | --- | --- |"]
    for group, rows in QUICK:
        for n, (keys, does) in enumerate(rows):
            g.append(f"| {('**' + group + '**') if n == 0 else ''} | {keys.replace('|', chr(92) + '|')} | {does} |")
    parts["glance"] = "\n".join(g) + "\n"
    for lv in levels:
        w = [f"## Level {lv['number']}: {lv['title']}\n", " ".join(lv["intro"].split()) + "\n"]
        for sec in lv["sections"]:
            w.append(f"### {sec['title']}\n")
            if sec.get("intro"):
                w.append(" ".join(sec["intro"].split()) + "\n")
            w += ["| Keys | Cursor starts | Before → after | What happens |", "| --- | --- | --- | --- |"]
            for e in sec["entries"]:
                does = cell(e["does"])
                if e.get("manual"):
                    does += f" †*Not checked automatically: {cell(e['manual'])}*"
                change = (f"{doc_text(e['before'])} → {doc_text(e['after'])}"
                          if "before" in e and "after" in e else cell(e.get("result", "")))
                w.append(f"| {e['keys'].replace('|', chr(92) + '|')} | {cell(e['where'])} | {change} | {does} |")
            w.append("")
        parts[f"level{lv['number']:02d}"] = "\n".join(w)
    t = ["## When a key doesn't work\n", "| Problem | Fix |", "| --- | --- |"]
    parts["trouble"] = "\n".join(t + [f"| {p} | {f} |" for p, f in TROUBLE]) + "\n"
    return parts


# ---------- test cases ----------
def cases(levels):
    out = []
    for lv in levels:
        for sec in lv["sections"]:
            for e in sec["entries"]:
                c = {k: v for k, v in e.items() if k not in ("where", "does", "result")}
                if e.get("manual"):
                    out.append(c)
                    continue
                if "feed" not in c and "steps" not in c:
                    m = re.fullmatch(r"`([^`\s]+)`", e["keys"])
                    if not m and "checks" in c:
                        c["feed"] = ""
                        out.append(c)
                        continue
                    if m and re.search(r"Ctrl-|Shift-|Space|Enter|Esc|Tab|Alt-|F\d", m.group(1)):
                        m = None
                    if not m:
                        raise SystemExit(f"{e['id']}: needs feed= (keys are {e['keys']!r})")
                    c["feed"] = m.group(1)
                out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases")
    ap.add_argument("--out", default=str(REPO / "CHEATSHEET.md"))
    ap.add_argument("--doc", help="also write the guide as one markdown file per part into this folder")
    args = ap.parse_args()
    levels = with_ids(load_levels())
    pathlib.Path(args.out).write_text(render(levels))
    if args.doc:
        for name, md in render_doc_parts(levels).items():
            (pathlib.Path(args.doc) / f"{name}.md").write_text(md)
    cs = cases(levels)
    if args.cases:
        pathlib.Path(args.cases).write_text(json.dumps([c for c in cs if not c.get("manual")] +
                                                       [c for c in cs if c.get("manual")], indent=1))
    print(f"{len(cs)} entries, {sum(1 for c in cs if c.get('manual'))} manual")


if __name__ == "__main__":
    main()
