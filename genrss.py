#!/usr/bin/env python3
from datetime import date, timedelta
from glob import glob
from os.path import basename,splitext
from uuid import UUID
from hashlib import sha3_224
from sys import stdout

NUM_EPISODES = 5
FOLDER= "audiofiles"
OFFSET=timedelta(13)
ROOT="mkettn.github.io/prolog-podcast"
FLIST="flist.txt"
TITLE="Prolog von Ohrid (alter Kalender)"
OUTPUT_FILE="altkal.xml"

ID=UUID(bytes=sha3_224(TITLE.encode()).digest()[:16])
today = date.today()-OFFSET
today_str = date.today().strftime("%Y-%m-%dT%H:%M:%SZ")

audiofiles = []

def get_xml(d:date):
    s = "{:s}/{:d}. *.ogg".format(FOLDER, int(d.strftime("%j")))
    f = glob(s)[0]
    audiofiles.append(f)
    t = splitext(basename(f))[0]
    u = d.strftime("%Y-%m-%dT%H:%M:%SZ")
    _id = UUID(bytes=sha3_224(f.encode()).digest()[:16])
    return f"""<entry>
    <title>{t}</title>
    <link href="{ROOT}/{f}"/>
    <id>urn:uuid:{_id}</id>
    <updated>{u}</updated>
    <summary>Prolog von Ohrid Episode bereitgestellt von www.orthodoxinfo.de</summary>
</entry>"""

with open(OUTPUT_FILE, 'w') as ofd:
    ofd.write(f"""<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom">
	<title>{TITLE}</title>
	<subtitle>Quelle: www.orthodoxinfo.de</subtitle>
	<link href="http://{ROOT}/{OUTPUT_FILE}" rel="self" />
	<link href="http://{ROOT}" />
	<id>urn:uuid:{ID}</id>
	<updated>{today_str}</updated>""")
    for i in range(NUM_EPISODES):
        d = today-timedelta(days=i)
        ofd.write(get_xml(d))
    ofd.write("</feed>")

with open(FLIST, 'w') as ofd:
    ofd.write(" ".join(map(lambda x: f'"{x}"', [OUTPUT_FILE] + audiofiles)))
    ofd.write("\n")



