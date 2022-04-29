#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import glob
import imghdr
import tempfile
import exiftool

import openpyxl
from openpyxl.styles import Alignment
from PIL import Image


def attach_image(ws, img: str, col: int, row: int):
    pilImage = Image.open(img)
    ws.row_dimensions[row].height = pilImage.height * 0.75
    wsImg = openpyxl.drawing.image.Image(img)
    cell_address = ws.cell(row=row, column=col).coordinate
    wsImg.anchor = cell_address
    ws.add_image(wsImg)
    return pilImage.width


def get_exif(file):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata(file)
        return metadata


def add_tags(ws, tags, file: str, col: int, row: int):
    if len(tags) <= 0:
        return

    exif = get_exif(file)

    offset = 0
    for tag in tags:
        cell = ws.cell(row=row, column=col + offset)
        cell.value = str(exif.get(tag, ""))
        cell.alignment = Alignment(wrapText=True, vertical="top")
        offset += 1


def resize_image(imgpath: str, size: int, outdir: str):
    pilImage = Image.open(imgpath)
    pilImage.thumbnail((size, size))

    path = os.path.join(outdir, os.path.basename(imgpath))
    pilImage.save(path)

    return path


def main():

    parser = argparse.ArgumentParser(
        description="Generate an Excel sheet with thumbnails from an image files."
    )

    parser.add_argument("inputdir", help="Input directory that contain image files.")
    parser.add_argument("output", help="Output Excel file name.")
    parser.add_argument(
        "--size", type=int, default=320, help="Thumbnails size.(default 320px)"
    )
    parser.add_argument(
        "--tags",
        help="Append exif tags. If specify the multiple tags, use commna for separate. The tag names may include group names, asusual in the format `<group>:<tag>`.",
    )

    args = parser.parse_args()

    tags = []
    if args.tags is not None:
        tags = args.tags.split(",")

    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    ws.title = "image list"

    ws.cell(1, 1).value = "No."
    ws.cell(1, 2).value = "Thumbnail"
    ws.cell(1, 3).value = "Filename"

    i = 4
    for tag in tags:
        ws.cell(1, i).value = tag
        i += 1

    files = sorted(glob.glob(os.path.join(args.inputdir, "*")))
    tmppath = tempfile.TemporaryDirectory()

    row = 2
    max_width = 0
    max_filename = 0
    for file in files:
        if imghdr.what(file) != None:
            ws.cell(column=1, row=row).value = row - 1
            ws.cell(column=1, row=row).alignment = Alignment(vertical="top")
            thumb = resize_image(file, args.size, tmppath.name)
            width = attach_image(ws, thumb, 2, row)
            if width > max_width:
                max_width = width
            fn = os.path.basename(file)
            cell = ws.cell(column=3, row=row)
            cell.value = fn
            cell.alignment = Alignment(wrapText=True, vertical="top")

            if len(fn) > max_filename:
                max_filename = len(fn)

            add_tags(ws, tags, file, 4, row)

            row += 1

    ws.column_dimensions["B"].width = max_width * 0.13
    ws.column_dimensions["C"].width = (max_filename + 2) * 1.2

    for n in range(len(tags) + 1):
        colname = openpyxl.utils.get_column_letter(n + 3)
        max_length = 0
        for cell in ws[colname]:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))

        max_length = min(max_length, 100)
        ws.column_dimensions[colname].width = (max_length + 2) * 1.2

    wb.save(args.output)

    tmppath.cleanup()
