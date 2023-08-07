import io
from PIL import Image, _binary
from pathlib import Path
from PIL._util import is_path

from math import ceil
import numpy as np

terminating_string = "$end$"

def set_comment(fp, comment, out_path=None):
    
    exclusive_fp = False
    filename = ''
    if isinstance(fp, Path):
        filename = str(fp.resolve())
    elif is_path(fp):
        filename = fp

    if filename:
        fp = open(filename, 'rb')
        exclusive_fp = True # exclusive_fp means path was passed
    try:
        fp.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        fp = io.BytesIO(fp.read())
        exclusive_fp = True

    # skip through data of extension blocks
    # - all extension blocks except comment have a BLOCKSIZE field
    def skip_data():
        s = fp.read(1) # blocksize
        if s and s[0]:
            return fp.read(s[0]) # read through next BLOCKSIZE bytes

    s = fp.read(13) # read gif file header

    # first 6 bytes of gif file denote file signature (i.e., GIF)
    # and file version (87a or 89a)
    if s[:6] not in [b'GIF87a', b'GIF89a']:
        raise SyntaxError("File provided is not a gif file")
    
    packed = s[10] # 10th byte is the packed value (packed is little endian)

    # bitwise AND with 10000000
    # if global color table (GCT) exists
    if packed & 128:

        # bits 0-2 denote the size of gct, and 7(b10) is 111,
        # so packed & 7 = packed
        # maybe purpose and & is to add/remove padding, and/or conversion
        
        # (spec states num_gct_entries = gct_size + 1)
        num_gct_entries = (packed & 7) + 1


        # each gct is 3 bytes in size
        # so one gct requires 3 bytes, two gcts 6 bytes, 3 gcts 9 bytes
        fp.read(3 << num_gct_entries) # NOTE: should this be * rather than <<?

    # after will store location of pointer after comment block
    after = None

    # mark position to insert comment block
    before = fp.tell()
    after = before
    s = fp.read(1) # first byte of extension block indicates extension block
    if s == b'!': # if block is an extension block
        s = fp.read(1)
        if s[0] == 254: # if extension block is a comment block
            
            # skip through comment block
            while skip_data():
                pass
            after = fp.tell() # mark position of end of comment block
    fp.seek(0)
    before_bytes = fp.read(before)
    fp.seek(after)
    after_bytes = fp.read()
    if out_path:
        fp = open(out_path, 'wb')
    # else:
    #     fp = io.BufferedWriter(io.BytesIO())

    fp.write(before_bytes) # write all bytes before comment block

    # write comment block
    if comment:
        # write introducer and label of comment block
        #  (! indicates extension block, 254(b10) = xFE which indicates comment block)
        fp.write(b"!" + _binary.o8(254))

        # convery comment to binary if not already
        if isinstance(comment, str):
            comment = comment.encode()
        if not isinstance(comment, bytes):
            raise SyntaxError("Comment provided is not a string or binary string")
        
        # write comment in blocks of 256 bytes (1 byte for subbblock size, up to 255 bytes for comment)
        for i in range(0, len(comment), 255):
            subblock = comment[i: i + 255]
            # write subblock size + comment partition to file
            fp.write(_binary.o8(len(subblock)) + subblock)

        fp.write(_binary.o8(0)) # write block terminator
    fp.write(after_bytes) # write remaining bytes
    fp.close()


