# Byte: int
# Ascii: str
# Short: int
# Long: Long
# Rational: (long, Long)
# Undefined: str
# SLong: long
# SRational: (Long, Long)

import io
import struct

from _common import *

TAGS = {
 'GPSInfo': {0: {'group': 'GPSVersionID', 'type': 'Byte'},
             1: {'group': 'GPSLatitudeRef', 'type': 'Ascii'},
             2: {'group': 'GPSLatitude', 'type': 'Rational'},
             3: {'group': 'GPSLongitudeRef', 'type': 'Ascii'},
             4: {'group': 'GPSLongitude', 'type': 'Rational'},
             5: {'group': 'GPSAltitudeRef', 'type': 'Byte'},
             6: {'group': 'GPSAltitude', 'type': 'Rational'},
             7: {'group': 'GPSTimeStamp', 'type': 'Rational'},
             8: {'group': 'GPSSatellites', 'type': 'Ascii'},
             9: {'group': 'GPSStatus', 'type': 'Ascii'},
             10: {'group': 'GPSMeasureMode', 'type': 'Ascii'},
             11: {'group': 'GPSDOP', 'type': 'Rational'},
             12: {'group': 'GPSSpeedRef', 'type': 'Ascii'},
             13: {'group': 'GPSSpeed', 'type': 'Rational'},
             14: {'group': 'GPSTrackRef', 'type': 'Ascii'},
             15: {'group': 'GPSTrack', 'type': 'Rational'},
             16: {'group': 'GPSImgDirectionRef', 'type': 'Ascii'},
             17: {'group': 'GPSImgDirection', 'type': 'Rational'},
             18: {'group': 'GPSMapDatum', 'type': 'Ascii'},
             19: {'group': 'GPSDestLatitudeRef', 'type': 'Ascii'},
             20: {'group': 'GPSDestLatitude', 'type': 'Rational'},
             21: {'group': 'GPSDestLongitudeRef', 'type': 'Ascii'},
             22: {'group': 'GPSDestLongitude', 'type': 'Rational'},
             23: {'group': 'GPSDestBearingRef', 'type': 'Ascii'},
             24: {'group': 'GPSDestBearing', 'type': 'Rational'},
             25: {'group': 'GPSDestDistanceRef', 'type': 'Ascii'},
             26: {'group': 'GPSDestDistance', 'type': 'Rational'},
             27: {'group': 'GPSProcessingMethod', 'type': 'Undefined'},
             28: {'group': 'GPSAreaInformation', 'type': 'Undefined'},
             29: {'group': 'GPSDateStamp', 'type': 'Ascii'},
             30: {'group': 'GPSDifferential', 'type': 'Short'}},
 'Image': {11: {'group': 'ProcessingSoftware', 'type': 'Ascii'},
           254: {'group': 'NewSubfileType', 'type': 'Long'},
           255: {'group': 'SubfileType', 'type': 'Short'},
           256: {'group': 'ImageWidth', 'type': 'Long'},
           257: {'group': 'ImageLength', 'type': 'Long'},
           258: {'group': 'BitsPerSample', 'type': 'Short'},
           259: {'group': 'Compression', 'type': 'Short'},
           262: {'group': 'PhotometricInterpretation', 'type': 'Short'},
           263: {'group': 'Threshholding', 'type': 'Short'},
           264: {'group': 'CellWidth', 'type': 'Short'},
           265: {'group': 'CellLength', 'type': 'Short'},
           266: {'group': 'FillOrder', 'type': 'Short'},
           269: {'group': 'DocumentName', 'type': 'Ascii'},
           270: {'group': 'ImageDescription', 'type': 'Ascii'},
           271: {'group': 'Make', 'type': 'Ascii'},
           272: {'group': 'Model', 'type': 'Ascii'},
           273: {'group': 'StripOffsets', 'type': 'Long'},
           274: {'group': 'Orientation', 'type': 'Short'},
           277: {'group': 'SamplesPerPixel', 'type': 'Short'},
           278: {'group': 'RowsPerStrip', 'type': 'Long'},
           279: {'group': 'StripByteCounts', 'type': 'Long'},
           282: {'group': 'XResolution', 'type': 'Rational'},
           283: {'group': 'YResolution', 'type': 'Rational'},
           284: {'group': 'PlanarConfiguration', 'type': 'Short'},
           290: {'group': 'GrayResponseUnit', 'type': 'Short'},
           291: {'group': 'GrayResponseCurve', 'type': 'Short'},
           292: {'group': 'T4Options', 'type': 'Long'},
           293: {'group': 'T6Options', 'type': 'Long'},
           296: {'group': 'ResolutionUnit', 'type': 'Short'},
           301: {'group': 'TransferFunction', 'type': 'Short'},
           305: {'group': 'Software', 'type': 'Ascii'},
           306: {'group': 'DateTime', 'type': 'Ascii'},
           315: {'group': 'Artist', 'type': 'Ascii'},
           316: {'group': 'HostComputer', 'type': 'Ascii'},
           317: {'group': 'Predictor', 'type': 'Short'},
           318: {'group': 'WhitePoint', 'type': 'Rational'},
           319: {'group': 'PrimaryChromaticities', 'type': 'Rational'},
           320: {'group': 'ColorMap', 'type': 'Short'},
           321: {'group': 'HalftoneHints', 'type': 'Short'},
           322: {'group': 'TileWidth', 'type': 'Short'},
           323: {'group': 'TileLength', 'type': 'Short'},
           324: {'group': 'TileOffsets', 'type': 'Short'},
           325: {'group': 'TileByteCounts', 'type': 'Short'},
           330: {'group': 'SubIFDs', 'type': 'Long'},
           332: {'group': 'InkSet', 'type': 'Short'},
           333: {'group': 'InkNames', 'type': 'Ascii'},
           334: {'group': 'NumberOfInks', 'type': 'Short'},
           336: {'group': 'DotRange', 'type': 'Byte'},
           337: {'group': 'TargetPrinter', 'type': 'Ascii'},
           338: {'group': 'ExtraSamples', 'type': 'Short'},
           339: {'group': 'SampleFormat', 'type': 'Short'},
           340: {'group': 'SMinSampleValue', 'type': 'Short'},
           341: {'group': 'SMaxSampleValue', 'type': 'Short'},
           342: {'group': 'TransferRange', 'type': 'Short'},
           343: {'group': 'ClipPath', 'type': 'Byte'},
           344: {'group': 'XClipPathUnits', 'type': 'Long'},
           345: {'group': 'YClipPathUnits', 'type': 'Long'},
           346: {'group': 'Indexed', 'type': 'Short'},
           347: {'group': 'JPEGTables', 'type': 'Undefined'},
           351: {'group': 'OPIProxy', 'type': 'Short'},
           512: {'group': 'JPEGProc', 'type': 'Long'},
           513: {'group': 'JPEGInterchangeFormat', 'type': 'Long'},
           514: {'group': 'JPEGInterchangeFormatLength', 'type': 'Long'},
           515: {'group': 'JPEGRestartInterval', 'type': 'Short'},
           517: {'group': 'JPEGLosslessPredictors', 'type': 'Short'},
           518: {'group': 'JPEGPointTransforms', 'type': 'Short'},
           519: {'group': 'JPEGQTables', 'type': 'Long'},
           520: {'group': 'JPEGDCTables', 'type': 'Long'},
           521: {'group': 'JPEGACTables', 'type': 'Long'},
           529: {'group': 'YCbCrCoefficients', 'type': 'Rational'},
           530: {'group': 'YCbCrSubSampling', 'type': 'Short'},
           531: {'group': 'YCbCrPositioning', 'type': 'Short'},
           532: {'group': 'ReferenceBlackWhite', 'type': 'Rational'},
           700: {'group': 'XMLPacket', 'type': 'Byte'},
           18246: {'group': 'Rating', 'type': 'Short'},
           18249: {'group': 'RatingPercent', 'type': 'Short'},
           32781: {'group': 'ImageID', 'type': 'Ascii'},
           33421: {'group': 'CFARepeatPatternDim', 'type': 'Short'},
           33422: {'group': 'CFAPattern', 'type': 'Byte'},
           33423: {'group': 'BatteryLevel', 'type': 'Rational'},
           33432: {'group': 'Copyright', 'type': 'Ascii'},
           33434: {'group': 'ExposureTime', 'type': 'Rational'},
           34377: {'group': 'ImageResources', 'type': 'Byte'},
           34665: {'group': 'ExifTag', 'type': 'Long'},
           34675: {'group': 'InterColorProfile', 'type': 'Undefined'},
           34853: {'group': 'GPSTag', 'type': 'Long'},
           34857: {'group': 'Interlace', 'type': 'Short'},
           34858: {'group': 'TimeZoneOffset', 'type': 'Long'},
           34859: {'group': 'SelfTimerMode', 'type': 'Short'},
           37387: {'group': 'FlashEnergy', 'type': 'Rational'},
           37388: {'group': 'SpatialFrequencyResponse', 'type': 'Undefined'},
           37389: {'group': 'Noise', 'type': 'Undefined'},
           37390: {'group': 'FocalPlaneXResolution', 'type': 'Rational'},
           37391: {'group': 'FocalPlaneYResolution', 'type': 'Rational'},
           37392: {'group': 'FocalPlaneResolutionUnit', 'type': 'Short'},
           37393: {'group': 'ImageNumber', 'type': 'Long'},
           37394: {'group': 'SecurityClassification', 'type': 'Ascii'},
           37395: {'group': 'ImageHistory', 'type': 'Ascii'},
           37397: {'group': 'ExposureIndex', 'type': 'Rational'},
           37398: {'group': 'TIFFEPStandardID', 'type': 'Byte'},
           37399: {'group': 'SensingMethod', 'type': 'Short'},
           40091: {'group': 'XPTitle', 'type': 'Byte'},
           40092: {'group': 'XPComment', 'type': 'Byte'},
           40093: {'group': 'XPAuthor', 'type': 'Byte'},
           40094: {'group': 'XPKeywords', 'type': 'Byte'},
           40095: {'group': 'XPSubject', 'type': 'Byte'},
           50341: {'group': 'PrintImageMatching', 'type': 'Undefined'},
           50706: {'group': 'DNGVersion', 'type': 'Byte'},
           50707: {'group': 'DNGBackwardVersion', 'type': 'Byte'},
           50708: {'group': 'UniqueCameraModel', 'type': 'Ascii'},
           50709: {'group': 'LocalizedCameraModel', 'type': 'Byte'},
           50710: {'group': 'CFAPlaneColor', 'type': 'Byte'},
           50711: {'group': 'CFALayout', 'type': 'Short'},
           50712: {'group': 'LinearizationTable', 'type': 'Short'},
           50713: {'group': 'BlackLevelRepeatDim', 'type': 'Short'},
           50714: {'group': 'BlackLevel', 'type': 'Rational'},
           50715: {'group': 'BlackLevelDeltaH', 'type': 'SRational'},
           50716: {'group': 'BlackLevelDeltaV', 'type': 'SRational'},
           50717: {'group': 'WhiteLevel', 'type': 'Short'},
           50718: {'group': 'DefaultScale', 'type': 'Rational'},
           50719: {'group': 'DefaultCropOrigin', 'type': 'Short'},
           50720: {'group': 'DefaultCropSize', 'type': 'Short'},
           50721: {'group': 'ColorMatrix1', 'type': 'SRational'},
           50722: {'group': 'ColorMatrix2', 'type': 'SRational'},
           50723: {'group': 'CameraCalibration1', 'type': 'SRational'},
           50724: {'group': 'CameraCalibration2', 'type': 'SRational'},
           50725: {'group': 'ReductionMatrix1', 'type': 'SRational'},
           50726: {'group': 'ReductionMatrix2', 'type': 'SRational'},
           50727: {'group': 'AnalogBalance', 'type': 'Rational'},
           50728: {'group': 'AsShotNeutral', 'type': 'Short'},
           50729: {'group': 'AsShotWhiteXY', 'type': 'Rational'},
           50730: {'group': 'BaselineExposure', 'type': 'SRational'},
           50731: {'group': 'BaselineNoise', 'type': 'Rational'},
           50732: {'group': 'BaselineSharpness', 'type': 'Rational'},
           50733: {'group': 'BayerGreenSplit', 'type': 'Long'},
           50734: {'group': 'LinearResponseLimit', 'type': 'Rational'},
           50735: {'group': 'CameraSerialNumber', 'type': 'Ascii'},
           50736: {'group': 'LensInfo', 'type': 'Rational'},
           50737: {'group': 'ChromaBlurRadius', 'type': 'Rational'},
           50738: {'group': 'AntiAliasStrength', 'type': 'Rational'},
           50739: {'group': 'ShadowScale', 'type': 'SRational'},
           50740: {'group': 'DNGPrivateData', 'type': 'Byte'},
           50741: {'group': 'MakerNoteSafety', 'type': 'Short'},
           50778: {'group': 'CalibrationIlluminant1', 'type': 'Short'},
           50779: {'group': 'CalibrationIlluminant2', 'type': 'Short'},
           50780: {'group': 'BestQualityScale', 'type': 'Rational'},
           50781: {'group': 'RawDataUniqueID', 'type': 'Byte'},
           50827: {'group': 'OriginalRawFileName', 'type': 'Byte'},
           50828: {'group': 'OriginalRawFileData', 'type': 'Undefined'},
           50829: {'group': 'ActiveArea', 'type': 'Short'},
           50830: {'group': 'MaskedAreas', 'type': 'Short'},
           50831: {'group': 'AsShotICCProfile', 'type': 'Undefined'},
           50832: {'group': 'AsShotPreProfileMatrix', 'type': 'SRational'},
           50833: {'group': 'CurrentICCProfile', 'type': 'Undefined'},
           50834: {'group': 'CurrentPreProfileMatrix', 'type': 'SRational'},
           50879: {'group': 'ColorimetricReference', 'type': 'Short'},
           50931: {'group': 'CameraCalibrationSignature', 'type': 'Byte'},
           50932: {'group': 'ProfileCalibrationSignature', 'type': 'Byte'},
           50934: {'group': 'AsShotProfileName', 'type': 'Byte'},
           50935: {'group': 'NoiseReductionApplied', 'type': 'Rational'},
           50936: {'group': 'ProfileName', 'type': 'Byte'},
           50937: {'group': 'ProfileHueSatMapDims', 'type': 'Long'},
           50938: {'group': 'ProfileHueSatMapData1', 'type': 'Float'},
           50939: {'group': 'ProfileHueSatMapData2', 'type': 'Float'},
           50940: {'group': 'ProfileToneCurve', 'type': 'Float'},
           50941: {'group': 'ProfileEmbedPolicy', 'type': 'Long'},
           50942: {'group': 'ProfileCopyright', 'type': 'Byte'},
           50964: {'group': 'ForwardMatrix1', 'type': 'SRational'},
           50965: {'group': 'ForwardMatrix2', 'type': 'SRational'},
           50966: {'group': 'PreviewApplicationName', 'type': 'Byte'},
           50967: {'group': 'PreviewApplicationVersion', 'type': 'Byte'},
           50968: {'group': 'PreviewSettingsName', 'type': 'Byte'},
           50969: {'group': 'PreviewSettingsDigest', 'type': 'Byte'},
           50970: {'group': 'PreviewColorSpace', 'type': 'Long'},
           50971: {'group': 'PreviewDateTime', 'type': 'Ascii'},
           50972: {'group': 'RawImageDigest', 'type': 'Undefined'},
           50973: {'group': 'OriginalRawFileDigest', 'type': 'Undefined'},
           50974: {'group': 'SubTileBlockSize', 'type': 'Long'},
           50975: {'group': 'RowInterleaveFactor', 'type': 'Long'},
           50981: {'group': 'ProfileLookTableDims', 'type': 'Long'},
           50982: {'group': 'ProfileLookTableData', 'type': 'Float'},
           51008: {'group': 'OpcodeList1', 'type': 'Undefined'},
           51009: {'group': 'OpcodeList2', 'type': 'Undefined'},
           51022: {'group': 'OpcodeList3', 'type': 'Undefined'},
           51041: {'group': 'NoiseProfile', 'type': 'Double'}},
 'Photo': {33434: {'group': 'ExposureTime', 'type': 'Rational'},
           33437: {'group': 'FNumber', 'type': 'Rational'},
           34850: {'group': 'ExposureProgram', 'type': 'Short'},
           34852: {'group': 'SpectralSensitivity', 'type': 'Ascii'},
           34855: {'group': 'ISOSpeedRatings', 'type': 'Short'},
           34856: {'group': 'OECF', 'type': 'Undefined'},
           34864: {'group': 'SensitivityType', 'type': 'Short'},
           34865: {'group': 'StandardOutputSensitivity', 'type': 'Long'},
           34866: {'group': 'RecommendedExposureIndex', 'type': 'Long'},
           34867: {'group': 'ISOSpeed', 'type': 'Long'},
           34868: {'group': 'ISOSpeedLatitudeyyy', 'type': 'Long'},
           34869: {'group': 'ISOSpeedLatitudezzz', 'type': 'Long'},
           36864: {'group': 'ExifVersion', 'type': 'Undefined'},
           36867: {'group': 'DateTimeOriginal', 'type': 'Ascii'},
           36868: {'group': 'DateTimeDigitized', 'type': 'Ascii'},
           37121: {'group': 'ComponentsConfiguration', 'type': 'Undefined'},
           37122: {'group': 'CompressedBitsPerPixel', 'type': 'Rational'},
           37377: {'group': 'ShutterSpeedValue', 'type': 'SRational'},
           37378: {'group': 'ApertureValue', 'type': 'Rational'},
           37379: {'group': 'BrightnessValue', 'type': 'SRational'},
           37380: {'group': 'ExposureBiasValue', 'type': 'SRational'},
           37381: {'group': 'MaxApertureValue', 'type': 'Rational'},
           37382: {'group': 'SubjectDistance', 'type': 'Rational'},
           37383: {'group': 'MeteringMode', 'type': 'Short'},
           37384: {'group': 'LightSource', 'type': 'Short'},
           37385: {'group': 'Flash', 'type': 'Short'},
           37386: {'group': 'FocalLength', 'type': 'Rational'},
           37396: {'group': 'SubjectArea', 'type': 'Short'},
           37500: {'group': 'MakerNote', 'type': 'Undefined'},
           37510: {'group': 'UserComment', 'type': 'Comment'},
           37520: {'group': 'SubSecTime', 'type': 'Ascii'},
           37521: {'group': 'SubSecTimeOriginal', 'type': 'Ascii'},
           37522: {'group': 'SubSecTimeDigitized', 'type': 'Ascii'},
           40960: {'group': 'FlashpixVersion', 'type': 'Undefined'},
           40961: {'group': 'ColorSpace', 'type': 'Short'},
           40962: {'group': 'PixelXDimension', 'type': 'Long'},
           40963: {'group': 'PixelYDimension', 'type': 'Long'},
           40964: {'group': 'RelatedSoundFile', 'type': 'Ascii'},
           40965: {'group': 'InteroperabilityTag', 'type': 'Long'},
           41483: {'group': 'FlashEnergy', 'type': 'Rational'},
           41484: {'group': 'SpatialFrequencyResponse', 'type': 'Undefined'},
           41486: {'group': 'FocalPlaneXResolution', 'type': 'Rational'},
           41487: {'group': 'FocalPlaneYResolution', 'type': 'Rational'},
           41488: {'group': 'FocalPlaneResolutionUnit', 'type': 'Short'},
           41492: {'group': 'SubjectLocation', 'type': 'Short'},
           41493: {'group': 'ExposureIndex', 'type': 'Rational'},
           41495: {'group': 'SensingMethod', 'type': 'Short'},
           41728: {'group': 'FileSource', 'type': 'Undefined'},
           41729: {'group': 'SceneType', 'type': 'Undefined'},
           41730: {'group': 'CFAPattern', 'type': 'Undefined'},
           41985: {'group': 'CustomRendered', 'type': 'Short'},
           41986: {'group': 'ExposureMode', 'type': 'Short'},
           41987: {'group': 'WhiteBalance', 'type': 'Short'},
           41988: {'group': 'DigitalZoomRatio', 'type': 'Rational'},
           41989: {'group': 'FocalLengthIn35mmFilm', 'type': 'Short'},
           41990: {'group': 'SceneCaptureType', 'type': 'Short'},
           41991: {'group': 'GainControl', 'type': 'Short'},
           41992: {'group': 'Contrast', 'type': 'Short'},
           41993: {'group': 'Saturation', 'type': 'Short'},
           41994: {'group': 'Sharpness', 'type': 'Short'},
           41995: {'group': 'DeviceSettingDescription', 'type': 'Undefined'},
           41996: {'group': 'SubjectDistanceRange', 'type': 'Short'},
           42016: {'group': 'ImageUniqueID', 'type': 'Ascii'},
           42032: {'group': 'CameraOwnerName', 'type': 'Ascii'},
           42033: {'group': 'BodySerialNumber', 'type': 'Ascii'},
           42034: {'group': 'LensSpecification', 'type': 'Rational'},
           42035: {'group': 'LensMake', 'type': 'Ascii'},
           42036: {'group': 'LensModel', 'type': 'Ascii'},
           42037: {'group': 'LensSerialNumber', 'type': 'Ascii'}}}

