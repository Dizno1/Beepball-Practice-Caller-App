from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / 'audio'
EXTS = {'.mp3', '.m4a', '.wav', '.ogg'}

def files(folder):
    return sorted([p for p in (AUDIO / folder).iterdir() if p.is_file() and p.suffix.lower() in EXTS], key=lambda p: p.name.lower())

def pretty_stem(stem):
    text = re.sub(r'[_-]+', ' ', stem)
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

left = files('left')
right_by_key = {re.sub(r'_right$', '', p.stem): p for p in files('right')}
callers = {}
missing_pairs = []
for lp in left:
    key = re.sub(r'_left$', '', lp.stem)
    rp = right_by_key.get(key)
    if not rp:
        missing_pairs.append(lp.name)
        continue
    parts = key.split('_', 1)
    caller = parts[0]
    call_type = pretty_stem(parts[1] if len(parts) > 1 else key)
    callers.setdefault(caller, []).append({
        'callType': call_type,
        'leftFile': lp.relative_to(ROOT).as_posix(),
        'rightFile': rp.relative_to(ROOT).as_posix(),
    })

pitchers = [{'label': pretty_stem(p.stem), 'file': p.relative_to(ROOT).as_posix()} for p in files('pitchers')]
sounds = [{'label': pretty_stem(p.stem), 'file': p.relative_to(ROOT).as_posix()} for p in files('sounds')]
library = {'callers': callers, 'pitchers': pitchers, 'sounds': sounds}

(ROOT / 'audioLibrary.json').write_text(json.dumps(library, indent=2), encoding='utf-8')
(ROOT / 'audioLibrary.js').write_text('window.audioLibrary = ' + json.dumps(library, indent=2) + ';\n', encoding='utf-8')

print(f"Generated audioLibrary.js and audioLibrary.json")
print(f"Callers: {len(callers)}")
print(f"Paired calls: {sum(len(v) for v in callers.values())}")
print(f"Pitchers: {len(pitchers)}")
print(f"Sounds: {len(sounds)}")
if missing_pairs:
    print('Missing right-side partners:')
    for name in missing_pairs:
        print('  ' + name)
