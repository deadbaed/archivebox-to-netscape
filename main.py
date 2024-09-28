#!/usr/bin/env python

import sqlite3
import argparse
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List,Optional

@dataclass
class ArchiveboxBookmark:
    id: str
    timestamp: str
    title: Optional[str]
    added: str
    updated: Optional[str]
    url: str

def get_archivebox_bookmarks(cur: sqlite3.Cursor) -> List[ArchiveboxBookmark]:
    cur.row_factory = lambda _cursor, row: ArchiveboxBookmark(*row)
    data: List[ArchiveboxBookmark] = cur.execute("select * from core_snapshot;").fetchall()
    return data

def create_html(bookmarks: List[ArchiveboxBookmark]) -> str:
    # thanks microsoft for a bit of documentation on the format
    # https://web.archive.org/web/20240925141030/https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)
    html = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!--This is an automatically generated file.
It will be read and overwritten.
Do Not Edit! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<Title>Bookmarks</Title>
<H1>Bookmarks</H1>
"""
    html += "<DL>\n"
    for link in bookmarks:
        # keep seconds in timestamps, format is  <seconds.milliseconds>
        timestamp_seconds = link.timestamp.split(".")[0]

        # use url as title if real title is not available
        title = link.title if link.title is not None else link.url

        # add new item to list
        html += f"<DT><A HREF=\"{link.url}\" ADD_DATE=\"{timestamp_seconds}\">{title}</A>\n"
    html += "</DL>"
    return html

def main(database: Path) -> int:
    # get data from database
    con = sqlite3.connect(database)
    archivebox_bookmarks = get_archivebox_bookmarks(con.cursor())
    con.close()

    # construct html
    html = create_html(archivebox_bookmarks)
    print(html)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ArchiveboxToNetscape",
        description="Convert Archivebox SQLite database to Netscape bookmarks format")
    parser.add_argument("database", help="Archivebox SQLite file to read")
    args = parser.parse_args()
    sys.exit(main(args.database))
