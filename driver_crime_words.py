from gutenberg import *


corpus = get_corpus('The Valley of Fear')
text = corpus.lower()

# Get region of interest (ROI)
roi_span = get_text(text)  # all text
print(roi_span)

# Search keywords
keywords = [
    'dead', 'death', 'murder', 'crime', 'hurt', 'blood', 'treasure', 'suffer',
    'guilty', 'assassin', 'pain', 'theft', 'steal', 'victim', 'poison',
    'gunshot', 'criminal', 'wound', 'attack',
]
keyword_spans = get_keywords_map(text, roi_span[0], keywords)

# Generate frequency table
freq = generate_frequency_map(keyword_spans, threshold=5)
print(freq)

# Plot
labels = []
data = []
for k, v in freq.items():
    labels.append(k)
    data.append(v)

print(labels)
print(data)
barplot(data, labels)
plt.show()
