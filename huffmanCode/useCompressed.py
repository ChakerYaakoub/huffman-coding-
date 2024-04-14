from huffman import HuffmanCoding
import sys

path = "sample.txt"

h = HuffmanCoding()

output_path = h.compress(path)
print("Compressed file path: " + output_path)

