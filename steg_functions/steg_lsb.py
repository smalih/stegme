from PIL import Image
from math import ceil
import numpy as np





def encode(src, message, dest=None):
    try:
        input_img = Image.open(src, 'r')
    except FileNotFoundError:
        print("File cannot be found. Please ensure file exists.")
        return
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
        print("type", type(enc_img))
        return enc_img

def decode(src):
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

# input_src = input("Enter input location")
# message = input("Enter message: ")
# encode(input_src, message, 'out.png')
# output_src = input("Enter output location: ")
# print(decode(output_src))