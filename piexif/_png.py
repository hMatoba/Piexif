import struct
from zlib import crc32

PNG_HEADER = b"\x89PNG\x0d\x0a\x1a\x0a"
EXIF_MARKER = b"eXIf"

def split(data):
    if data[0:8] != PNG_HEADER:
        raise ValueError("Not PNG")

    start = 8
    pointer = start
    CHUNK_FOURCC_LENGTH = 4
    LENGTH_BYTES_LENGTH = 4
    CRC_LENGTH = 4
    file_size = len(data)
    END_SIGN = b"IEND"

    chunks = []
    while pointer + CHUNK_FOURCC_LENGTH + LENGTH_BYTES_LENGTH < file_size:
        data_length_bytes = data[pointer:pointer + LENGTH_BYTES_LENGTH]
        data_length = struct.unpack(">L", data_length_bytes)[0]
        pointer += LENGTH_BYTES_LENGTH

        fourcc = data[pointer:pointer + CHUNK_FOURCC_LENGTH]
        pointer += CHUNK_FOURCC_LENGTH

        chunk_data = data[pointer:pointer + data_length]
        pointer += data_length

        crc = data[pointer:pointer + CRC_LENGTH]
        pointer += CRC_LENGTH
        chunks.append({
            "fourcc":fourcc,
            "length_bytes":data_length_bytes,
            "data":chunk_data,
            "crc":crc
        })

        if fourcc == END_SIGN:
            break
        
    return chunks

def merge_chunks(chunks):
    merged = b"".join([chunk["length_bytes"] 
                       + chunk["fourcc"]
                       + chunk["data"]
                       + chunk["crc"]
                        for chunk in chunks])
    return merged


def get_exif(data):
    if data[0:8] != PNG_HEADER:
        raise ValueError("Not PNG")

    chunks = split(data)
    for chunk in chunks:
        if chunk["fourcc"] == EXIF_MARKER:
            return chunk["data"]
    return None


def insert_exif_into_chunks(chunks, exif_bytes):
    exif_length_bytes = struct.pack("<L", len(exif_bytes))
    crc = struct.pack("<L", crc32(EXIF_MARKER + exif_bytes))[::-1]
    print(EXIF_MARKER + exif_bytes)
    exif_chunk = {
        "fourcc":EXIF_MARKER,
        "length_bytes":exif_length_bytes,
        "data":exif_bytes,
        "crc":crc
    }

    for index, chunk in enumerate(chunks):
        if chunk["fourcc"] == EXIF_MARKER:
            chunks[index] = exif_chunk
            return chunks
    chunks.insert(-1, exif_chunk)
    for chunk in chunks:
        print(chunk["fourcc"])
    return chunks


def insert(png_bytes, exif_bytes):
    EXIF_CODE = b"Exif\x00\x00"
    if exif_bytes.startswith(EXIF_CODE):
        exif_bytes = exif_bytes[6:]
    chunks = split(png_bytes)
    new_chunks = insert_exif_into_chunks(chunks, exif_bytes)
    merged = merge_chunks(new_chunks)
    new_png_bytes = PNG_HEADER + merged
    return new_png_bytes


def remove(png_bytes):
    chunks = split(png_bytes)
    for index, chunk in enumerate(chunks):
        if chunk["fourcc"] == EXIF_MARKER:
            chunks.pop(index)
            break
    merged = merge_chunks(chunks)
    new_png_bytes = PNG_HEADER + merged
    return new_png_bytes
