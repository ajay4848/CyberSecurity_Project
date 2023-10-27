import numpy as np

from math import floor
from PIL import Image
from time import sleep



def add_leading_zero(byte):

    while len(byte) != 8:
        byte = '0' + byte
    return byte


def colorByte(colorCode):
    return add_leading_zero(bin(colorCode)[2:])


def format_pixels(pixelValues):
   
    return [colorCode for pixel in pixelValues for colorCode in pixel]


def image_size(imagePATH):
    with open(imagePATH,"rb") as fp:
        im = Image.open(fp)
        width, height = im.size
        im.close()
        return (width, height)


def get_pixels(imagePATH):
    im = Image.open(imagePATH).convert('RGB')  
    pixelValues = list(im.getdata())
    im.close()
    return pixelValues


def encodeMessage(message):
  
    binaryMessage = ''
    for i in range(len(message)):
        current_char = message[i]
        binaryMessage += add_leading_zero(bin(ord(current_char))[2:])
        try:
       
            next_char = message[i+1]
            binaryMessage += '0'
        except:  
            binaryMessage += '1'
    
    return binaryMessage, len(binaryMessage)




def encryptMessage(message, original_imagePATH, encrypted_imagePATH, initial_colorCode, step_size):
    width, height = image_size(original_imagePATH)
    binaryMessage, binaryMessageLength = encodeMessage(message)
    org_colorCodeValues = format_pixels(get_pixels(original_imagePATH))
    enc_colorCodeValues = org_colorCodeValues.copy()
    initial_colorCode_loc = initial_colorCode[0] * initial_colorCode[1]
    final_pixel_loc = initial_colorCode_loc + (binaryMessageLength*step_size)
    bit_counter = 0
    
   
    expected_size = height * width * 3
    actual_size = len(enc_colorCodeValues)

  
    if actual_size != expected_size:
        print(f"Error: Unexpected array size ({actual_size}). Expected size: {expected_size}")
    else:
        for i in range(initial_colorCode_loc, final_pixel_loc, step_size):
            org_colorCode = org_colorCodeValues[i]
            messageBit = binaryMessage[bit_counter]

            enc_colorCodeValues[i] = int(colorByte(org_colorCode)[:7] + messageBit, 2)
            bit_counter += 1

     
        updated_pixelValues = np.reshape(
            np.array(enc_colorCodeValues, dtype=np.uint8), newshape=(height, width, 3))
        
      
        enc_image = Image.fromarray(updated_pixelValues)
        enc_image.save(encrypted_imagePATH)
        enc_image.close()



def decryptMessage(encrypted_imagePATH, initial_colorCode, step_size):

    enc_colorCodeValues = format_pixels(get_pixels(encrypted_imagePATH))
    initial_colorCode_loc = initial_colorCode[0] * initial_colorCode[1]
    step_counter = 0
    bitCounter = 1
    EOF_bit = '0'
    binaryMessage = ''
    while EOF_bit != '1':
        enc_colorCode = enc_colorCodeValues[initial_colorCode_loc + step_counter]
        decrypted_bit = colorByte(enc_colorCode)[-1]
        if bitCounter % 9 != 0:
            binaryMessage += decrypted_bit
        else:
            EOF_bit = decrypted_bit
            if EOF_bit == '1':
                break
            else:
                binaryMessage += ','
        step_counter += step_size
        bitCounter += 1

    decrypted_message = ''.join([chr(int(i, 2)) for i in binaryMessage.split(',')])
    
    return decrypted_message



def run_encryption(message, original_imagePATH, encrypted_imagePATH, initial_colorCode=(0, 0), step_size=1):

    pixel_num = image_size(original_imagePATH)[0]*image_size(original_imagePATH)[1]
    max_char_num = floor(pixel_num / 3)
    messageLength = len(message)

    print('Starting the encryption process...')
    print('-'*10)
    sleep(1)
    print('Pixel number: {}'.format(pixel_num))
    print('Maximum characters/bytes that can be stored in the image: {}'.format(max_char_num))
    print('Length of the message: {}'.format(messageLength))
    print('-'*10)
    encryptMessage(message, original_imagePATH, encrypted_imagePATH, initial_colorCode, step_size)
    print('Encryption is successful!')


def run_decryption(encrypted_imagePATH, initial_colorCode=(0, 0), step_size=1):

    print('Starting the decryption process...')
    sleep(1)
    print('-'*10)
    print('Printing the result...')
    sleep(1)
    print('='*10)
    try:
        print(decryptMessage(encrypted_imagePATH, initial_colorCode, step_size))
        print('='*10)
        print('Decryption is successful!')
    except:
        print('Something went wrong!')
