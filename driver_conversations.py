from gutenberg import *


story = 'The Valley of Fear'
corpus = get_corpus(story)
spans = get_text(corpus.lower())
conv = get_conversations(corpus, spans[0])
print(conv)

story = 'The Boscombe Valley Mystery'
corpus = get_corpus(story)
spans = get_adventures(corpus.lower(), n=4)
conv = get_conversations(corpus, spans[0])
print(conv)
