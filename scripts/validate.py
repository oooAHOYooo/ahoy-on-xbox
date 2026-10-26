"""Source checks only; Windows SDK and device tests remain required."""
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

root = Path(__file__).resolve().parent.parent
for file in (root / 'AhoyXbox').glob('*.xaml'):
    ET.parse(file)
ET.parse(root / 'AhoyXbox/Package.appxmanifest')
ET.parse(root / 'AhoyXbox/AhoyXbox.csproj')
videos = json.loads((root / 'AhoyXbox/Data/catalog.json').read_text())['videos']
assert videos, 'Empty catalog'
assert len({v['id'] for v in videos}) == len(videos), 'Duplicate IDs'
for video in videos:
    assert video['title'] and video['status'] == 'available'
    uri = urlparse(video['url'])
    assert uri.scheme == 'https' and uri.hostname, video['id']
for name, size in {'StoreLogo': (50, 50), 'Square44x44Logo': (44, 44),
                   'Square150x150Logo': (150, 150), 'Wide310x150Logo': (310, 150),
                   'SplashScreen': (620, 300)}.items():
    data = (root / f'AhoyXbox/Assets/{name}.png').read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    assert struct.unpack('>II', data[16:24]) == size
print(f'Source checks passed: XML, {len(videos)} catalog entries, five development assets.')
print('Windows compilation, network playback, controller behavior, and certification are unverified.')
