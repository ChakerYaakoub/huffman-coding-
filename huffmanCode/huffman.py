import heapq
import os

class HuffmanCoding:
	def __init__(self):
		
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def make_frequency_dict(self, text):
     #calc freq and return  
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
        #make priority queue and return 
        #return heap
        
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
       # build huffman tree , Save root node in heap 
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)

    # i just use in the make codes fc 
	def make_codes_helper(self, root, current_code):
        #make codes from root to leaf and save 
     
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
        # make codes from root to leaf and save 
        #make codes for each character and save 
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
        #replace character with code and return
     
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
        #pad encoded text to make it multiple of 8 and return
     
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
        #convert bits  to bytes array and return byte array
     
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self  , content):


		text = content
		# text = text.rstrip()

		frequency = self.make_frequency_dict(text)
		self.make_heap(frequency)
		self.merge_nodes()
		self.make_codes()

		encoded_text = self.get_encoded_text(text)
		padded_encoded_text = self.pad_encoded_text(encoded_text)

		b = self.get_byte_array(padded_encoded_text)
		# output.write(bytes(b))

		print("Compressed")
		# print(self.reverse_mapping)
		# print(bytes(b))
  
  
  
  
  
  
		return b , self.reverse_mapping


	""" functions for decompression: """

#    USED  IN THE DECOMPRESS FC
	def remove_padding(self, padded_encoded_text):
        #remove padding from bit string and return
     
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text


    #DECODE THE TEXT
	def decode_text(self, encoded_text , reverse_mapping):
        #decode the text and return
     
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in reverse_mapping):
				character = reverse_mapping[current_code]
				decoded_text += character
				current_code = ""
    
    

		return decoded_text


	def decompress(self, content ,reverse_mapping):

		bit_string = ""


		for byte in content:
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits 


		encoded_text = self.remove_padding(bit_string)
		# print('encoded_text: ', encoded_text)
		# print('reverse_mapping in huffman: ', reverse_mapping)
  
  
  


		decompressed_text = self.decode_text(encoded_text , reverse_mapping)
			

		# print("Decompressed")
		return decompressed_text

