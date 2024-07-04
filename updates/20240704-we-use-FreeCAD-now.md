# Switch from bespoke Python script (`make_lens.py`) to FreeCAD

Lmao. Insanely rookie mistake. I was like, huh, I need to parametrically generate a lens model. Surely a Python script that manually writes an `.obj` is the best way to do that?

NO! This is what CAD software is for. It's literally programmatic by default. Have made [`lens.FCStd`](/lens.FCStd) which replaces [`make_lens.py`](/make_lens.py).

Just click `VariableHolder_EDIT_ME`, and go to properties -> Lens, and you can change the variables.