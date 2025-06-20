from utils import *

file_path = 'Gajah_Gray_scale.png'

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

# ---- Main Process ----
array_gray_scale = read_grayscale_image_to_array(file_path)

# Flatten to 1D
flat_pixels = array_gray_scale

# RLE on 1D pixel list
rle_list = run_length_encode(flat_pixels)



# Encode (value, count) -> (binary(value), fibonacci(count))
rle_encoded_list = [(decimal_to_binary(val), fibonacciEncoding(count)) for val, count in rle_list]

rle_encoded_list_basic = [(decimal_to_binary(val), decimal_to_binary(count)) for val, count in rle_list]



original_size_bits = array_gray_scale.size * 8  # each pixel = 8 bits
val_size_bits = len(rle_encoded_list) * 8
length_size_bits = sum(len(code) for _, code in rle_encoded_list)

print_analysis("Analysis RLE Fibonaccii encoding", original_size_bits, val_size_bits,length_size_bits)


