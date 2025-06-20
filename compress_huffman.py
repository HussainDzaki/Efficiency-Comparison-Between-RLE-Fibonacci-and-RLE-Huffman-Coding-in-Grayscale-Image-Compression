from utils import *

file_path = 'Gajah_Gray_scale.png'

# ---- Main Process ----
array_gray_scale = read_grayscale_image_to_array(file_path)

# Flatten to 1D
flat_pixels = array_gray_scale

# RLE on 1D pixel list
rle_list = run_length_encode(flat_pixels)

# ---------- Run Huffman Coding ----------
# Assuming rle_list is already generated from flat_pixels
freq_dict = count_gray_frequencies(rle_list)
huffman_tree = build_huffman_tree(freq_dict)
huffman_codes = generate_huffman_codes(huffman_tree)
huffman_encoded_rle = huffman_encode_rle(rle_list, huffman_codes)


# ---------- Output Result ----------
print("\n--- Huffman Codes ---")
for gray, code in sorted(huffman_codes.items()):
    print(f"Gray {gray}: {code}")

# --- Analysis ---
total_pixels = array_gray_scale.size
original_size_bits = total_pixels * 8  # Each pixel = 8 bits

# Assume each 'count' still stored as 8 bits (or you can use Fibonacci length instead)
gray_code_bits = sum(len(gray_code) for gray_code, _ in huffman_encoded_rle)
count_bits = len(huffman_encoded_rle) * 8  # 8 bits per count
compressed_size_bits = gray_code_bits + count_bits

print_analysis("RLE Huffman Analysis",original_size_bits, gray_code_bits,count_bits)