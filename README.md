# Beepball Practice Caller

Current build notes:

- The page title and main heading use Beepball Practice Caller.
- Audio starts from the normal practice and test buttons.
- No manual audio player is shown on the page.
- Pitcher cadence is selectable.
- Last call is displayed after the call has played, not before.

## Testing

Extract the ZIP first. Open `index.html` in Chrome. Do not run the file from inside the ZIP preview.

## Open Door Design visual standard applied

This project uses the Open Door Design AAA-oriented visual standard. The interface avoids blue/green pairings, uses green as the single brand accent, uses dark neutral text for structure, and uses a high-visibility gold focus indicator. Returned project archives intentionally exclude the `.git` directory.


## Visual remediation

- Added a keyboard-accessible Skip to main content link.
- Ensured the skip link sizes to its text instead of using a fixed narrow width.
- Limited the skip link to the viewport width while allowing readable wrapping on very small screens.
- Preserved the existing Open Door Design green button styling and light green page background.

## Dynamic audio library

The application no longer hardcodes callers, pitchers, or trial ball sounds in `index.html`.

The interface is populated from `audioLibrary.js`, which is generated from these folders:

- `audio/left`
- `audio/right`
- `audio/pitchers`
- `audio/sounds`

After adding, renaming, or removing audio files, run:

`py refreshAudioLibrary.py`

The script regenerates both `audioLibrary.js` for the browser and `audioLibrary.json` for inspection or future tooling. Commit and push the regenerated files with the audio changes.

Caller recordings must use matching left and right filenames. For example:

- `Alex_hard_1_left.mp3`
- `Alex_hard_1_right.mp3`

The first filename section becomes the caller name, and the remaining filename becomes the call description. Pitcher and sound labels are generated from their filenames.

The current generated library contains two callers, sixty-six paired calls, five pitchers, and one trial ball sound.
