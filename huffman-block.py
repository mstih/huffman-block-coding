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

#Generate the sequence
sequence = random.choices(symbols, weights=p, k=1000 )
print("####################################################\n")
print(f'Random sequence: {"".join(sequence)}\n')
print("####################################################\n")

#combine the letters into blocks from the sequence
blocks = []
for i in range(len(sequence) - 1):
    block = sequence[i] + sequence[i+1]
    blocks.append(block)

block_count = {}
for b in blocks:
    if b in block_count:
        block_count[b] += 1
    else:
        block_count[b] = 1    

# Calculate the probability of these new blocks
total_blocks = len(blocks)   
block_probs = {}
for b in block_count:
    block_probs[b] = block_count[b] / total_blocks 

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


codes = {}
for item in huffman_list[0][1:]:
    codes[item[0]] = item[1]
print(f'Codes: {codes}\n')    
print("####################################################\n")

average_len = 0
for b in block_probs:
    average_len += block_probs[b] * len(codes[b])

# Compression ratio calculated
compression_ratio = 16 / average_len

print("Avg. codeword length: ", round(average_len, 2), "bits")
print("Compression ratio: ", round(compression_ratio, 2), "x")

# Encode the sequence using the Huffman codes
encoded_bits = ""
for i in range(len(sequence) - 1):
    pair = sequence[i] + sequence[i + 1]
    if pair in codes:
        encoded_bits += codes[pair]

# Print the encoded bit sequence (first 200 bits for preview)
print("Encoded sequence (first 200 bits): ", encoded_bits[:200], '...')