class ImageGroup:
    """Exif tag number reference"""
    ProcessingSoftware = 11
    NewSubfileType = 254
    SubfileType = 255
    ImageWidth = 256
    ImageLength = 257
    BitsPerSample = 258
    Compression = 259
    PhotometricInterpretation = 262
    Threshholding = 263
    CellWidth = 264
    CellLength = 265
    FillOrder = 266
    DocumentName = 269
    ImageDescription = 270
    Make = 271
    Model = 272
    StripOffsets = 273
    Orientation = 274
    SamplesPerPixel = 277
    RowsPerStrip = 278
    StripByteCounts = 279
    XResolution = 282
    YResolution = 283
    PlanarConfiguration = 284
    GrayResponseUnit = 290
    GrayResponseCurve = 291
    T4Options = 292
    T6Options = 293
    ResolutionUnit = 296
    TransferFunction = 301
    Software = 305
    DateTime = 306
    Artist = 315
    HostComputer = 316
    Predictor = 317
    WhitePoint = 318
    PrimaryChromaticities = 319
    ColorMap = 320
    HalftoneHints = 321
    TileWidth = 322
    TileLength = 323
    TileOffsets = 324
    TileByteCounts = 325
    SubIFDs = 330
    InkSet = 332
    InkNames = 333
    NumberOfInks = 334
    DotRange = 336
    TargetPrinter = 337
    ExtraSamples = 338
    SampleFormat = 339
    SMinSampleValue = 340
    SMaxSampleValue = 341
    TransferRange = 342
    ClipPath = 343
    XClipPathUnits = 344
    YClipPathUnits = 345
    Indexed = 346
    JPEGTables = 347
    OPIProxy = 351
    JPEGProc = 512
    JPEGInterchangeFormat = 513
    JPEGInterchangeFormatLength = 514
    JPEGRestartInterval = 515
    JPEGLosslessPredictors = 517
    JPEGPointTransforms = 518
    JPEGQTables = 519
    JPEGDCTables = 520
    JPEGACTables = 521
    YCbCrCoefficients = 529
    YCbCrSubSampling = 530
    YCbCrPositioning = 531
    ReferenceBlackWhite = 532
    XMLPacket = 700
    Rating = 18246
    RatingPercent = 18249
    ImageID = 32781
    CFARepeatPatternDim = 33421
    CFAPattern = 33422
    BatteryLevel = 33423
    Copyright = 33432
    ExposureTime = 33434
    ImageResources = 34377
    ExifTag = 34665
    InterColorProfile = 34675
    GPSTag = 34853
    Interlace = 34857
    TimeZoneOffset = 34858
    SelfTimerMode = 34859
    FlashEnergy = 37387
    SpatialFrequencyResponse = 37388
    Noise = 37389
    FocalPlaneXResolution = 37390
    FocalPlaneYResolution = 37391
    FocalPlaneResolutionUnit = 37392
    ImageNumber = 37393
    SecurityClassification = 37394
    ImageHistory = 37395
    ExposureIndex = 37397
    TIFFEPStandardID = 37398
    SensingMethod = 37399
    XPTitle = 40091
    XPComment = 40092
    XPAuthor = 40093
    XPKeywords = 40094
    XPSubject = 40095
    PrintImageMatching = 50341
    DNGVersion = 50706
    DNGBackwardVersion = 50707
    UniqueCameraModel = 50708
    LocalizedCameraModel = 50709
    CFAPlaneColor = 50710
    CFALayout = 50711
    LinearizationTable = 50712
    BlackLevelRepeatDim = 50713
    BlackLevel = 50714
    BlackLevelDeltaH = 50715
    BlackLevelDeltaV = 50716
    WhiteLevel = 50717
    DefaultScale = 50718
    DefaultCropOrigin = 50719
    DefaultCropSize = 50720
    ColorMatrix1 = 50721
    ColorMatrix2 = 50722
    CameraCalibration1 = 50723
    CameraCalibration2 = 50724
    ReductionMatrix1 = 50725
    ReductionMatrix2 = 50726
    AnalogBalance = 50727
    AsShotNeutral = 50728
    AsShotWhiteXY = 50729
    BaselineExposure = 50730
    BaselineNoise = 50731
    BaselineSharpness = 50732
    BayerGreenSplit = 50733
    LinearResponseLimit = 50734
    CameraSerialNumber = 50735
    LensInfo = 50736
    ChromaBlurRadius = 50737
    AntiAliasStrength = 50738
    ShadowScale = 50739
    DNGPrivateData = 50740
    MakerNoteSafety = 50741
    CalibrationIlluminant1 = 50778
    CalibrationIlluminant2 = 50779
    BestQualityScale = 50780
    RawDataUniqueID = 50781
    OriginalRawFileName = 50827
    OriginalRawFileData = 50828
    ActiveArea = 50829
    MaskedAreas = 50830
    AsShotICCProfile = 50831
    AsShotPreProfileMatrix = 50832
    CurrentICCProfile = 50833
    CurrentPreProfileMatrix = 50834
    ColorimetricReference = 50879
    CameraCalibrationSignature = 50931
    ProfileCalibrationSignature = 50932
    AsShotProfileName = 50934
    NoiseReductionApplied = 50935
    ProfileName = 50936
    ProfileHueSatMapDims = 50937
    ProfileHueSatMapData1 = 50938
    ProfileHueSatMapData2 = 50939
    ProfileToneCurve = 50940
    ProfileEmbedPolicy = 50941
    ProfileCopyright = 50942
    ForwardMatrix1 = 50964
    ForwardMatrix2 = 50965
    PreviewApplicationName = 50966
    PreviewApplicationVersion = 50967
    PreviewSettingsName = 50968
    PreviewSettingsDigest = 50969
    PreviewColorSpace = 50970
    PreviewDateTime = 50971
    RawImageDigest = 50972
    OriginalRawFileDigest = 50973
    SubTileBlockSize = 50974
    RowInterleaveFactor = 50975
    ProfileLookTableDims = 50981
    ProfileLookTableData = 50982
    OpcodeList1 = 51008
    OpcodeList2 = 51009
    OpcodeList3 = 51022
    NoiseProfile = 51041


