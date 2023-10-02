
#------ Thu vien ngoai ------#
import cv2
import struct
import sys
import bitstring
import numpy  as np
import zigzag as zz
#================================#
#---------- Source Dang dung trong file nay --------#
import data_embedding as stego

import image_preparation   as img
#================================#



def extract_stego(filename):
    stego_image     = cv2.imread(filename, flags=cv2.IMREAD_COLOR)
    stego_image_f32 = np.float32(stego_image)
    stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

    # Thuc hien DCT Thuan
    dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]]  # Quan tam kenh Luma (Y) kenh choi'

    # Luong Tu Hoa
    dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]

    # ZigZag ra mang 1 chieu
    sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

    # Giai ma de lay thong tin
    recovered_data = stego.extract_encoded_data_from_DCT(sorted_coefficients)
    
    # Lay do dai ra trc
    #print(int(recovered_data.read('uint:32')))
    data_len = int(recovered_data.read('uint:32') / 8)
    if data_len > 1000:
        return None

    # Lay du lieu ra
    extracted_data = bytes()
    for _ in range(data_len): extracted_data += struct.pack('=b', recovered_data.read('uint:8'))

    # CHuyen sang ascii
    #print(extracted_data.decode('ascii'))
    return extracted_data.decode('ascii')
#print(extract_stego("./image.PNG"))


