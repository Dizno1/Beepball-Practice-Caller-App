from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "audio"
EXTS = {".mp3", ".m4a", ".wav", ".ogg"}


def audio_files(folder_name):
    folder = AUDIO / folder_name
    if not folder.exists():
        return []
    return sorted(
        [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in EXTS],
        key=lambda p: p.name.lower(),
    )


def pretty_text(text):
    text = re.sub(r"[_-]+", " ", text)
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def recording_key(path, side):
    """Return a side-neutral key for matching files in left and right folders.

    The containing folder already identifies the side, so filenames may either
    include a trailing side marker or omit it entirely.
    """
    stem = path.stem.strip()
    stem = re.sub(rf"(?:[\s_-]+){side}$", "", stem, flags=re.IGNORECASE)
    return re.sub(r"[\s_-]+", " ", stem).strip().casefold()


def caller_and_call_type(path, side):
    """Extract the caller once and retain the remainder as the call description.

    Supported examples:
      Nick_1_fly_left.mp3       -> Nick / 1 fly
      Gina_fly_ball_1_right.mp3 -> Gina / fly ball 1
      Pete 1 hard.m4a           -> Pete / 1 hard
    """
    stem = path.stem.strip()
    stem = re.sub(rf"(?:[\s_-]+){side}$", "", stem, flags=re.IGNORECASE)
    cleaned = pretty_text(stem)
    parts = cleaned.split(" ", 1)
    caller = parts[0].strip()
    call_type = parts[1].strip() if len(parts) > 1 else cleaned
    return caller, call_type


left_files = audio_files("left")
right_files = audio_files("right")
right_by_key = {recording_key(path, "right"): path for path in right_files}

callers = {}
missing_right = []
matched_right_keys = set()

for left_path in left_files:
    key = recording_key(left_path, "left")
    right_path = right_by_key.get(key)
    if not right_path:
        missing_right.append(left_path.name)
        continue

    matched_right_keys.add(key)
    caller, call_type = caller_and_call_type(left_path, "left")
    callers.setdefault(caller, []).append(
        {
            "callType": call_type,
            "leftFile": left_path.relative_to(ROOT).as_posix(),
            "rightFile": right_path.relative_to(ROOT).as_posix(),
        }
    )

missing_left = [
    path.name
    for path in right_files
    if recording_key(path, "right") not in matched_right_keys
]

for calls in callers.values():
    calls.sort(key=lambda item: item["callType"].casefold())

callers = dict(sorted(callers.items(), key=lambda item: item[0].casefold()))
pitchers = [
    {"label": pretty_text(path.stem), "file": path.relative_to(ROOT).as_posix()}
    for path in audio_files("pitchers")
]
sounds = [
    {"label": pretty_text(path.stem), "file": path.relative_to(ROOT).as_posix()}
    for path in audio_files("sounds")
]

library = {"callers": callers, "pitchers": pitchers, "sounds": sounds}

(ROOT / "audioLibrary.json").write_text(
    json.dumps(library, indent=2), encoding="utf-8"
)
(ROOT / "audioLibrary.js").write_text(
    "window.audioLibrary = " + json.dumps(library, indent=2) + ";\n",
    encoding="utf-8",
)

print("Generated audioLibrary.js and audioLibrary.json")
print(f"Callers: {len(callers)}")
for caller, calls in callers.items():
    print(f"  {caller}: {len(calls)} paired calls")
print(f"Paired calls: {sum(len(value) for value in callers.values())}")
print(f"Pitchers: {len(pitchers)}")
print(f"Sounds: {len(sounds)}")

if missing_right:
    print("WARNING: Left recordings missing matching right recordings:")
    for name in missing_right:
        print("  " + name)

if missing_left:
    print("WARNING: Right recordings missing matching left recordings:")
    for name in missing_left:
        print("  " + name)

if missing_right or missing_left:
    sys.exit(1)