class PhotoGroup:
    """Exif tag number reference"""
    ExposureTime = 33434
    FNumber = 33437
    ExposureProgram = 34850
    SpectralSensitivity = 34852
    ISOSpeedRatings = 34855
    OECF = 34856
    SensitivityType = 34864
    StandardOutputSensitivity = 34865
    RecommendedExposureIndex = 34866
    ISOSpeed = 34867
    ISOSpeedLatitudeyyy = 34868
    ISOSpeedLatitudezzz = 34869
    ExifVersion = 36864
    DateTimeOriginal = 36867
    DateTimeDigitized = 36868
    ComponentsConfiguration = 37121
    CompressedBitsPerPixel = 37122
    ShutterSpeedValue = 37377
    ApertureValue = 37378
    BrightnessValue = 37379
    ExposureBiasValue = 37380
    MaxApertureValue = 37381
    SubjectDistance = 37382
    MeteringMode = 37383
    LightSource = 37384
    Flash = 37385
    FocalLength = 37386
    SubjectArea = 37396
    MakerNote = 37500
    UserComment = 37510
    SubSecTime = 37520
    SubSecTimeOriginal = 37521
    SubSecTimeDigitized = 37522
    FlashpixVersion = 40960
    ColorSpace = 40961
    PixelXDimension = 40962
    PixelYDimension = 40963
    RelatedSoundFile = 40964
    InteroperabilityTag = 40965
    FlashEnergy = 41483
    SpatialFrequencyResponse = 41484
    FocalPlaneXResolution = 41486
    FocalPlaneYResolution = 41487
    FocalPlaneResolutionUnit = 41488
    SubjectLocation = 41492
    ExposureIndex = 41493
    SensingMethod = 41495
    FileSource = 41728
    SceneType = 41729
    CFAPattern = 41730
    CustomRendered = 41985
    ExposureMode = 41986
    WhiteBalance = 41987
    DigitalZoomRatio = 41988
    FocalLengthIn35mmFilm = 41989
    SceneCaptureType = 41990
    GainControl = 41991
    Contrast = 41992
    Saturation = 41993
    Sharpness = 41994
    DeviceSettingDescription = 41995
    SubjectDistanceRange = 41996
    ImageUniqueID = 42016
    CameraOwnerName = 42032
    BodySerialNumber = 42033
    LensSpecification = 42034
    LensMake = 42035
    LensModel = 42036
    LensSerialNumber = 42037


