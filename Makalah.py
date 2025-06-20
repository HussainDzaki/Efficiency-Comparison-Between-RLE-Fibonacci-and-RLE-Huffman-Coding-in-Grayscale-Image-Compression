from PIL import Image
from collections import defaultdict
import numpy as np
import heapq
import csv

# ---- Settings ----

file_path = 'input.png'

# ---- Image Reading ----
def read_grayscale_image_to_array(filepath):
    img = Image.open(filepath).convert('L')
    return np.array(img).flatten()

# ---- Run-Length Encoding ----
def run_length_encode(arr):
    rle = []
    prev = arr[0]
    rle_length = 1
    for pixel in arr[1:]:
        if pixel == prev:
            rle_length += 1
        else:
            rle.append((prev, rle_length))
            prev = pixel
            rle_length = 1
    rle.append((prev, rle_length))
    return rle

# ---- Fibonacci Encoding ----
# N denote preallocation size
N = 100

fib = [0 for _ in range(N)]

def largestFiboLessOrEqual(n):
    fib[0] = 1
    fib[1] = 2
    i = 2
    while fib[i - 1] <= n:
        fib[i] = fib[i - 1] + fib[i - 2]
        i += 1
    return i - 2

def fibonacciEncoding(n):
    index = largestFiboLessOrEqual(n)
    codeword = ['*' for _ in range(index + 2)] #initialize array
    i = index
    while n:
        codeword[i] = '1'
        n -= fib[i]
        i -= 1
        while i >= 0 and fib[i] > n:
            codeword[i] = '0'
            i -= 1
    codeword[index + 1] = '1'
    return "".join(codeword)

def decimal_to_binary(n):
    return bin(n)[2:]

# --- Huffman Encoding --- 
# Node structure for Huffman tree
class HuffmanNode:
    def __init__(self, gray=None, freq=None, left=None, right=None):
        self.gray = gray      # Grayscale value
        self.freq = freq      # Frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

# Step 1: Count frequency of gray values from RLE
def count_gray_frequencies(rle_list):
    freq = defaultdict(int)
    for value, count in rle_list:
        freq[value] += count
    return freq

# Step 2–4: Build Huffman tree from frequency
def build_huffman_tree(freq_dict):
    heap = []
    for gray, freq in freq_dict.items():
        heapq.heappush(heap, HuffmanNode(gray=gray, freq=freq))

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

# Step 5–6: Traverse tree to get binary Huffman codes
def generate_huffman_codes(tree):
    codes = {}

    def traverse(node, prefix=""):
        if node is None:
            return
        if node.gray is not None:
            codes[node.gray] = prefix
        traverse(node.left, prefix + "0")
        traverse(node.right, prefix + "1")

    traverse(tree)
    return codes

# Apply Huffman encoding to RLE list
def huffman_encode_rle(rle_list, huffman_codes):
    return [(huffman_codes[value], count) for value, count in rle_list]



# ---- Main Process ----
array_gray_scale = read_grayscale_image_to_array(file_path)

# Flatten to 1D
flat_pixels = array_gray_scale

# RLE on 1D pixel list
rle_list = run_length_encode(flat_pixels)



# Encode (value, count) -> (binary(value), fibonacci(count))
rle_encoded_list = [(decimal_to_binary(val), fibonacciEncoding(count)) for val, count in rle_list]

rle_encoded_list_basic = [(decimal_to_binary(val), decimal_to_binary(count)) for val, count in rle_list]


# ---- Output ----
# for i, (val_bin, fib_code) in enumerate(rle_encoded_list):
#     print(f"{i:04d}: Value (bin) = {val_bin}, Count Fibo-Encoded = {fib_code}")



# Apply Huffman encoding to RLE list
def huffman_encode_rle(rle_list, huffman_codes):
    return [(huffman_codes[value], decimal_to_binary(count) ) for value, count in rle_list]



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

# print("\n--- Huffman Encoded RLE ---")
# for i, (gray_code, count) in enumerate(huffman_encoded_rle):
#     print(f"{i:04d}: Gray Code = {gray_code}, Count = {count}") 

