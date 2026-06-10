import re
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "assembled-landing" / "code.html"
t = p.read_text(encoding="utf-8")
classes = set()
for m in re.finditer(r'class="([^"]+)"', t):
    for c in m.group(1).split():
        classes.add(c)
print(len(classes))
for c in sorted(classes):
    print(c)
