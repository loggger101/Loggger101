# Image generators

The banner, typing line, stat tiles, repo diagram and gallery thumbnails in `docs/` are generated, not hand-edited.
Run from the repo root:

```bash
python tools/banner.py docs/banner.svg
python tools/tiles.py docs/stats      # full tiles plus the -compact versions phones get
python tools/gallery.py docs/gallery  # project cards, plus the -compact versions phones get
python tools/typing_line.py docs/typing.svg
python tools/pipeline.py docs         # the repo diagram, plus the -compact version phones get
```

`gallery.py` reads each project's images from the local clones under
`C:\Users\Loggg\OneDrive\Documents\GitHub` and needs Pillow and numpy. The numbers on the
tiles are set in `tiles.py`; check them against the source repos before changing.
The arrows in `pipeline.py` follow what each repo's README says it reads from
the others; check both READMEs before adding or moving one.
