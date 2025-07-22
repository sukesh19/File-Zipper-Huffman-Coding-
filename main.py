import heapq
from collections import defaultdict, Counter
import pickle

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}
    
    def build_frequency_table(self, text):
        """Build frequency table from text"""
        return Counter(text)
    
    def build_huffman_tree(self, frequency):
        """Build Huffman tree from frequency table"""
        heap = []
        
        # Create leaf nodes and add to heap
        for char, freq in frequency.items():
            node = Node(char, freq)
            heapq.heappush(heap, node)
        
        # Build tree bottom-up
        while len(heap) > 1:
            # Get two nodes with minimum frequency
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # Create internal node
            internal_node = Node(freq=left.freq + right.freq, left=left, right=right)
            heapq.heappush(heap, internal_node)
        
        self.root = heap[0]
        return self.root
    
    def generate_codes(self, root, code=""):
        """Generate Huffman codes for each character"""
        if root:
            # Leaf node
            if root.char:
                self.codes[root.char] = code if code else "0"  # Single char case
                self.reverse_codes[code if code else "0"] = root.char
                return
            
            # Traverse left and right
            self.generate_codes(root.left, code + "0")
            self.generate_codes(root.right, code + "1")
    
    def encode_text(self, text):
        """Encode text using Huffman codes"""
        encoded = ""
        for char in text:
            encoded += self.codes[char]
        return encoded
    
    def decode_text(self, encoded_text):
        """Decode text using Huffman tree"""
        decoded = ""
        current_node = self.root
        
        for bit in encoded_text:
            if bit == "0":
                current_node = current_node.left
            else:
                current_node = current_node.right
            
            # Reached leaf node
            if current_node.char:
                decoded += current_node.char
                current_node = self.root
        
        return decoded
    
    def compress_file(self, input_file, output_file):
        """Compress a file using Huffman coding"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if not text:
                print("File is empty!")
                return
            
            # Build Huffman tree
            frequency = self.build_frequency_table(text)
            self.build_huffman_tree(frequency)
            self.generate_codes(self.root)
            
            # Encode text
            encoded_text = self.encode_text(text)
            
            # Save compressed data
            with open(output_file, 'wb') as f:
                pickle.dump({
                    'encoded_text': encoded_text,
                    'codes': self.reverse_codes,
                    'original_size': len(text)
                }, f)
            
            # Calculate compression ratio
            original_size = len(text) * 8  # Original size in bits
            compressed_size = len(encoded_text)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"Compression complete!")
            print(f"Original size: {original_size} bits")
            print(f"Compressed size: {compressed_size} bits")
            print(f"Compression ratio: {compression_ratio:.2f}%")
            
        except FileNotFoundError:
            print(f"File '{input_file}' not found!")
    
    def decompress_file(self, input_file, output_file):
        """Decompress a Huffman coded file"""
        try:
            with open(input_file, 'rb') as f:
                data = pickle.load(f)
            
            encoded_text = data['encoded_text']
            self.reverse_codes = data['codes']
            
            # Rebuild tree from codes
            self.rebuild_tree_from_codes()
            
            # Decode text
            decoded_text = self.decode_text(encoded_text)
            
            # Save decompressed text
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decoded_text)
            
            print(f"Decompression complete! File saved as '{output_file}'")
            
        except FileNotFoundError:
            print(f"Compressed file '{input_file}' not found!")
    
    def rebuild_tree_from_codes(self):
        """Rebuild Huffman tree from codes"""
        self.root = Node()
        
        for code, char in self.reverse_codes.items():
            current_node = self.root
            
            for bit in code:
                if bit == "0":
                    if not current_node.left:
                        current_node.left = Node()
                    current_node = current_node.left
                else:
                    if not current_node.right:
                        current_node.right = Node()
                    current_node = current_node.right
            
            current_node.char = char

# Example usage
def demo_huffman():
    # Create sample text file
    sample_text = """
    This is a sample text for Huffman coding demonstration.
    The algorithm will compress this text by assigning shorter codes
    to more frequently occurring characters. This results in significant
    space savings for text files with repetitive patterns.
    """
    
    with open("sample.txt", "w") as f:
        f.write(sample_text)
    
    # Compress and decompress
    huffman = HuffmanCoding()
    
    print("Compressing file...")
    huffman.compress_file("sample.txt", "compressed.bin")
    
    print("\nDecompressing file...")
    huffman.decompress_file("compressed.bin", "decompressed.txt")
    
    # Verify files are identical
    with open("sample.txt", "r") as f1, open("decompressed.txt", "r") as f2:
        if f1.read() == f2.read():
            print("\n✓ Compression and decompression successful!")
        else:
            print("\n✗ Error in compression/decompression")

if __name__ == "__main__":
    demo_huffman()
