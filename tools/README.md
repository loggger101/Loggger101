# Image generators

The banner, typing line, stat tiles and gallery thumbnails in `docs/` are generated, not hand-edited.
Run from the repo root:

```bash
python tools/banner.py docs/banner.svg
python tools/tiles.py docs/stats
python tools/gallery.py docs/gallery
python tools/typing.py docs/typing.svg
```

`gallery.py` reads each project's images from the local clones under
`C:\Users\Loggg\OneDrive\Documents\GitHub` and needs Pillow. The numbers on the
tiles are set in `tiles.py`; check them against the source repos before changing.
