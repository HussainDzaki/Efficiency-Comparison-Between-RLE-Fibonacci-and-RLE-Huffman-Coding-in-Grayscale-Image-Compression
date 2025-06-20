# 📦 Grayscale Image Compression using RLE, Fibonacci, and Huffman Encoding
by Dzaki Ahmad Al Hussainy (13524084) from Informatics ITB
This repository contains the full implementation of grayscale image compression algorithms used in the research paper:  
**"Efficiency Comparison Between RLE-Fibonacci and RLE-Huffman Coding in Grayscale Image Compression"**.

## 📄 Overview

The project explores and compares multiple lossless image compression techniques applied to grayscale images, including:

- **Run-Length Encoding (RLE)**
- **RLE + Fibonacci Encoding**
- **RLE + Huffman Encoding**
- **Basic RLE using fixed-length binary encoding**

These methods are evaluated on two image scales: a **small 800-bit synthetic test** and a **large 1,036,800-bit real image**, with analysis of compression ratio and size reduction.

## 📁 Repository Structure
├── compress_fibonacci.py   # RLE + Fibonacci encoding implementation
├── compress_huffman.py     # RLE + Huffman encoding implementation
├── compress_rle_basic.py   # Basic RLE with fixed binary representation
├── utils.py                # Helper functions (Fibonacci, Huffman tree, binary conversion)
├── Makalah.py              # All combined file (so messy)
├── Gajah_Gray_scale.png    # Example grayscale image used for testing
└── README.md               # This file
