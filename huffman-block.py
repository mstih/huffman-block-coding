import random

alphabet = {
    'a' : 0.05, 
    'b' : 0.10,
    'c' : 0.15,
    'd' : 0.18,
    'e' : 0.22,
    'f' : 0.30
}

symbols = list(alphabet.keys())
p = list(alphabet.values())

sequence_len = 1000

#Generate the sequence
sequence = random.choices(symbols, weights=p, k=sequence_len )
print("####################################################\n")
print(f'Random sequence: {"".join(sequence[:100])}...\n')
print("####################################################\n")

# Create all 36 possible 2-letter blocks
all_blocks = []
for a in symbols:
    for b in symbols:
        all_blocks.append(a + b)


blocks = []
for i in range(0, len(sequence) - 1, 2):
    blocks.append(sequence[i] + sequence[i+1])

block_count = {block : 0 for block in all_blocks}
for block in blocks:
    if block in block_count:
        block_count[block] += 1

# Calculate the probability of these new blocks
total_blocks = len(blocks)   
block_probs = {block: block_count[block] / total_blocks for block in all_blocks}

# ACTUAL HUFFMAN CODE #
huffman_list = []
for b in block_probs:
    # Add all codes to a list 
    huffman_list.append([block_probs[b], [b, ""]])

# Sort the list and combine two with the lowest probabilities until there is only one
while len(huffman_list) > 1:
    # Sort them so the smallest are always ready to pop
    huffman_list.sort()
    # Pops the smallest two out
    first = huffman_list.pop(0)
    second = huffman_list.pop(0)

    for item in first[1:]:
        item[1] = "0" + item[1]
    for item in second[1:]:
        item[1] = "1" + item[1]

    # Join them and add them back to the list
    new_item = [first[0] + second[0]] + first[1:] + second[1:]
    huffman_list.append(new_item)

#Extract codes
codes = {}
for item in huffman_list[0][1:]:
    codes[item[0]] = item[1]

print("Huffman codes for blocks:")
for k, v in codes.items():
    print(f"{k}: {v}")
print()

# Calculate average length of codeword
average_len = 0
for b in block_probs:
    average_len += block_probs[b] * len(codes[b])

# Compression ratio calculated
# 1 ASCII char = 8bit -> 2 ASCII char = 16bit
compression_ratio = 16 / average_len 

print("Avg. codeword length: ", round(average_len, 2), "bits")
print("Compression ratio: ", round(compression_ratio, 2), "x")

# Encode the sequence using the Huffman codes
encoded_bits = ""
for b in blocks: 
    encoded_bits += codes[b]
# Print the encoded bit sequence (first 200 bits for preview)
print("Encoded sequence/bitstream (first 200 bits): ", encoded_bits[:200], '...')

#DECODING function
def decode(encoded_bits, codebook):
    reverse_codebook = {v: k for k, v in codebook.items()}
    decoded_blocks = []
    current = ""
    for bit in encoded_bits: 
        current += bit
        if current in reverse_codebook:
            decoded_blocks.append(reverse_codebook[current])
            current = ""
    return decoded_blocks        

# Decoding part
decoded_blocks = decode(encoded_bits, codes)
decoded_sequence = []
for block in decoded_blocks:
    decoded_sequence.extend(list(block))

decoded_sequence_string = ''.join(decoded_sequence)    
print("Decoded sequence (first 100 characters): ", decoded_sequence[:100])

original_sequence_string = ''.join(sequence[:len(decoded_sequence)])
if decoded_sequence_string == original_sequence_string:
    print("Decoding successfull!")
else: 
    print("Decoding failed! Mismatch in the decoded sequence.")    