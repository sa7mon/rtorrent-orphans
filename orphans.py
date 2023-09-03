import requests
import os
from pathlib import Path

api_base = "http://flood.ip.address:3000/api"
cookies = ""
s = requests.Session() 

res = s.post(f"{api_base}/auth/authenticate", json={"username": "", "password": ""})
if res.status_code != 200:
    print(res.status_code)
    print(f"error authenticating: {res.text}")

print(res.headers)
cookies = res.headers['Set-Cookie']

res = s.get(f"{api_base}/client/connection-test")
if res.status_code != 200:
    print(res.status_code)
    print(f"error authenticating: {res.text}")
print(res.text)

torrent_paths = []

for hash in res_torrents.json()['torrents'].keys():
    dir = res_torrents.json()['torrents'][hash]['directory']
    name = res_torrents.json()['torrents'][hash]['name']

    # Filter out torrents saved to white pool
    if not dir.startswith('/mnt/torrent/'):
        continue

    res = s.get(f"{api_base}/torrents/{hash}/contents")
    if res.status_code != 200:
        print(res.status_code)
        print(f"error authenticating: {res.text}")

    for f in res.json():
        a = os.path.join(dir, f['path'])
        a = a.replace('/mnt/torrent/downloads/', '/mnt/torrents/downloads/', 1)
        torrent_paths.append(a)


print(f"{len(torrent_paths)} files belong to torrents")


downloaded = []
for p in Path( '/mnt/torrents/downloads/' ).rglob( '*' ):
    if p.is_file():
        downloaded.append(str(p))
print(f"{len(downloaded)} files in downloads folder")

diff = set(downloaded) - set(torrent_paths)
print(f"{len(diff)} orphaned files")

with open("/tmp/orphans.txt", "w") as f:
    for d in sorted(diff):
        f.write(str(d) + "\n")
