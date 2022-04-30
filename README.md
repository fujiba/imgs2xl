# imgs2xl
Generate an Excel sheet with thumbnails from an image files.

# Description

This tool reads image files in a specified directory and generates an Excel sheet with thumbnails. It can optionally add specified Exif tags to the list.

![Image of output excel sheet image.](outputsample.png)

# Install

```bash
pip install git+https://github.com/fujiba/imgs2xl
```

# Usage

## CLI

imgs2xl [-h] [--size SIZE] [--tags TAGS] inputdir output

positional arguments

- inputdir     Input directory that contain image files.
- output       Output Excel file name.

optional arguments:

- -h, --help   show this help message and exit
- --size SIZE  Thumbnails size.(default 320px)
- --tags TAGS  Append exif tags. If specify the multiple tags, use commna for separate. The tag names may include group names, asusual in the format `<group>:<tag>`.

example

```bash
imgs2xl imgsdir imglist.xlsx --size 240 --tags EXIF:Model,EXIF:LensModel,EXIF:DateTimeOriginal
```

## GUI

```bash
gimgs2xl
```

![Image of output excel sheet image.](screenshot.png)

| UI Element       | Description                                                          |
|------------------|----------------------------------------------------------------------|
| Images path      | Input directory that contain image files.                            |
| Excel book path  | Output Excel file name.                                              |
| Thumbsnail size  | Thumnbsnails size.                                                   |
| Tags             | Famous tags are can select multiple.                                 |
| Other tags       | Specify a tag that is not in the list above, use comma for separate. |
| Run!             | Execute an imgs2xl to output Excel book.                             |
| Exit             | Exit this programm.                                                  |

# Requirements

- Python >= 3.7
  - openpyxl
  - Pillow
  - PyExifTool
- [exiftool CLI](https://exiftool.org/)

# Author

- [T.Fujiba]("https://github.com/fujiba/")
  - Web: https://www.fujiba.net/
  - Twitter: [@fujiba](https://twitter.com/fujiba)

# License

MIT License