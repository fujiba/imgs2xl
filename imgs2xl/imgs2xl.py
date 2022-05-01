#!/usr/bin/env python
# coding: utf-8

import os
import sys
import glob
import imghdr
import tempfile
import json
import math
import traceback

import openpyxl
import PIL
from openpyxl.styles import Alignment
from PIL import Image, ExifTags


def output_json(
    jsonpath: str,
    imgsdir: str,
    xlsxpath: str,
    recursive: bool,
    thumbssize: int,
    tags: list[str],
):
    """
    Generate a JSON file for CLI input arguments.

    Parameters
    ----------
    jsonpath : str
        Output JSON file path.
    imgspath : str
        Input directory that contain image files.
    xlsxpath: str
       Output Excel file name.
    thumbssize: int
       Thumbnails size.
    recursive: bool
        Recursively search for files.
    tags: list[str]
        Append exif tags.  The tag names may include group names, asusual in the format `<group>:<tag>`.
    """

    with open(jsonpath, mode="w", encoding="utf-8") as file:
        json.dump(
            {
                "inputdir": imgsdir,
                "output": xlsxpath,
                "recursive": recursive,
                "size": thumbssize,
                "tags": tags,
            },
            file,
            ensure_ascii=False,
            indent=2,
        )


def input_json(jsonpath: str):
    """
    Load CLI arguments from JSON file.

    Parameters
    ----------
    jsonpath : str
        Input JSON file path.
    """
    with open(jsonpath, mode="r", encoding="utf-8") as file:
        return json.load(file)


def _attach_image(ws, img: str, col: int, row: int):
    pilImage = Image.open(img)
    ws.row_dimensions[row].height = pilImage.height * 0.75
    wsImg = openpyxl.drawing.image.Image(img)
    cell_address = ws.cell(row=row, column=col).coordinate
    wsImg.anchor = cell_address
    ws.add_image(wsImg)
    return pilImage.width


def _get_aperture_value(rational):
    if not isinstance(rational, PIL.TiffImagePlugin.IFDRational):
        return str(rational)

    val = round(math.sqrt(pow(2, rational.numerator / rational.denominator)), 2)
    return f"f{val}"


def _get_shutter_speed_value(rational):
    if not isinstance(rational, PIL.TiffImagePlugin.IFDRational):
        return str(rational)

    val = round(pow(2, rational.numerator / rational.denominator))
    return f"1/{val}" if rational.numerator > 0 else str(val)


def _get_exposure_program(val):
    if type(val) is not int:
        return str(val)

    _EXPOSURE_PROGRAM = [
        "N/A",
        "Manual",
        "Normal program",
        "Aperture priority",
        "Shutter priority",
        "Creative program",
        "Action program ",
        "Portrait mode",
        "Landscape mode",
    ]
    return (
        _EXPOSURE_PROGRAM[val]
        if val >= 0 and val < len(_EXPOSURE_PROGRAM)
        else "Uknown"
    )


def _get_tagvalue(key, tag):
    if tag is None:
        return ""

    if key == "ShutterSpeedValue":
        value = _get_shutter_speed_value(tag)
    elif key == "ApertureValue":
        value = _get_aperture_value(tag)
    elif key == "ExposureProgram":
        value = _get_exposure_program(tag)
    else:
        value = str(tag)

    return value


def _add_tags(ws, tags, exif: dict, col: int, row: int):
    if len(tags) <= 0:
        return

    offset = 0
    for tag in tags:
        cell = ws.cell(row=row, column=col + offset)
        cell.value = _get_tagvalue(tag, exif.get(tag, ""))
        cell.alignment = Alignment(wrapText=True, vertical="top")
        offset += 1


def _retrieve_thumbs_and_exif(imgpath: str, size: int, outdir: str):
    pilImage = Image.open(imgpath)
    rawmeta = pilImage._getexif()
    pilImage.thumbnail((size, size))

    path = os.path.join(outdir, os.path.basename(imgpath))
    pilImage.save(path)

    exif = {ExifTags.TAGS.get(key, key): rawmeta[key] for key in rawmeta}

    return path, exif


def run(
    imgspath: str,
    xlsxpath: str,
    thumbssize: int,
    tags: list[str],
    recursive: bool,
    callback=None,
):
    """
    Generate an Excel sheet with thumbnails from an image files.

    Parameters
    ----------
    imgspath : str
        Input directory that contain image files.
    xlsxpath: str
       Output Excel file name.
    thumbssize: int
       Thumbnails size.
    recursive: bool
        Recursively search for files.
    tags: list[str]
        Append exif tags.  The tag names may include group names, asusual in the format `<group>:<tag>`.
    callback: function
        The callback function that called when processed per file.
        ```
        def verbose_callback(filename, total, n):
            filename: processed file name.
            total: total files num.
            n: current file num.
        ```
    """

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

    files = sorted(glob.glob(os.path.join(imgspath, "**"), recursive=recursive))
    tmppath = tempfile.TemporaryDirectory()

    try:
        row = 2
        max_width = 0
        max_filename = 0

        filenum = len(files)

        for n, file in enumerate(files):
            if os.path.isdir(file):
                continue
            if imghdr.what(file) != None:
                ws.cell(column=1, row=row).value = row - 1
                ws.cell(column=1, row=row).alignment = Alignment(vertical="top")
                thumb, exif = _retrieve_thumbs_and_exif(file, thumbssize, tmppath.name)
                width = _attach_image(ws, thumb, 2, row)
                if width > max_width:
                    max_width = width
                fn = os.path.basename(file)
                cell = ws.cell(column=3, row=row)
                cell.value = fn
                cell.alignment = Alignment(wrapText=True, vertical="top")

                if len(fn) > max_filename:
                    max_filename = len(fn)

                _add_tags(ws, tags, exif, 4, row)

                row += 1

            if callback:
                callback(file, filenum, n + 1)

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

        wb.save(xlsxpath)
    except Exception as e:
        sys.stderr.write(traceback.format_exc())
    finally:
        tmppath.cleanup()
