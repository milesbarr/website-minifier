import os
from pathlib import Path

from ._css import minify_css
from ._html import minify_html
from ._json import minify_json
from ._xml import minify_xml


__all__ = [
    "minify_css",
    "minify_html",
    "minify_json",
    "minify_xml",
    "minify_file",
    "minify_dir",
]

_MINIFY_BY_EXTENSION = {
    ".atom": minify_xml,
    ".css": minify_css,
    ".html": minify_html,
    ".json": minify_json,
    ".rss": minify_xml,
    ".svg": minify_xml,
    ".webmanifest": minify_json,
    ".xml": minify_xml,
}


def minify_file(path: str | bytes | os.PathLike) -> None:
    path = Path(path)
    minify = _MINIFY_BY_EXTENSION.get(path.suffix)
    if not minify:
        return
    with path.open("r+") as f:
        s = f.read()
        minified = minify(s)
        if minified != s:
            f.seek(0)
            f.write(minified)
            f.truncate()


def minify_dir(path: str | bytes | os.PathLike) -> None:
    path = Path(path)
    for root, _, files in path.walk():
        for file in files:
            minify_file(root / file)
