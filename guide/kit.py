"""Building blocks for guide entries.

Every entry becomes one row in CHEATSHEET.md and one automatic check in
tests/run.sh, so what the guide says is exactly what was tested.

Text uses '▌' for the cursor: it sits on the character right after it
(in Insert mode, between the two characters).
"""


def E(keys, where, before, after, does, **kw):
    """An edit you can see in the text: `before` becomes `after`."""
    return dict(keys=keys, where=where, before=before, after=after, does=does, **kw)


def UI(keys, where, result, does, checks, **kw):
    """Something that changes the screen (a window, a panel, a file):
    `result` describes it, `checks` are Vim expressions that must be true.
    Keys to type go in feed= (nothing is typed by default)."""
    kw.setdefault("feed", "")
    return dict(keys=keys, where=where, result=result, does=does, checks=checks, **kw)


def M(keys, where, result, does, reason):
    """Can't be checked automatically (needs a sign-in, a mouse, macOS...)."""
    return dict(keys=keys, where=where, result=result, does=does, manual=reason)


def section(title, intro, entries, requires=None):
    """requires: what every entry here needs (e.g. ["plugin:vim-surround"]);
    on machines without it they're skipped with that reason."""
    if requires:
        for e in entries:
            if not e.get("manual"):
                e["requires"] = sorted(set(e.get("requires", []) + requires))
    return dict(title=title, intro=intro, entries=entries)


def level(number, title, intro, sections):
    return dict(number=number, title=title, intro=intro, sections=sections)
