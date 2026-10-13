"""Tests for loc.py's counting rules: one small sample per rule, with the count it should get.
Run from anywhere; CI runs it on every push (.github/workflows/check.yml).

    python tools/test_loc.py
"""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("loc", Path(__file__).resolve().parent / "loc.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
HERE = Path(tempfile.mkdtemp())

fails = 0
def eq(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}: got {got!r}, want {want!r}")

# C-style: strings hide comment markers; block and line comments; template literal spanning lines.
js = 'const g = "src/**/*.js"; // glob\n/* block\n still block */\nlet a = 1; /* x */ let b = 2;\n// only comment\nconst u = "http://x";\nconst t = `a\nb`;\n'
eq("js", m.c_lines(js), 5)
eq("js /* in a string isn't a comment", m.c_lines('const s = "/*";\nlet x = 1;\nlet y = 2;\n'), 3)
eq("js // in a string isn't a comment", m.c_lines('const u = "a//b"; let z = `\n/* not a comment */`;\n'), 2)
eq("js program in a template literal", m.c_lines('const PAGE = `<script>\n  // a comment in the page\n\n  run();\n</script>`;\nconst glob = `${d}/**/*.css`;\n'), 4)
eq("js unclosed quote ends at newline", m.c_lines("const s = 'it\nlet x = 1;\n// c\n"), 2)
eq("css", m.c_lines('a { content: "/* no */"; }\n/* c */\nb { }\n', line_comments=False), 2)
eq("css url //", m.c_lines('a { background: url(//cdn/x.png); }\n', line_comments=False), 1)
# Python: docstrings out, other strings in, trailing comments in.
eq("python", m.python_lines('"""doc"""\nx = 1  # c\n# c\ndef f():\n    """doc\n    two"""\n    return """a\n    b"""\n'), 4)
eq("python blank lines in a string", m.python_lines('x = """a\n\n   \nb"""\n'), 2)
# Perl: POD and __END__ data out.
src = "use strict;\n# c\n=pod\n\nabout\n\n=cut\nprint 1;\n__END__\nnot code\n"
p = HERE / "t.pl"; p.write_text(src, encoding="utf-8"); eq("perl", m.count(p, "perl"), 2)
p = HERE / "t.bat"; p.write_text("@echo off\nREM c\n@rem c\n:: c\necho hi\n", encoding="utf-8"); eq("batch", m.count(p, "batch"), 2)
p = HERE / "t.vbs"; p.write_text("' c\nRem c\nDim x\nx = 1 ' trailing\n", encoding="utf-8"); eq("vbscript", m.count(p, "vbscript"), 2)
p = HERE / "t.ps1"; p.write_text("<#\nhelp\n#>\n# c\nWrite-Host 1\n", encoding="utf-8"); eq("powershell", m.count(p, "powershell"), 1)
p = HERE / "t.ipynb"; p.write_text('{"cells":[{"cell_type":"code","source":["%matplotlib inline\\n","\\"\\"\\"doc\\"\\"\\"\\n","x = 1\\n","!pip install y\\n"]},{"cell_type":"markdown","source":["# Title"]}]}', encoding="utf-8")
eq("notebook", m.count(p, "notebook"), 3)
# Language detection.
heads = {"hooks/post-merge": b"#!/bin/sh\n", "bin/tool": b"#!/usr/bin/env python3\n", "LICENSE": b"MIT License", "run": b"#!/usr/bin/env -S node --x\n"}
lang = lambda path: m.language(path, lambda q: heads[q])
eq("sh shebang", lang("hooks/post-merge"), "hash")
eq("python shebang", lang("bin/tool"), "python")
eq("env -S node", lang("run"), "c")
eq("no shebang", lang("LICENSE"), None)
eq("Dockerfile", lang("Dockerfile"), "hash")
eq(".command", lang("launch.command"), "hash")
eq("markdown", lang("README.md"), None)
# .gitattributes.
rules = [("*.ipynb", ["linguist-documentation"]), ("master.py", ["linguist-generated=true"]),
         ("docs/*", ["linguist-vendored"]), ("docs/keep.py", ["-linguist-vendored"]), ("x.py", ["linguist-generated=false"])]
eq("ipynb nested", m.linguist_excluded("notebooks/a.ipynb", rules), True)
eq("master.py", m.linguist_excluded("master.py", rules), True)
eq("docs vendored", m.linguist_excluded("docs/a.py", rules), True)
eq("later unset wins", m.linguist_excluded("docs/keep.py", rules), False)
eq("=false", m.linguist_excluded("x.py", rules), False)
eq("plain file", m.linguist_excluded("src/a.py", rules), False)
shutil.rmtree(HERE)
sys.exit(f"{fails} failed" if fails else 0)