# ---- Analysis ----
# write summary
def print_analysis(title, original_bits, pixel_bits, length_bits):
    compressed_bits = pixel_bits + length_bits
    print(f"\n--- {title} ---")
    print(f"Original Size   : {original_bits} bits")
    print(f"Compressed Size : {compressed_bits} bits")
    print(f"  - Pixel Values: {pixel_bits} bits")
    print(f"  - Run Lengths : {length_bits} bits")
    if compressed_bits > 0:
        ratio = compressed_bits / original_bits * 100
        print(f"Compression Ratio: {ratio:.2f}%")
        size_reduction = 100 - ratio
        print(f"Size reduction: {size_reduction:.2f}%")
    return compressed_bits

original_size_bits = array_gray_scale.size * 8  # each pixel = 8 bits
val_size_bits = len(rle_encoded_list) * 8
length_size_bits = sum(len(code) for _, code in rle_encoded_list)

print_analysis("Analysis RLE Fibonaccii encoding", original_size_bits, val_size_bits,length_size_bits)

# --- Analysis ---
total_pixels = array_gray_scale.size
original_size_bits = total_pixels * 8  # Each pixel = 8 bits

# Assume each 'count' still stored as 8 bits (or you can use Fibonacci length instead)
gray_code_bits = sum(len(gray_code) for gray_code, _ in huffman_encoded_rle)
count_bits = len(huffman_encoded_rle) * 8  # 8 bits per count
compressed_size_bits = gray_code_bits + count_bits

print_analysis("RLE Huffman Analysis",original_size_bits, gray_code_bits,count_bits)

# ---- Analysis ----
original_size_bits = array_gray_scale.size * 8  # each pixel = 8 bits
val_size_bits_RLE = len(rle_encoded_list_basic) * 8
length_size_bits_RLE = len(rle_encoded_list_basic) * 8

print_analysis("Analysis Basic RLE",original_size_bits, val_size_bits_RLE,length_size_bits_RLE)




# --- SAVE RLE + Fibonacci to CSV ---
with open('rle_fibonacci.csv', mode='w', newline='') as file_fib:
    writer = csv.writer(file_fib)
    writer.writerow(['Gray_Binary', 'Count_Fib_Encoded'])
    for gray_bin, fib_code in rle_encoded_list:
        writer.writerow([gray_bin, fib_code])

# --- SAVE RLE + Huffman to CSV ---
with open('rle_huffman.csv', mode='w', newline='') as file_huff:
    writer = csv.writer(file_huff)
    writer.writerow(['Gray_Huffman_Code', 'Count'])
    for gray_code, count in huffman_encoded_rle:
        writer.writerow([gray_code, count])

def save_decompressed_to_image(decompressed, shape, output_file):
    array_2d = np.array(decompressed, dtype=np.uint8).reshape(shape)
    img = Image.fromarray(array_2d, 'L')
    img.save(output_file)


def fibonacci_decoding(code):
    # Generate same Fibonacci list as encoder
    fib = [1, 2]
    while len(fib) < len(code):  # overshoot sedikit
        fib.append(fib[-1] + fib[-2])

    result = 0
    for i in range(len(code) - 1):  # Skip last '1' (terminator)
        if code[i] == '1':
            result += fib[i]
    return result

def decompress_fibonacci_csv(file_path):
    decompressed = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gray_val = int(row['Gray_Binary'], 2)
            count = fibonacci_decoding(row['Count_Fib_Encoded'])
            decompressed.extend([gray_val] * count)
    return decompressed

# Reverse huffman_codes dictionary: code → gray_value
reverse_huffman_codes = {code: gray for gray, code in huffman_codes.items()}
def decompress_huffman_csv(file_path, reverse_huffman_codes):
    decompressed = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            gray_val = reverse_huffman_codes[row['Gray_Huffman_Code']]
            count = int(row['Count'])
            decompressed.extend([gray_val] * count)
    return decompressed

def save_decompressed_to_image(decompressed, shape, output_file):
    array_2d = np.array(decompressed, dtype=np.uint8).reshape(shape)
    img = Image.fromarray(array_2d, 'L')
    img.save(output_file)


# pixels = decompress_fibonacci_csv('rle_fibonacci.csv')
# save_decompressed_to_image(pixels, array_gray_scale.shape, 'decoded_fib.png')

# pixels = decompress_huffman_csv('rle_huffman.csv', reverse_huffman_codes)
# save_decompressed_to_image(pixels, array_gray_scale.shape, 'decoded_huff.png')

