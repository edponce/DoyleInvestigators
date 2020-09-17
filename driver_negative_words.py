from gutenberg import *


corpus = get_corpus('The Valley of Fear')
corpus_l = corpus.lower()

# Get region of interest (ROI)
roi_spans = get_rois(corpus_l)  # all text
# roi_spans = get_rois(corpus_l, 'part')  # parts
roi_span = roi_spans[0]
print(roi_spans)
print(roi_span)

# Search keywords
keywords = ['dead', 'death', 'murder', 'crime', 'hurt', 'blood', 'treasure',
            'suffer', 'guilty', 'assassin', 'suspect', 'pain']
keyword_spans = get_keywords_map(corpus_l, roi_span, keywords)

# Generate frequency table
keyword_freq = generate_frequency_map(keyword_spans, threshold=5)
print(keyword_freq)

# Plot
labels = list(keyword_freq.keys())
data = list(keyword_freq.values())
print(labels)
print(data)
histogram_words(data, labels)