class GPSInfoGroup:
    """Exif tag number reference"""
    GPSVersionID = 0
    GPSLatitudeRef = 1
    GPSLatitude = 2
    GPSLongitudeRef = 3
    GPSLongitude = 4
    GPSAltitudeRef = 5
    GPSAltitude = 6
    GPSTimeStamp = 7
    GPSSatellites = 8
    GPSStatus = 9
    GPSMeasureMode = 10
    GPSDOP = 11
    GPSSpeedRef = 12
    GPSSpeed = 13
    GPSTrackRef = 14
    GPSTrack = 15
    GPSImgDirectionRef = 16
    GPSImgDirection = 17
    GPSMapDatum = 18
    GPSDestLatitudeRef = 19
    GPSDestLatitude = 20
    GPSDestLongitudeRef = 21
    GPSDestLongitude = 22
    GPSDestBearingRef = 23
    GPSDestBearing = 24
    GPSDestDistanceRef = 25
    GPSDestDistance = 26
    GPSProcessingMethod = 27
    GPSAreaInformation = 28
    GPSDateStamp = 29
    GPSDifferential = 30


TYPES = {
    "Byte": 1,
    "Ascii": 2,
    "Short": 3,
    "Long": 4,
    "Rational": 5,
    "Undefined": 7,
    "SLong": 9,
    "SRational": 10}


