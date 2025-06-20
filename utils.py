from PIL import Image
import numpy as np
from collections import defaultdict
import heapq
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
