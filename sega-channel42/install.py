#!/usr/bin/env python3
"""Install launcher files without root; never overwrite an existing station."""
import argparse
import json
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--prefix', type=Path, default=Path.home()/'sega-channel42')
parser.add_argument('--fs42', type=Path, help='Optional FieldStation42 directory')
parser.add_argument('--channel', type=int, default=42)
args = parser.parse_args()
if args.channel < 1:
    parser.error('channel must be positive')
source = Path(__file__).resolve().parent
prefix = args.prefix.expanduser().resolve()
station = None
if args.fs42:
    confs = args.fs42.expanduser().resolve()/'confs'
    if not confs.is_dir():
        parser.error('FieldStation42 confs directory not found')
    station = confs/'sega_channel42.json'
    if station.exists():
        parser.error('station file already exists; preserve/review it manually')
    for candidate in confs.glob('*.json'):
        try:
            data = json.loads(candidate.read_text()).get('station_conf', {})
        except (ValueError, OSError):
            continue
        if str(data.get('channel_number')) == str(args.channel):
            parser.error('channel already used by '+str(candidate))
for folder in ('bin', 'cores', 'roms', 'logs'):
    (prefix/folder).mkdir(parents=True, exist_ok=True)
for src, dst in [(source/'bin/sega-channel42', prefix/'bin/sega-channel42'),
                 (source/'config/retroarch.cfg', prefix/'retroarch.cfg')]:
    if dst.exists():
        print('Preserved existing:', dst)
    else:
        shutil.copy2(src, dst)
(prefix/'bin/sega-channel42').chmod(0o755)
if station:
    data = {'station_conf': {'network_name': 'Sega Channel', 'channel_number': args.channel,
            'network_type': 'executable', 'executable_command': str(prefix/'bin/sega-channel42')}}
    with station.open('x') as handle:
        json.dump(data, handle, indent=2)
        handle.write('\n')
    print('Created station:', station)
print('Installed launcher:', prefix/'bin/sega-channel42')
print('Supply your own compatible core and games; see README.md before launching.')