POINTERS = (34665, 34853)


LITTLE_ENDIAN = b"\x49\x49"


TIFF_HEADER_LENGTH = 8


class ExifReader(object):
    def __init__(self, data):
        if data[0:2] == b"\xff\xd8":
            pass
        elif data[0:6] == b"\x45\x78\x69\x66\x00\x00":
            self.exif_str = data
            return
        else:
            with open(data, 'rb') as f:
                data = f.read()

        segments = split_into_segments(data)
        exif = get_exif(segments)

        if exif:
            self.exif_str = exif[10:]
        else:
            self.exif_str = None

    def get_exif_ifd(self):
        endian = self.exif_str[0:2]
        self.little_endian = True if endian == LITTLE_ENDIAN else False
        self.endian_mark = "<" if endian == LITTLE_ENDIAN else ">"
        exif_dict = {}
        gps_dict = {}

        pointer = struct.unpack(self.endian_mark + "L", self.exif_str[4:8])[0]
        zeroth_dict = self.get_ifd_info(pointer)

        if 34665 in zeroth_dict:
            pointer = struct.unpack(self.endian_mark + "L", zeroth_dict[34665][2])[0]
            exif_dict = self.get_ifd_info(pointer)

        if 34853 in exif_dict:
            pointer = struct.unpack(self.endian_mark + "L", exif_dict[34853][2])[0]
            gps_dict = self.get_ifd_info(pointer)

        return zeroth_dict, exif_dict, gps_dict

    def get_ifd_info(self, pointer):
        ifd_dict = {}
        tag_count = struct.unpack(self.endian_mark + "H", self.exif_str[pointer: pointer+2])[0]
        offset = pointer + 2
        for x in range(tag_count):
            pointer = offset + 12 * x
            tag_code = struct.unpack(self.endian_mark + "H", self.exif_str[pointer: pointer+2])[0]
            value_type = struct.unpack(self.endian_mark + "H", self.exif_str[pointer + 2: pointer + 4])[0]
            value_num = struct.unpack(self.endian_mark + "L", self.exif_str[pointer + 4: pointer + 8])[0]
            value = self.exif_str[pointer+8: pointer+12]
            ifd_dict.update({tag_code:[value_type, value_num, value]})
        return ifd_dict

    def get_info(self, val):
        data = None

        if val[0] == 1: # BYTE
            data = int(val[2][0].encode("hex"), 16)
        elif val[0] == 2: # ASCII
            if val[1] > 4:
                pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
                data = self.exif_str[pointer: pointer+val[1]].split(b"\x00")[0]
            else:
                data = val[2][0: val[1]]
        elif val[0] == 3: # SHORT
            data = struct.unpack(self.endian_mark + "H", val[2][0:2])[0]
        elif val[0] == 4: # LONG
            data = struct.unpack(self.endian_mark + "L", val[2])[0]
        elif val[0] == 5: # RATIONAL
            pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
            data = (struct.unpack(self.endian_mark + "L", self.exif_str[pointer: pointer + 4])[0],
                    struct.unpack(self.endian_mark + "L", self.exif_str[pointer + 4: pointer + 8])[0])
        elif val[0] == 7: # UNDEFINED BYTES
            if val[1] > 4:
                pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
                data = self.exif_str[pointer: pointer+val[1]]
            else:
                data = val[2][0: val[1]]
        elif val[0] == 9: # SLONG
            data = struct.unpack(self.endian_mark + "l", val[2])[0]
        elif val[0] == 10: # SRATIONAL
            pointer = struct.unpack(self.endian_mark + "L", val[2])[0]
            data = (struct.unpack(self.endian_mark + "l", self.exif_str[pointer: pointer + 4])[0],
                    struct.unpack(self.endian_mark + "l", self.exif_str[pointer + 4: pointer + 8])[0])

        return data


