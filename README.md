# Rename File Sequence
A quick and dirty script for batch renaming file sequences.

Timelapse photography produces hundreds of files, which when named properly
in sequence, can be easily loaded into [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve#)

## How it works
```
IMG_0000.jpg
IMG_0001.jpg
IMG_0002.jpg
```
Becomes:
```
Your New Name (001).jpg
Your New Name (002).jpg
Your New Name (003).jpg
```

## Features
- Saves previous file names into JSON
- Undo (loads the aforementioned JSON and undoes renaming)
- Dry run (preview the result before committing)

## Usage
```
python rename.py path/to/dir [-n NEW_NAME] [-x EXTS [EXTS ...]] [-u] [--dry-run]
```

### Flags
- `-n`, `--new_name`: The new name of the file.
- `-x`, `--exts`: Extensions to look for e.g. `-x jpg png gif` (If empty, will be `["jpg", "png", "gif", "jpeg"]`)
- `-u`, `--undo`: Given that there is a JSON file in the same folder as the images, loads it and undoes renaming based on mappings.
- `--dry-run`: Preview the renaming results without actually doing it.
