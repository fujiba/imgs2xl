import math
import os
import datetime
import filetype
import re

from PIL import Image, ExifTags, IptcImagePlugin, TiffImagePlugin

_ILLEGAL_CHARACTERS_REGEX = re.compile(
    r"[\000-\010]|[\013-\014]|[\016-\037]|[\x00-\x1f\x7f-\x9f]|[\uffff]"
)

_EXIF_FILESOURCE = {
    0: "Other",
    1: "Transmissive Scanner",
    2: "Reflective Scanner",
    3: "Digital Still Camera",
}

_IIMP_PROPS = {
    5: "ObjectName",
    7: "EditStatus",
    8: "EditorialUpdate",
    10: "Urgency",
    12: "SubjectReference",
    15: "Category",
    20: "SupplementalCategory",
    22: "FixtureIdentifier",
    25: "Keywords",
    26: "ContentLocationCode",
    27: "ContentLocationName",
    30: "ReleaseDate",
    35: "ReleaseTime",
    37: "ExpirationDate",
    38: "ExpirationTime",
    40: "SpecialInstructions",
    42: "ActionAdvised",
    45: "ReferenceService",
    47: "ReferenceDate",
    50: "ReferenceNumber",
    55: "DateCreated",
    60: "TimeCreated",
    62: "DigitalCreationDate",
    63: "DigitalCreationTime",
    65: "OriginatingProgram",
    70: "ProgramVersion",
    75: "ObjectCycle",
    80: "ByLine",
    85: "ByLineTitle",
    90: "City",
    92: "SubLocation",
    95: "Province_State",
    100: "Country_PrimaryLocationCode",
    101: "Country_PrimaryLocationName",
    103: "OriginalTransmissionReference",
    105: "Headline",
    110: "Credit",
    115: "Source",
    116: "CopyrightNotice",
    118: "Contact",
    120: "CaptionAbstract",
    121: "LocalCaption",
    122: "WriterEditor",
    130: "ImageType",
    131: "ImageOrientation",
    135: "LanguageIdentifier",
}


def _get_aperture_value(rational):
    if not isinstance(rational, TiffImagePlugin.IFDRational):
        return str(rational)

    val = round(math.sqrt(pow(2, rational.numerator / rational.denominator)), 2)
    return f"f{val}"


def _get_shutter_speed_value(rational):
    if not isinstance(rational, TiffImagePlugin.IFDRational):
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


def _get_file_source(val):
    return _EXIF_FILESOURCE[val[0]] if val[0] in _EXIF_FILESOURCE else "unkonwn"


def _tostring_xmpval(xmpval: dict):
    v = ""

    if "Alt" in xmpval:
        v = xmpval["Alt"]["li"]["text"]
    elif "Seq" in xmpval:
        v = xmpval["Seq"]["li"]
    else:
        v = str(xmpval)

    return v


def _add_xmpvalues(metadata: dict, xmp: dict):
    for key in xmp:
        val = xmp[key]
        if isinstance(val, dict):
            metadata[f"XMP:{key}"] = _tostring_xmpval(val)
        else:
            metadata[f"XMP:{key}"] = val


def _normalise_exif_value(key, val):
    if key == "ShutterSpeedValue":
        value = _get_shutter_speed_value(val)
    elif key == "ApertureValue":
        value = _get_aperture_value(val)
    elif key == "ExposureProgram":
        value = _get_exposure_program(val)
    elif key == "FileSource":
        value = _get_file_source(val)
    elif key == "SceneType":
        value = f"{val[0]}"
    elif key == "ComponentsConfiguration":
        value = f"{val[0]} {val[1]} {val[2]} {val[3]}"
    elif key == "ImageDescription":
        value = val
    elif key == "UserComment":
        codec = "ascii"
        code = val[:8]
        if code[0] == 0x4A and code[1] == 0x49 and code[2] == 0x53:
            codec = "iso2022_jp"
        elif (
            code[0] == 0x55
            and code[1] == 0x4E
            and code[2] == 0x49
            and code[3] == 0x43
            and code[4] == 0x4F
            and code[5] == 0x44
            and code[6] == 0x45
        ):
            codec = "utf_16"
        value = val[8:].decode(codec)
    else:
        value = val.decode(encoding="utf-8") if isinstance(val, bytes) else str(val)
        value = _ILLEGAL_CHARACTERS_REGEX.sub("?", value)

    return value


def get_metadata(path: str):
    metadata = {}

    pilImage = Image.open(path)
    rawmeta = pilImage._getexif()

    # Generic file informations.
    metadata["File:Filename"] = os.path.basename(path)
    metadata["File:Directory"] = os.path.dirname(path)
    stat = os.stat(path)
    metadata["File:FileModifyDate"] = datetime.datetime.fromtimestamp(
        stat.st_mtime
    ).strftime("%Y/%m/%d %H:%M:%S")
    metadata["File:FileAccessDate"] = datetime.datetime.fromtimestamp(
        stat.st_mtime
    ).strftime("%Y/%m/%d %H:%M:%S")
    kind = filetype.guess(path)
    metadata["File:FileType"] = kind.mime.rsplit("/", 1)[1]
    metadata["File:FileTypeExtension"] = kind.extension
    metadata["File:MIMEType"] = kind.mime
    metadata["File:ImageWidth"] = pilImage.width
    metadata["File:ImageHeight"] = pilImage.height

    # retrieve exif values
    if rawmeta:
        for key in rawmeta:
            keyname = ExifTags.TAGS.get(key, str(key))
            metadata[f"EXIF:{keyname}"] = _normalise_exif_value(keyname, rawmeta[key])

    # retrieve IPTC values
    iptc = IptcImagePlugin.getiptcinfo(pilImage)
    if iptc:
        for key, val in iptc.items():
            if key[0] == 2 and key[1] in _IIMP_PROPS:
                if isinstance(val, list):
                    metadata[f"IPTC:{_IIMP_PROPS[key[1]]}"] = ",".join(
                        [x.decode() for x in val]
                    )
                else:
                    metadata[f"IPTC:{_IIMP_PROPS[key[1]]}"] = val.decode()

    # retrieve XMP values
    xmp = pilImage.getxmp()
    if (
        "xmpmeta" in xmp
        and "RDF" in xmp["xmpmeta"]
        and "Description" in xmp["xmpmeta"]["RDF"]
    ):
        if isinstance(xmp["xmpmeta"]["RDF"]["Description"], dict):
            _add_xmpvalues(metadata, xmp["xmpmeta"]["RDF"]["Description"])
        elif isinstance(xmp["xmpmeta"]["RDF"]["Description"], list):
            for sub in xmp["xmpmeta"]["RDF"]["Description"]:
                _add_xmpvalues(metadata, sub)

    return metadata
