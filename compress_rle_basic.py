from utils import *

file_path = 'Gajah_Gray_scale.png'


# ---- Main Process ----
array_gray_scale = read_grayscale_image_to_array(file_path)

# Flatten to 1D
flat_pixels = array_gray_scale

# RLE on 1D pixel list
rle_list = run_length_encode(flat_pixels)
rle_encoded_list_basic = [(decimal_to_binary(val), decimal_to_binary(count)) for val, count in rle_list]
# ---- Analysis ----
original_size_bits = array_gray_scale.size * 8  # each pixel = 8 bits
val_size_bits_RLE = len(rle_encoded_list_basic) * 8
length_size_bits_RLE = len(rle_encoded_list_basic) * 8

print_analysis("Analysis Basic RLE",original_size_bits, val_size_bits_RLE,length_size_bits_RLE)