def load(input_str):
    """converts JPEG or exif bytes to dicts"""
    exifReader = ExifReader(input_str)
    if exifReader.exif_str is None:
        return {}, {}, {}
    zeroth_ifd, exif_ifd, gps_ifd = exifReader.get_exif_ifd()
    zeroth_dict = {key: (TAGS["Image"][key]["group"], exifReader.get_info(zeroth_ifd[key]))
                   for key in zeroth_ifd if key in TAGS["Image"]}
    exif_dict = {key: (TAGS["Photo"][key]["group"], exifReader.get_info(exif_ifd[key]))
                 for key in exif_ifd if key in TAGS["Photo"]}
    gps_dict = {key: (TAGS["GPSInfo"][key]["group"], exifReader.get_info(gps_ifd[key]))
                for key in gps_ifd if key in TAGS["GPSInfo"]}

    return zeroth_dict, exif_dict, gps_dict


def dump(zeroth_ifd, exif_ifd={}, gps_ifd={}):
    """converts dict to exif bytes"""
    header = b"\x45\x78\x69\x66\x00\x00\x4d\x4d\x00\x2a\x00\x00\x00\x08"
    if len(exif_ifd):
        exif_bytes = dict_to_bytes(zeroth_ifd, "Image", 0, True)
        if len(gps_ifd):
            exif_bytes += dict_to_bytes(exif_ifd, "Photo", len(exif_bytes), True)
            exif_bytes += dict_to_bytes(gps_ifd, "GPSInfo", len(exif_bytes))
        else:
            exif_bytes += dict_to_bytes(exif_ifd, "Photo", len(exif_bytes))
    else:
        exif_bytes = dict_to_bytes(zeroth_ifd, "Image", 0)
    return header + exif_bytes


