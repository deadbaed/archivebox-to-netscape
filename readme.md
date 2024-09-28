# archivebox to netscape bookmarks

I was transferring my bookmarks from [archivebox](https://archivebox.io/) to [linkding](https://linkding.link).

Linkding supports importing existing bookmarks saved in the Netscape bookmarks format (which is extremely not documented).

I could not find a quick way to export the bookmarks from my archivebox installation, so I quickly wrote one using the sqlite database where archivebox stores links.

## requirements

modern python

## get started

1. `python3 -m venv venv`
2. `source ./venv/bin/activate`
3. `pip install -r requirements.txt`

## how to run

In your archivebox installation, locate and retrieve the sqlite database.

`./main.py <database>`
