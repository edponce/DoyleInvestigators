from gutenberg import *


def get_negative_words(negative_words):
    """
    Get list of negative words
    """
    return [negative_words[match.start():match.end()] for match in re.finditer(r'(?<=\n)[a-zA-Z]+(?=\n)', negative_words)]
    # return [negative_words[match.start():match.end()] for match in re.finditer(r'(?<=\n)[a-zA-Z]+(?=\n)', negative_words)]


def get_top_negative_words(corpus, negative_list, *, top=20):
    """
    Get top list of negative words
    """
    frequency_list = []
    for word in negative_list:
        result_list = [match.span() for match in re.finditer(fr'(?<![a-zA-Z0-9]){word}', corpus)]
        frequency_list.append(len(result_list))
    
    # Sort results
    temp_list = np.asarray(list(zip(negative_list,frequency_list)), dtype = [('word', np.unicode_, 16), ('frequency', int)] )
    sorted_list = np.sort(temp_list, order='frequency', kind="quicksort")
    sorted_list = sorted_list[::-1]

    return sorted_list[:top]


# Get negative words
url = "https://raw.githubusercontent.com/edponce/DoyleInvestigators/develop/negative-words.txt"
negative_words = get_corpus_from_url(url)
result_negative = get_negative_words(negative_words)


story = 'The Valley of Fear'

# Get corpus (use all text between Gutenberg tags)
corpus = get_corpus(story)
corpus_l = corpus.lower()
text = get_text_from_span(corpus_l, get_text(corpus_l)[0])

# Get count
results = get_top_negative_words(text, result_negative, top=20)
print(results)


story = 'A Study in Scarlet'

# Get corpus (use all text between Gutenberg tags)
corpus = get_corpus(story)
corpus_l = corpus.lower()
spans = get_parts(corpus_l, n=1) # n = Part
text = get_text_from_span(corpus_l, spans[0])

# Get count
results = get_top_negative_words(text, result_negative, top=20)
print(results)


story = 'The Sign of the Four'

# Get corpus (use all text between Gutenberg tags)
corpus = get_corpus(story)
corpus_l = corpus.lower()
text = get_text_from_span(corpus_l, get_text(corpus_l)[0])

# Get count
results = get_top_negative_words(text, result_negative, top=20)
print(results)


story = 'The Hound of the Baskervilles'

# Get corpus (use all text between Gutenberg tags)
corpus = get_corpus(story)
corpus_l = corpus.lower()
text = get_text_from_span(corpus_l, get_text(corpus_l)[0])

# Get count
results = get_top_negative_words(text, result_negative, top=20)
print(results)


story = 'The Boscombe Valley Mystery'

# Get corpus (use all text between Gutenberg tags)
corpus = get_corpus(story)
corpus_l = corpus.lower()
spans = get_adventures(corpus_l, n=4)
text = get_text_from_span(corpus_l, spans[0])

# Get count
results = get_top_negative_words(text, result_negative, top=20)
print(results)