def dict_to_bytes(ifd_dict, group, ifd_offset, next_ifd=False):
    if next_ifd:
        if group == "Image":
            ifd_dict.update({34665: 1})
        elif group == "Photo":
            ifd_dict.update({34853: 1})

    tag_count = len(ifd_dict)
    entry_header = struct.pack(">H", tag_count)
    entries_length = 2 + tag_count * 12 + 4
    entries = b""
    values = b""

    for n, key in enumerate(ifd_dict):
        if key in POINTERS:
            pointer_key = key
            continue
        raw_value = ifd_dict[key]
        key_str = struct.pack(">H", key)
        value_type = TAGS[group][key]["type"]
        type_str = struct.pack(">H", TYPES[value_type])
        if value_type == "Byte":
            length = 1
            value_str = struct.pack('>I', raw_value)[3] + b"\x00" * 3
        elif value_type == "Short":
            length = 2
            value_str = struct.pack('>I', raw_value)[2:4] + b"\x00" * 2
        elif value_type == "Long":
            length = 4
            value_str = struct.pack('>I', raw_value)
        elif value_type == "SLong":
            length = 4
            value_str = struct.pack('>i', raw_value)
        elif value_type == "Ascii":
            raw_value = raw_value.encode()
            length = len(raw_value)
            if length > 4:
                if length % 4:
                    new_value = raw_value + b"\x00" * (4 - length % 4)
                    length = len(new_value)
                else:
                    new_value = raw_value
                offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
                value_str = struct.pack(">I", offset)
                values += new_value
            else:
                length = len(raw_value)
                value_str = raw_value + b"\x00" * (4 - length)
        elif value_type == "Rational":
            length = 1
            num, den = raw_value
            new_value = struct.pack(">L", num) + struct.pack(">L", den)
            offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
            value_str = struct.pack(">I", offset)
            values += new_value
        elif value_type == "SRational":
            length = 1
            num, den = raw_value
            new_value = struct.pack(">l", num) + struct.pack(">l", den)
            offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
            value_str = struct.pack(">I", offset)
            values += new_value
        elif value_type == "Undefined":
            raw_value = raw_value.encode()
            if len(raw_value) > 4:
                length = len(raw_value)
                if length % 4:
                    new_value = raw_value + b"\x00" * (4 - length % 4)
                    length = length + (4 - length % 4)
                else:
                    new_value = raw_value
                offset = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
                value_str = struct.pack(">I", offset)
                values += new_value
            else:
                length = len(raw_value)
                value_str = raw_value + b"\x00" * (4 - length)

        length_str = struct.pack(">I", length)
        entries += key_str + type_str + length_str + value_str

    if next_ifd:
        pointer_value = TIFF_HEADER_LENGTH + ifd_offset + entries_length + len(values)
        pointer_str = struct.pack(">I", pointer_value)
        if group == "Image":
            key = 34665
        elif group == "Photo":
            key = 34853
        key_str = struct.pack(">H", key)
        type_str = struct.pack(">H", TYPES["Long"])
        length_str = struct.pack(">I", 1)
        entries += key_str + type_str + length_str + pointer_str

    ifd_str = entry_header + entries + b"\x00\x00\x00\x00" + values
    return ifd_str
