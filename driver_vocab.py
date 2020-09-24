from gutenberg import *


# Generate vocabulary frequency map
vspans = get_vocabulary_map(corpus_l, spans[0])
vfreq = generate_frequency_map(vspans, threshold=20)
print(vfreq)
