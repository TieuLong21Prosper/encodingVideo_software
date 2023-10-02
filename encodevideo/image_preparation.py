
#------ Thu Vien Ngoai------#
import cv2
import numpy as np
#================================#

#Test cho vui
HORIZ_AXIS = 1
VERT_AXIS  = 0

# Chon Q50 de vua` co anh dep vua nen' tot'
JPEG_STD_LUM_QUANT_TABLE = np.asarray([
                                        [16, 11, 10, 16,  24, 40,   51,  61],
                                        [12, 12, 14, 19,  26, 58,   60,  55],
                                        [14, 13, 16, 24,  40, 57,   69,  56],
                                        [14, 17, 22, 29,  51, 87,   80,  62],
                                        [18, 22, 37, 56,  68, 109, 103,  77],
                                        [24, 36, 55, 64,  81, 104, 113,  92],
                                        [49, 64, 78, 87, 103, 121, 120, 101],
                                        [72, 92, 95, 98, 112, 100, 103,  99]
                                      ],
                                      dtype = np.float32)
# Chia 1 hinh` thanh` cac khoi block 8x8
class YCC_Image(object):
    def __init__(self, cover_image):
        self.height, self.width = cover_image.shape[:2]
        #Ba kenh la Y Cr Cb tuong ung 0 1 2, lay ra ma tran 2D cua moi kenh
        self.channels = [
                         split_image_into_8x8_blocks(cover_image[:,:,0]),
                         split_image_into_8x8_blocks(cover_image[:,:,1]),
                         split_image_into_8x8_blocks(cover_image[:,:,2]),
                        ]

#====================================================================================================#
#====================================================================================================#

def stitch_8x8_blocks_back_together(Nc, block_segments):
    #Co rong 640 / 8 = 80 cu moi 80 khoi ta ghep chung lai voi nhau thang mot khoi' to, ham np.block se tu ghep cac khoi to thanh mot kenh lai
    
    #Do dai cua Block Segment la rat nhieu vi tham so truyen vao la mot mang chua nhieu MANG 8x8, Debug=3600 block segments
    #Width = 640
    image_rows = []
    temp = []
    for i in range(len(block_segments)):
        if i > 0 and not(i % int(Nc / 8)):
            image_rows.append(temp)
            temp = [block_segments[i]]
        else:
            temp.append(block_segments[i])
    image_rows.append(temp)

    return np.block(image_rows)

#====================================================================================================#
#====================================================================================================#

def split_image_into_8x8_blocks(image):
    blocks = []
    for vert_slice in np.vsplit(image, int(image.shape[0] / 8)):  #Chia mang  2 chieu theo cot
        for horiz_slice in np.hsplit(vert_slice, int(image.shape[1] / 8)): #Chia mang 2 chieu theo hang
            blocks.append(horiz_slice)
    return blocks

#====================================================================================================#
#====================================================================================================#