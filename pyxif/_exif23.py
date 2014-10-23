

TAGS = {
    "Image":{
        256: {'name': 'ImageWidth', 'type':'Short/Long', 'length':1},
        257: {'name': 'ImageLength', 'type':'Short/Long', 'length':1},
        258: {'name': 'BitsPerSample', 'type':'Short', 'length':3},
        259: {'name': 'Compression', 'type':'Short', 'length':1},
        262: {'name': 'PhotometricInterpretation', 'type':'Short', 'length':1},
        270: {'name': 'ImageDescription', 'type':'Ascii', 'length':-1},
        271: {'name': 'Make', 'type':'Ascii', 'length':-1},
        272: {'name': 'Model', 'type':'Ascii', 'length':-1},
        273: {'name': 'StripOffsets', 'type':'Short/Long', 'length':1},
        274: {'name': 'Orientation', 'type':'Short', 'length':1},
        277: {'name': 'SamplesPerPixel', 'type':'Short', 'length':1},
        278: {'name': 'RowsPerStrip', 'type':'Short/Long', 'length':1},
        279: {'name': 'StripByteCounts', 'type':'Short/Long', 'length':-1},
        282: {'name': 'XResolution', 'type':'Rational', 'length':1},
        283: {'name': 'YResolution', 'type':'Rational', 'length':1},
        284: {'name': 'PlanarConfiguration', 'type':'Short', 'length':1},
        296: {'name': 'ResolutionUnit', 'type':'Short', 'length':1},
        301: {'name': 'TransferFunction', 'type':'Short', 'length':3*256},
        305: {'name': 'Software', 'type':'Ascii', 'length':-1},
        306: {'name': 'DateTime', 'type':'Ascii', 'length':20},
        315: {'name': 'Artist', 'type':'Ascii', 'length':-1},
        318: {'name': 'WhitePoint', 'type':'Rational', 'length':2},
        319: {'name': 'PrimaryChromaticities', 'type':'Rational', 'length':6},
        513: {'name': 'JPEGInterchangeFormat', 'type':'Long', 'length':1},
        514: {'name': 'JPEGInterchangeFormatLength', 'type':'Long', 'length':1},
        529: {'name': 'YCbCrCoefficients', 'type':'Rational', 'length':3},
        530: {'name': 'YCbCrSubSampling', 'type':'Short', 'length':2},
        531: {'name': 'YCbCrPositioning', 'type':'Short', 'length':1},
        532: {'name': 'ReferenceBlackWhite', 'type':'Rational', 'length':6},
        33432: {'name': 'Copyright', 'type':'Ascii', 'length':-1},
        34665: {'name': 'Exif IFD Pointer', 'type':'Long', 'length':1},
        34853: {'name': 'GPSInfo IFD Pointer', 'type':'Long', 'length':1},
    },
    "Photo":{
        33434: {'name': 'ExposureTime', 'type':'Rational', 'length':1},
        33437: {'name': 'FNumber', 'type':'Rational', 'length':1},
        34850: {'name': 'ExposureProgram', 'type':'Short', 'length':1},
        34852: {'name': 'SpectralSensitivity', 'type':'Ascii', 'length':-1},
        34855: {'name': 'PhotographicSensitivity', 'type':'Short', 'length':-1},
        34856: {'name': 'OECF', 'type':'Undefined', 'length':-1},
        34864: {'name': 'SensitivityType', 'type':'Short', 'length':1},
        34865: {'name': 'StandardOutputSensitivity', 'type':'Long', 'length':1},
        34866: {'name': 'RecommendedExposureIndex', 'type':'Long', 'length':1},
        34867: {'name': 'ISOSpeed', 'type':'Long', 'length':1},
        34868: {'name': 'ISOSpeedLatitudeyyy', 'type':'Long', 'length':1},
        34869: {'name': 'ISOSpeedLatitudezzz', 'type':'Long', 'length':1},
        36864: {'name': 'ExifVersion', 'type':'Undefined', 'length':4},
        36867: {'name': 'DateTimeOriginal', 'type':'Ascii', 'length':20},
        36868: {'name': 'DateTimeDigitized', 'type':'Ascii', 'length':20},
        37121: {'name': 'ComponentsConfiguration', 'type':'Undefined', 'length':4},
        37122: {'name': 'CompressedBitsPerPixel', 'type':'Rational', 'length':1},
        37377: {'name': 'ShutterSpeedValue', 'type':'SRational', 'length':1},
        37378: {'name': 'ApertureValue', 'type':'Rational', 'length':1},
        37379: {'name': 'BrightnessValue', 'type':'SRational', 'length':1},
        37380: {'name': 'ExposureBiasValue', 'type':'SRational', 'length':1},
        37381: {'name': 'MaxApertureValue', 'type':'Rational', 'length':1},
        37382: {'name': 'SubjectDistance', 'type':'Rational', 'length':1},
        37383: {'name': 'MeteringMode', 'type':'Short', 'length':1},
        37384: {'name': 'LightSource', 'type':'Short', 'length':1},
        37385: {'name': 'Flash', 'type':'Short', 'length':1},
        37386: {'name': 'FocalLength', 'type':'Rational', 'length':1},
        37396: {'name': 'SubjectArea', 'type':'Short', 'length':-1},
        37500: {'name': 'MakerNote', 'type':'Undefined', 'length':-1},
        37510: {'name': 'UserComment', 'type':'Undefined', 'length':-1},
        37520: {'name': 'SubSecTime', 'type':'Ascii', 'length':-1},
        37521: {'name': 'SubSecTimeOriginal', 'type':'Ascii', 'length':-1},
        37522: {'name': 'SubSecTimeDigitized', 'type':'Ascii', 'length':-1},
        40960: {'name': 'FlashpixVersion', 'type':'Undefined', 'length':4},
        40961: {'name': 'ColorSpace', 'type':'Short', 'length':1},
        40962: {'name': 'PixelXDimension', 'type':'Short/Long', 'length':1},
        40963: {'name': 'PixelYDimension', 'type':'Short/Long', 'length':1},
        40964: {'name': 'RelatedSoundFile', 'type':'Ascii', 'length':13},
        40965: {'name': 'Interoperability IFD Pointer', 'type':'Long', 'length':1},
        41483: {'name': 'FlashEnergy', 'type':'Rational', 'length':1},
        41484: {'name': 'SpatialFrequencyResponse', 'type':'Undefined', 'length':-1},
        41486: {'name': 'FocalPlaneXResolution', 'type':'Rational', 'length':1},
        41487: {'name': 'FocalPlaneYResolution', 'type':'Rational', 'length':1},
        41488: {'name': 'FocalPlaneResolutionUnit', 'type':'Short', 'length':1},
        41492: {'name': 'SubjectLocation', 'type':'Short', 'length':2},
        41493: {'name': 'ExposureIndex', 'type':'Rational', 'length':1},
        41495: {'name': 'SensingMethod', 'type':'Short', 'length':1},
        41728: {'name': 'FileSource', 'type':'Undefined', 'length':1},
        41729: {'name': 'SceneType', 'type':'Undefined', 'length':1},
        41730: {'name': 'CFAPattern', 'type':'Undefined', 'length':-1},
        41985: {'name': 'CustomRendered', 'type':'Short', 'length':1},
        41986: {'name': 'ExposureMode', 'type':'Short', 'length':1},
        41987: {'name': 'WhiteBalance', 'type':'Short', 'length':1},
        41988: {'name': 'DigitalZoomRatio', 'type':'Rational', 'length':1},
        41989: {'name': 'FocalLengthIn35mmFilm', 'type':'Short', 'length':1},
        41990: {'name': 'SceneCaptureType', 'type':'Short', 'length':1},
        41991: {'name': 'GainControl', 'type':'Short', 'length':1},
        41992: {'name': 'Contrast', 'type':'Short', 'length':1},
        41993: {'name': 'Saturation', 'type':'Short', 'length':1},
        41994: {'name': 'Sharpness', 'type':'Short', 'length':1},
        41995: {'name': 'DeviceSettingDescription', 'type':'Undefined', 'length':-1},
        41996: {'name': 'SubjectDistanceRange', 'type':'Short', 'length':1},
        42016: {'name': 'ImageUniqueID', 'type':'Ascii', 'length':33},
        42032: {'name': 'CameraOwnerName', 'type':'Ascii', 'length':-1},
        42033: {'name': 'BodySerialNumber', 'type':'Ascii', 'length':-1},
        42034: {'name': 'LensSpecification', 'type':'Rational', 'length':4},
        42035: {'name': 'LensMake', 'type':'Ascii', 'length':-1},
        42036: {'name': 'LensModel', 'type':'Ascii', 'length':-1},
        42037: {'name': 'LensSerialNumber', 'type':'Ascii', 'length':-1},
        42240: {'name': 'Gamma', 'type':'Rational', 'length':1},
    },
    "GPSInfo":{
        0: {'name': 'GPSVersionID', 'type':'Byte', 'length':4},
        1: {'name': 'GPSLatitudeRef', 'type':'Ascii', 'length':2},
        2: {'name': 'GPSLatitude', 'type':'Rational', 'length':3},
        3: {'name': 'GPSLongitudeRef', 'type':'Ascii', 'length':2},
        4: {'name': 'GPSLongitude', 'type':'Rational', 'length':3},
        5: {'name': 'GPSAltitudeRef', 'type':'Byte', 'length':1},
        6: {'name': 'GPSAltitude', 'type':'Rational', 'length':1},
        7: {'name': 'GPSTimeStamp', 'type':'Rational', 'length':3},
        8: {'name': 'GPSSatellites', 'type':'Ascii', 'length':-1},
        9: {'name': 'GPSStatus', 'type':'Ascii', 'length':2},
        10: {'name': 'GPSMeasureMode', 'type':'Ascii', 'length':2},
        11: {'name': 'GPSDOP', 'type':'Rational', 'length':1},
        12: {'name': 'GPSSpeedRef', 'type':'Ascii', 'length':2},
        13: {'name': 'GPSSpeed', 'type':'Rational', 'length':1},
        14: {'name': 'GPSTrackRef', 'type':'Ascii', 'length':2},
        15: {'name': 'GPSTrack', 'type':'Rational', 'length':1},
        16: {'name': 'GPSImgDirectionRef', 'type':'Ascii', 'length':2},
        17: {'name': 'GPSImgDirection', 'type':'Rational', 'length':1},
        18: {'name': 'GPSMapDatum', 'type':'Ascii', 'length':-1},
        19: {'name': 'GPSDestLatitudeRef', 'type':'Ascii', 'length':2},
        20: {'name': 'GPSDestLatitude', 'type':'Rational', 'length':3},
        21: {'name': 'GPSDestLongitudeRef', 'type':'Ascii', 'length':2},
        22: {'name': 'GPSDestLongitude', 'type':'Rational', 'length':3},
        23: {'name': 'GPSDestBearingRef', 'type':'Ascii', 'length':2},
        24: {'name': 'GPSDestBearing', 'type':'Rational', 'length':1},
        25: {'name': 'GPSDestDistanceRef', 'type':'Ascii', 'length':2},
        26: {'name': 'GPSDestDistance', 'type':'Rational', 'length':1},
        27: {'name': 'GPSProcessingMethod', 'type':'Undefined', 'length':-1},
        28: {'name': 'GPSAreaInformation', 'type':'Undefined', 'length':-1},
        29: {'name': 'GPSDateStamp', 'type':'Ascii', 'length':11},
        30: {'name': 'GPSDifferential', 'type':'Short', 'length':1},
        31: {'name': 'GPSHPositioningError', 'type':'Rational', 'length':1},
    },
}


class ImageGroup:
    ImageWidth = 256
    ImageLength = 257
    BitsPerSample = 258
    Compression = 259
    PhotometricInterpretation = 262
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
    ResolutionUnit = 296
    TransferFunction = 301
    Software = 305
    DateTime = 306
    Artist = 315
    WhitePoint = 318
    PrimaryChromaticities = 319
    JPEGInterchangeFormat = 513
    JPEGInterchangeFormatLength = 514
    YCbCrCoefficients = 529
    YCbCrSubSampling = 530
    YCbCrPositioning = 531
    ReferenceBlackWhite = 532
    Copyright = 33432
    ExifIFDPointer = 34665
    GPSInfoIFDPointer = 34853


class PhotoGroup:
    ExposureTime = 33434
    FNumber = 33437
    ExposureProgram = 34850
    SpectralSensitivity = 34852
    PhotographicSensitivity = 34855
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
    Gamma = 42240


class GPSInfoGroup:
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
    GPSHPositioningError = 31