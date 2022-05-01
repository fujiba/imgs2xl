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

imgs2xl.py [-h] [--recursive] [--verbose] [--size SIZE] [--input-json INPUT_JSON]
                  [--generate-skeleton GENERATE_SKELETON] [--tags TAGS]
                  [inputdir] [output]

positional arguments

| Argument         | Description                               |
|------------------|-------------------------------------------|
| inputdir         | Input directory that contain image files. |
| output           | Output Excel file name.                   |

optional arguments:

| Argument                              | Description                               |
|---------------------------------------|-------------------------------------------|
| -h, --help                            | show this help message and exit           |
| --size SIZE                           | Thumbnails size.(default 320px)           |
| --tags TAGS                           | Append exif tags. If specify the multiple tags, use commna for separate. |
| --input-json INPUT_JSON               | Use parameters json file.                 |
| --generate-skeleton GENERATE_SKELETON | Create parameters skeleton json file.     |
| --recursive                           | Recursively search for files.             |
| --verbose                             | Verbose mode(default False)               |

example

```bash
imgs2xl imgsdir imglist.xlsx --size 240 --tags Model,LensModel,DateTimeOriginal
```

### Input JSON

The imgs2xl is using parameters as JSON file. JSON file sample is following.

```json
{
  "inputdir": "/Users/fujiba/tmp/2022.04.25",
  "output": "/Users/fujiba/tmp/hoge.xlsx",
  "recursive": false,
  "size": 320,
  "tags": ["Make", "Model"]
}
```

To generate a skeleton file is calling `imgs2xl --generate-skeleton jsonfilename`.

## GUI

```bash
gimgs2xl
```

![Image of output excel sheet image.](screenshot.png)

| UI Element       | Description                                                          |
|------------------|----------------------------------------------------------------------|
| Images path      | Input directory that contain image files.                            |
| Recursive        | Recursively search for files.                                        |
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

GUI application is using `tkinter`. When happen a following error, you need install `python-tk`.

```
 File “/opt/homebrew/Cellar/python@3.9/3.9.5/Frameworks/Python.framework/Versions/3.9/lib/python3.9/tkinter/__init__.py”, line 37, in <module>

  import _tkinter # If this fails your Python may not be configured for Tk

ModuleNotFoundError: No module named ‘_tkinter’
```

To install `tkinter`, do the following.

* macOS
```bash
brew install python-tk
```

* linux(ubuntu)
```bash
sudo apt install python-tk
```

# Author

