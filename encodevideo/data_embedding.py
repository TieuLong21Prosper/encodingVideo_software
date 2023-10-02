
#------ Thu vien ngoai ------#
import bitstring
import numpy as np
#================================#

def extract_encoded_data_from_DCT(dct_blocks):
    extracted_data = ""
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            if (curr_coeff > 1):
                temp=np.uint8(current_dct_block[i]) & 0x01
                extracted_data += bitstring.pack('uint:1', np.uint8(current_dct_block[i]) & 0x01)
    return extracted_data

# ============================================================================= #
# ============================================================================= #
#dau tin o lsb cua cac trong so co gia tri duong
def embed_encoded_data_into_DCT(encoded_bits, dct_blocks):
    data_complete = False; encoded_bits.pos = 0
    #Do dai cua chuoi bit ra thanh 32 bit
    encoded_data_len = bitstring.pack('uint:32', len(encoded_bits))
    converted_blocks = []
    for current_dct_block in dct_blocks:
        #Bo cai DC ra lay tu 1 tro di
        for i in range(1, len(current_dct_block)):
            #Lay tung phan tu trong mang 1 chieu ZIGZAG
            curr_coeff = np.int32(current_dct_block[i])
            
            if (curr_coeff > 1):
                #Chuyen doi curr_coeff sang dinh dang unit8
                curr_coeff = np.uint8(current_dct_block[i])
                if (encoded_bits.pos == (len(encoded_bits) )): data_complete = True; break
                #Chuyen curr_coeff sang 8 bit
                pack_coeff = bitstring.pack('uint:8', curr_coeff)
                if (encoded_data_len.pos <= len(encoded_data_len) - 1):  #Doc tung ki tu cua do dai
                    pack_coeff[-1] = encoded_data_len.read(1) #doc tu dau den cuoi msb to lsb, moi lan read thi se thang pos len 1
                    
                else: pack_coeff[-1] = encoded_bits.read(1) #Doc toi tung bit ki tu
                # gan nguoc lai
                current_dct_block[i] = np.float32(pack_coeff.read('uint:8'))
        converted_blocks.append(current_dct_block)

    if not(data_complete): raise ValueError("Lỗi! Dữ liệu không được nhúng vô ảnh")

    return converted_blocks