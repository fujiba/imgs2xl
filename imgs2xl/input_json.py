#!/usr/bin/env python
# coding: utf-8

import json


def output_json(
    jsonpath: str,
    imgsdir: str,
    xlsxpath: str,
    recursive: bool,
    thumbssize: int,
    tags: list[str],
):
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
    with open(jsonpath, mode="r", encoding="utf-8") as file:
        return json.load(file)
