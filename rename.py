import os
import json
import argparse
import datetime

parser = argparse.ArgumentParser(
    prog="Batch Rename",
    description="Batch rename files in current directory.",
    epilog="Usage example: python rename.py path/to/dir -n 'Shared Name'",
)

parser.add_argument("dirname")
parser.add_argument("-n", "--new_name", default="Untitled")
parser.add_argument("-x", "--exts", nargs="+", type=str)
parser.add_argument("-u", "--undo", action="store_true")
parser.add_argument("--dry-run", action="store_true")

args = parser.parse_args()

shall_undo = args.undo
dry_run = args.dry_run
directory_path = args.dirname
valid_exts = args.exts if args.exts else ["jpg", "png", "gif", "jpeg"]
old_names = {}
    
def handle_undo():
    try:
        print("Undoing using latest JSON file.")
        latest_json = [j for j in os.listdir(directory_path) if os.path.isfile(j) and j.split(".")[1].lower() == "json"][-1]
        with open(os.path.join(directory_path, latest_json), "r") as jf:
            file_name_mapping = json.load(jf)
            print(file_name_mapping)
            for i, f in enumerate([file for file in os.listdir(directory_path) if os.path.isfile(file)]):
                name, ext = f.split(".")
                if (ext.lower() in valid_exts):
                    new_name = file_name_mapping[f]
                    old_names[new_name] = f
                    if (dry_run):
                        print(f"{f} --> {new_name}")
                    else:
                        os.rename(os.path.join(directory_path, f), os.path.join(directory_path, new_name))
    except IndexError as e:
        import sys
        print("No JSON file found. No action taken.")
        sys.exit()
    except Exception as e:
        import sys
        print(f"An error occurred: {e}")
        sys.exit()


def handle_rename():
    print("Renaming...")
    all_files = [file for file in os.listdir(directory_path) if os.path.isfile(file)]
    digits = len(str(len(all_files)))
    for i, f in enumerate(all_files):
        name, ext = f.split(".")
        if (ext.lower() in valid_exts):
            n = i + 1
            pad_count = digits - len(str(n))
            padded_number = ("0" * pad_count) + str(n)
            new_name = f"{args.new_name}({padded_number}).{ext}"
            old_names[new_name] = f
            if (dry_run):
                print(f"{f} --> {new_name}")
            else:
                os.rename(os.path.join(directory_path, f), os.path.join(directory_path, new_name))


if __name__ == "__main__":
    if (shall_undo):
        handle_undo()
    else:
        handle_rename()
        
    today = datetime.datetime.today().strftime("%Y-%b-%d_%H%M%S")
    output_file_name = f"old_names_{today}.json"
    if (dry_run):
        print(f"Will output mapping to: {output_file_name}")
    else:
        with open(output_file_name, "w") as f:
            f.write(json.dumps(old_names))