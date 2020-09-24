from gutenberg import *


corpus = get_corpus('The Valley of Fear')
corpus_l = corpus.lower()
spans = get_text(corpus_l)
text = get_text_from_span(corpus_l, spans[0])
print(text[:100])
print('-' * 80)

corpus = get_corpus('A Study in Scarlet')
corpus_l = corpus.lower()
spans = get_parts(corpus_l, n=1)  # n = Part
text = get_text_from_span(corpus_l, spans[0])
print(text[:100])
print('-' * 80)

corpus = get_corpus('The Sign of the Four')
corpus_l = corpus.lower()
spans = get_text(corpus_l)
text = get_text_from_span(corpus_l, spans[0])
print(text[:100])
print('-' * 80)

corpus = get_corpus('The Hound of the Baskervilles')
corpus_l = corpus.lower()
spans = get_text(corpus_l)
text = get_text_from_span(corpus_l, spans[0])
print(text[:100])
print('-' * 80)

corpus = get_corpus('The Boscombe Valley Mystery')
corpus_l = corpus.lower()
spans = get_adventures(corpus_l, n=4)
text = get_text_from_span(corpus_l, spans[0])
print(text[:100])
