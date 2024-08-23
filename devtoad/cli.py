import os
import argparse

def parse_options():
    parser = argparse.ArgumentParser(description="Generate a prompt for a directory")
    parser.add_argument("pos_dir", type=str, default=".", nargs="?", help="Directory to generate prompt for (positional argument)")
    parser.add_argument("--dir", type=str, help="Directory to generate prompt for (optional flag)")
    parser.add_argument("--filters", type=str, nargs="+", help="File extensions to filter for")
    parser.add_argument("--outpath", type=str, default=".", help="Output path for prompt file")
    parser.add_argument("--outfile", type=str, help="Output file name for prompt file (default: <dir>_prompt)")
    parser.add_argument("--ignore-dir", type=str, nargs="+", help="Additional directories to ignore: specify directory names (e.g., .git, __pycache__, etc.)")
    parser.add_argument("--ignore-file", type=str, nargs="+", help="Additional file types to ignore: specify extensions with or without dot (e.g., py, ipynb, .c, etc.)")
    parser.add_argument("--config", type=str, help="Path to the custom configuration file (default: config.json)")
    args = parser.parse_args()

    # prioritize --dir flag over positional argument -- args.dir will be None if flag not invoked
    # but pos_dir will always at least be the default value of "."
    args.dir = args.dir or args.pos_dir

    # remove "/" from beginning and end of dir path so that we can work with the name alone
    if args.dir.startswith("/"): args.dir = args.dir[1:]
    if args.dir.endswith("/"): args.dir = args.dir[:-1]

    # set the outfile name
    if args.outfile is None:
        if args.dir == ".":
            # replace "." with the actual base directory name
            dir_name = os.path.basename(os.getcwd()) 
        else:
            dir_name = os.path.basename(args.dir)
        args.outfile = f"{dir_name}_prompt"

    # format the file extensions in ignore files
    if args.ignore_file:
        formatted_ignore_files = []
        for file in args.ignore_file:
            if file.startswith("."):              
                formatted_ignore_files.append(f"*{file}") # .py -> *.py
            elif len(file) < 5: # 4 seems reasonable 
                formatted_ignore_files.append(f"*{file}*") # docx -> *.docx
            else:                                   
                formatted_ignore_files.append(file) # explicit files like LICENSE and yolo.py
        args.ignore_file = formatted_ignore_files
    
    # also ignore the current prompt so that it doesn't become nested in itself
    if not args.ignore_file:
        args.ignore_file = [f"{args.outfile}.txt"]
    else:
        args.ignore_file.append(f"{args.outfile}.txt")
        
    # set the default config file path 
    if args.config is None:
        args.config = str(files("dir2prompt").joinpath("config.json"))
    return args


def main():
    args = parse_options()

    config = load_config(args.config)
    IGNORE_DIRS = config["IGNORE_DIRS"]
    IGNORE_FILES = config["IGNORE_FILES"]

    # extend the default ignore lists with cli args
    if args.ignore_dir:
        IGNORE_DIRS.extend(args.ignore_dir)
    if args.ignore_file:
        IGNORE_FILES.extend(args.ignore_file)

    prompt = build_prompt(dir=args.dir, filters=args.filters, IGNORE_DIRS=IGNORE_DIRS, IGNORE_FILES=IGNORE_FILES)

    save_file(prompt, outpath=args.outpath, outfile=args.outfile)
    
    print(f"Prompt saved to {os.path.join(args.outpath, args.outfile)}.txt")


if __name__ == "__main__":
    main()