
#------ Thu vien ngoai ------#
import cv2
import struct
import bitstring
import sys
import numpy  as np
import zigzag as zz

#---------- Source --------#
import image_preparation as img
import data_embedding as stego
#================================#


def f_run_stego(frame,stringin):
    NUM_CHANNELS = 3
    COVER_IMAGE_FILEPATH  = frame#(PNG)
    STEGO_IMAGE_FILEPATH = frame
    SECRET_MESSAGE_STRING =  stringin

   
    # ============================================================================= #
    # =========================== BAT DAU TH CODE ============================ #
    
    #Doc xu li thi giac may tinh bang OpenCV, doc file anh nay` co mau dinh dang BGR
    raw_cover_image = cv2.imread(COVER_IMAGE_FILEPATH, flags=cv2.IMREAD_COLOR)
    #Hinh anh sau khi duoc doc se co ma tran 3 chieu la h,w va d, d se bang 3 neu anh mau (d=Channels)
    height, width   = raw_cover_image.shape[:2]
    # them cao vao rong cho du 8x8
    while(height % 8): height += 1 # Dong
    while(width  % 8): width  += 1 # Cot
    valid_dim = (width, height)
    padded_image    = cv2.resize(raw_cover_image, valid_dim)
    cover_image_f32 = np.float32(padded_image) #chuyen thanh mang float
    #Chuyen doi mau BGR cua anh sang YCrCb, Y la do choi, Cr Cb la thanh phan sac do khac nhau cua mau xanh va do
    #chuyen mang thanh tung mang 8x8 
    cover_image_YCC = img.YCC_Image(cv2.cvtColor(cover_image_f32, cv2.COLOR_BGR2YCrCb))
    
    # Tao mot ma tran anh rong~ co kich thuoc height x width bang anh ban dau
    stego_image = np.empty_like(cover_image_f32) 

    for chan_index in range(NUM_CHANNELS):
        # Thuc hien bien doi DCT thuan
        dct_blocks = [cv2.dct(block) for block in cover_image_YCC.channels[chan_index]]
        
        # Thuc hien luong tu hoa
        dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]
        
        # Thuc hien Zizag
        sorted_coefficients = [zz.zigzag(block) for block in dct_quants]

        # Nhung' du lieu vao do CHOI Y
        if (chan_index == 0):
            # Chuyen tung ki tu sang 8 bit de nhung'
            secret_data = ""
            for char in SECRET_MESSAGE_STRING.encode('ascii'): 
                secret_data += bitstring.pack('uint:8', char)
            embedded_dct_blocks   = stego.embed_encoded_data_into_DCT(secret_data, sorted_coefficients) # dau tin
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8,hmax=8) for block in embedded_dct_blocks] # tra mang 1 chiefu zigzac thanh 8x8
        else:
            # Chuyen zigzag mot chieu sang mang 2 chieu 8x8
            desorted_coefficients = [zz.inverse_zigzag(block, vmax=8,hmax=8) for block in sorted_coefficients]

        # Chuyen nguoc luong tu hoa bang cach NHAN cho Q50
        dct_dequants = [np.multiply(data, img.JPEG_STD_LUM_QUANT_TABLE) for data in desorted_coefficients]

        # Chuyen nguoc lai DCT la tu F sang f
        idct_blocks = [cv2.idct(block) for block in dct_dequants]

        # Dua hinh anh sau khi giau tin ve cac kenh ban dau la Y Cr Cb, asarray(tham so dau la mang can dua vao, tham so hai kieu du lieu, tham so 3 la sap xep)
        stego_image[:,:,chan_index] = np.asarray(img.stitch_8x8_blocks_back_together(cover_image_YCC.width, idct_blocks))
        
    #-------------------------------------------------------------------------------------------------------------------#

    # Chuyen mau YCrCb sang lai BGR
    stego_image_BGR = cv2.cvtColor(stego_image, cv2.COLOR_YCR_CB2BGR)

    #gioi han gia tri pixel tu [0-255]
    final_stego_image = np.uint8(np.clip(stego_image_BGR, 0, 255))
    
    # Viet vo phai tmp cai anh
    cv2.imwrite(STEGO_IMAGE_FILEPATH, final_stego_image)
#f_run_stego("image.PNG","123")