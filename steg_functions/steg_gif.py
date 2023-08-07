import io
from PIL import _binary
from pathlib import Path
from PIL._util import is_path



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


def encode(src, message, dest=None):
    if dest:
        set_comment(src, message, dest)
    else:
        buffer = set_comment(src, message, dest)

def decode(fp):

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
             
# message = input("Enter message: ")
# tp = open('giphy.gif', 'rb')
# # tp.close()
# encode(tp, message, 'giphy_out.gif')
# xp = open('giphy_out.gif', 'rb')
# # xp.close()
# decode(xp)
# tp.close()
# xp.close()