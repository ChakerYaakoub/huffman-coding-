from huffman import HuffmanCoding
import sys

# just for test  
# just for test  
# just for test  

h = HuffmanCoding()

reverse_mapping ={'00': 'h', '01': 'k', '100': 'r', '101': 'e', '110': 'c', '111': 'a'}

DecompressText = h.decompress( b'\x08\xc7l\x00' ,reverse_mapping )
print("Decompressed file path: " + DecompressText)