- [T.Fujiba]("https://github.com/fujiba/")
  - Web: https://www.fujiba.net/
  - Twitter: [@fujiba](https://twitter.com/fujiba)

# License

MIT License

# Appendix

## Exif tag names

```
InteropIndex
ProcessingSoftware
NewSubfileType
SubfileType
ImageWidth
ImageLength
BitsPerSample
Compression
PhotometricInterpretation
Thresholding
CellWidth
CellLength
FillOrder
DocumentName
ImageDescription
Make
Model
StripOffsets
Orientation
SamplesPerPixel
RowsPerStrip
StripByteCounts
MinSampleValue
MaxSampleValue
XResolution
YResolution
PlanarConfiguration
PageName
FreeOffsets
FreeByteCounts
GrayResponseUnit
GrayResponseCurve
T4Options
T6Options
ResolutionUnit
PageNumber
TransferFunction
Software
DateTime
Artist
HostComputer
Predictor
WhitePoint
PrimaryChromaticities
ColorMap
HalftoneHints
TileWidth
TileLength
TileOffsets
TileByteCounts
SubIFDs
InkSet
InkNames
NumberOfInks
DotRange
TargetPrinter
ExtraSamples
SampleFormat
SMinSampleValue
SMaxSampleValue
TransferRange
ClipPath
XClipPathUnits
YClipPathUnits
Indexed
JPEGTables
OPIProxy
JPEGProc
JpegIFOffset
JpegIFByteCount
JpegRestartInterval
JpegLosslessPredictors
JpegPointTransforms
JpegQTables
JpegDCTables
JpegACTables
YCbCrCoefficients
YCbCrSubSampling
YCbCrPositioning
ReferenceBlackWhite
XMLPacket
RelatedImageFileFormat
RelatedImageWidth
RelatedImageLength
Rating
RatingPercent
ImageID
CFARepeatPatternDim
CFAPattern
BatteryLevel
Copyright
ExposureTime
FNumber
IPTCNAA
ImageResources
ExifOffset
InterColorProfile
ExposureProgram
SpectralSensitivity
GPSInfo
ISOSpeedRatings
OECF
Interlace
TimeZoneOffset
SelfTimerMode
SensitivityType
StandardOutputSensitivity
RecommendedExposureIndex
ISOSpeed
ISOSpeedLatitudeyyy
ISOSpeedLatitudezzz
ExifVersion
DateTimeOriginal
DateTimeDigitized
OffsetTime
OffsetTimeOriginal
OffsetTimeDigitized
ComponentsConfiguration
CompressedBitsPerPixel
ShutterSpeedValue
ApertureValue
BrightnessValue
ExposureBiasValue
MaxApertureValue
SubjectDistance
MeteringMode
LightSource
Flash
FocalLength
FlashEnergy
SpatialFrequencyResponse
Noise
ImageNumber
SecurityClassification
ImageHistory
SubjectLocation
ExposureIndex
TIFF/EPStandardID
MakerNote
UserComment
SubsecTime
SubsecTimeOriginal
SubsecTimeDigitized
AmbientTemperature
Humidity
Pressure
WaterDepth
Acceleration
CameraElevationAngle
XPTitle
XPComment
XPAuthor
XPKeywords
XPSubject
FlashPixVersion
ColorSpace
ExifImageWidth
ExifImageHeight
RelatedSoundFile
ExifInteroperabilityOffset
FlashEnergy
SpatialFrequencyResponse
FocalPlaneXResolution
FocalPlaneYResolution
FocalPlaneResolutionUnit
SubjectLocation
ExposureIndex
SensingMethod
FileSource
SceneType
CFAPattern
CustomRendered
ExposureMode
WhiteBalance
DigitalZoomRatio
FocalLengthIn35mmFilm
SceneCaptureType
GainControl
Contrast
Saturation
Sharpness
DeviceSettingDescription
SubjectDistanceRange
ImageUniqueID
CameraOwnerName
BodySerialNumber
LensSpecification
LensMake
LensModel
LensSerialNumber
CompositeImage
CompositeImageCount
CompositeImageExposureTimes
Gamma
PrintImageMatching
DNGVersion
DNGBackwardVersion
UniqueCameraModel
LocalizedCameraModel
CFAPlaneColor
CFALayout
LinearizationTable
BlackLevelRepeatDim
BlackLevel
BlackLevelDeltaH
BlackLevelDeltaV
WhiteLevel
DefaultScale
DefaultCropOrigin
DefaultCropSize
ColorMatrix1
ColorMatrix2
CameraCalibration1
CameraCalibration2
ReductionMatrix1
ReductionMatrix2
AnalogBalance
AsShotNeutral
AsShotWhiteXY
BaselineExposure
BaselineNoise
BaselineSharpness
BayerGreenSplit
LinearResponseLimit
CameraSerialNumber
LensInfo
ChromaBlurRadius
AntiAliasStrength
ShadowScale
DNGPrivateData
MakerNoteSafety
CalibrationIlluminant1
CalibrationIlluminant2
BestQualityScale
RawDataUniqueID
OriginalRawFileName
OriginalRawFileData
ActiveArea
MaskedAreas
AsShotICCProfile
AsShotPreProfileMatrix
CurrentICCProfile
CurrentPreProfileMatrix
ColorimetricReference
CameraCalibrationSignature
ProfileCalibrationSignature
AsShotProfileName
NoiseReductionApplied
ProfileName
ProfileHueSatMapDims
ProfileHueSatMapData1
ProfileHueSatMapData2
ProfileToneCurve
ProfileEmbedPolicy
ProfileCopyright
ForwardMatrix1
ForwardMatrix2
PreviewApplicationName
PreviewApplicationVersion
PreviewSettingsName
PreviewSettingsDigest
PreviewColorSpace
PreviewDateTime
RawImageDigest
OriginalRawFileDigest
SubTileBlockSize
RowInterleaveFactor
ProfileLookTableDims
ProfileLookTableData
OpcodeList1
OpcodeList2
OpcodeList3
NoiseProfile
```