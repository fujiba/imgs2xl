#!/usr/bin/env python
# coding: utf-8
import sys
import argparse
import imgs2xl


def verbose_callback(filename, total, n):
    print(f"{filename} ({n}/{total})")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an Excel sheet with thumbnails from an image files."
    )

    parser.add_argument(
        "inputdir", nargs="?", help="Input directory that contain image files."
    )
    parser.add_argument("output", nargs="?", help="Output Excel file name.")
    parser.add_argument(
        "--recursive", action="store_true", help="Recursively search for files."
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose mode(default False)"
    )
    parser.add_argument(
        "--size", type=int, default=320, help="Thumbnails size.(default 320px)"
    )
    parser.add_argument("--input-json", type=str, help="Use parameters json file.")
    parser.add_argument(
        "--generate-skeleton", type=str, help="Create parameters skeleton json file."
    )
    parser.add_argument(
        "--tags",
        help="Append exif tags. If specify the multiple tags, use commna for separate.The tag names may include group names, asusual in the format `<group>:<tag>`.",
    )

    args = parser.parse_args()

    if args.generate_skeleton is not None:
        imgs2xl.output_json(args.generate_skeleton, "", "", False, 320, [])
        exit(0)

    if args.input_json is not None:
        _ = imgs2xl.input_json(args.input_json)
        imgspath = _["inputdir"]
        xlsxpath = _["output"]
        recursive = _["recursive"]
        thumbssize = _["size"]
        tags = _["tags"]
    else:
        imgspath = args.inputdir
        xlsxpath = args.output
        recursive = args.recursive
        thumbssize = args.size
        tags = args.tags
        tags = []
        if args.tags is not None:
            tags = args.tags.split(",")

    if imgspath is None or len(imgspath) <= 0:
        parser.print_usage()
        sys.stderr.write("inputdir is not specified.\n")
        exit(1)

    if xlsxpath is None or len(xlsxpath) <= 0:
        parser.print_usage()
        sys.stderr.write("output is not specified.\n")
        exit(1)

    callback = verbose_callback if args.verbose else None
    imgs2xl.run(imgspath, xlsxpath, thumbssize, tags, recursive, callback)


if __name__ == "__main__":
    main()