def decode_gif(fp):

    def read_comment_data():
        comment = b''
        while True:
            s = fp.read(1)
            if s == _binary.o8(0): # if terminator
                return comment 
            comment += fp.read(s[0])

    exclusive_fp = False
    filename = ''
    if isinstance(fp, Path):
        filename = str(fp.resolve())
    elif is_path(fp):
        filename = fp

    if filename:
        fp = open(filename, 'rb')
        exclusive_fp = True # exclusive_fp means path was passed
    try:
        fp.seek(0)
    except (AttributeError, io.UnsupportedOperation):
        fp = io.BytesIO(fp.read())
        exclusive_fp = True

    s = fp.read(13) # read gif file header
    if s[:6] not in [b'GIF87a', b'GIF89a']:
        raise SyntaxError("File provided is not a gif file")
    packed = s[10]

    if packed & 128:
        num_gct_entries = (packed & 7) + 1
        fp.read(3 << num_gct_entries)

    s = fp.read(1)
    if s == b'!':
        s = fp.read(1)
        if s[0] == 254:
            comment = read_comment_data()
            comment = comment.decode()
            print(comment)
            return comment



def encode_img(src, message, dest=None):
    try:
        input_img = Image.open(src, 'r')
    except FileNotFoundError:
        print("File cannot be found. Please ensure file exists.")
        return
    print('opening')
    width, height = input_img.size
    img_array = np.array(list(input_img.getdata()))
    print(input_img.mode)
    if input_img.mode == "RGB":
        n = 3
    elif input_img.mode == "RGBA":
        n = 4
    else:
        raise ValueError("Unable detect image mode of input image")

    total_pixels = len(img_array)
    
    message += terminating_string
    b_message = ''.join([format(ord(i), "08b") for i in message])
    min_pixels = ceil(len(b_message) / 3)
    if min_pixels > total_pixels:
        raise ValueError("input image does not have enough bits to encode message. Please choose an image with a larger file size")

    # print(img_array.size) # no. of r,g,b,a bytes (= len(img_array) * 4)
    # print(len(img_array)) # no. pixels (= width * height)
    
    index = 0
    for pixel in range(min_pixels):
        for colour in range(0,3):
            # print(img_array[pixel][colour])
            if index >= len(b_message):
                print("hello")
            try:
                img_array[pixel][colour] = int(bin(img_array[pixel][colour])[2:7] + b_message[index], 2)
            except IndexError:
                print("Error: ", pixel, index, len(b_message))
                break 
            index+=1
    
    img_array=img_array.reshape(height, width, n)
    enc_img = Image.fromarray(img_array.astype('uint8'), input_img.mode)
    # s = BytesIO()
    # enc_img.save(s, format="png")
    # return enc_img
    if dest:
        enc_img.save(dest, format="PNG")
    else:
        return enc_img

def decode_img(src):
    try:
        input_img = Image.open(src, 'r')
    except FileNotFoundError:
        print("File cannot be found. Please ensure file exists.")
        return
    encoded_img = Image.open(src, 'r')
    img_array = np.array(list(encoded_img.getdata()))

    terminating_binary = ''.join([format(ord(i), "08b") for i in terminating_string])
    hidden_b_message = ""
    break_loop = False
    for pixel in range(len(img_array)):
        for colour in range(3):
            hidden_b_message+=bin(img_array[pixel][colour])[-1]
            # print(hidden_b_message)
            if hidden_b_message[-len(terminating_binary):] == terminating_binary:
                print("yo")
                print(hidden_b_message[-len(terminating_binary):])
                # print(hidden_b_message)
                break_loop = True
                break
        if break_loop:
            break
    if not break_loop:
        print("Image does not contain hidden_message")
        return
    # print(hidden_b_message)
    hidden_message = ""      
    for i in range(0, len(hidden_b_message) - len(terminating_binary), 8):
        hidden_message += chr(int(hidden_b_message[i:i+8], 2))
    print(hidden_message)
    return hidden_message





def encode(fp, file_type, message, dest=None):
    if file_type == 'image/gif':
         set_comment(fp, message, dest)
    elif file_type in ['image/png', 'image/jpeg']:
        encode_img(fp, message, dest)
    else:
        raise Exception(f'File type {file_type} not supported')





def decode(fp, file_type):
    if file_type == 'image/gif':
       return decode_gif(fp)
    elif file_type in ['image/png', 'image/jpeg']:
        return decode_img(fp)


