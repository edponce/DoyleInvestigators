from gutenberg import *


story_n = 4


if story_n == 1:
    story = 'The Valley of Fear'

    # Select part(s)
    # spans = get_parts(get_corpus(story).lower(), n=1)  # n = Part
    # span = spans[0]  # [i] = Part i+1
    span = None  # all Parts or if no Parts

    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story, span)
    # plot_ner_counts_story_with_chapters(story, story_counts, show=False)

    # Full story
    # story_spans, story_counts = ner_story(story, span)
    # plot_ner_counts_story(story, story_counts, show=False)

    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(story_spans)
    # pp.pprint(story_counts)

elif story_n == 2:
    story = 'A Study in Scarlet'

    # Select part(s)
    spans = get_parts(get_corpus(story).lower())  # n = Part
    span = spans[0]  # [i] = Part i+1

    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story, span)
    # plot_ner_counts_story_with_chapters(story, story_counts, show=False)

    # Full story
    # story_spans, story_counts = ner_story(story, span)
    # plot_ner_counts_story(story, story_counts, show=True)

    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(story_spans)
    # pp.pprint(story_counts)

elif story_n == 3:
    story = 'The Sign of the Four'

    spans = get_text(get_corpus(story).lower())
    span = spans[0]

    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story)
    # plot_ner_counts_story_with_chapters(story, story_counts, show=False)

    # Full story
    # story_spans, story_counts = ner_story(story)
    # plot_ner_counts_story(story, story_counts, show=True)

    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(story_spans)
    # pp.pprint(story_counts)

elif story_n == 4:
    story = 'The Hound of the Baskervilles'

    spans = get_text(get_corpus(story).lower())
    span = spans[0]

    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story)
    # plot_ner_counts_story_with_chapters(story, story_counts, show=False)

    # Full story
    # story_spans, story_counts = ner_story(story)
    # plot_ner_counts_story(story, story_counts, show=True)

    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(story_spans)
    # pp.pprint(story_counts)

elif story_n == 5:
    story = 'The Boscombe Valley Mystery'

    spans = get_adventures(get_corpus(story).lower(), n=4)
    span = spans[0]

    # Per paragraph
    # story_spans, story_counts = ner_story_with_paragraphs(story, span)
    # plot_ner_counts_story_with_paragraphs(story, story_counts, show=True)

    # Full story
    story_spans, story_counts = ner_story(story, span)
    # plot_ner_counts_story(story, story_counts, show=False)

    pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(story_spans)
    # pp.pprint(story_counts)


################
# Neighbor Words
################

# print(story_spans)

# Merge perpetrators spans across story chapters/sections
perpetrators = {}
for section, characters in story_spans['perpetrators'].items():
    for character, spans in characters.items():
        if character not in perpetrators:
            perpetrators[character] = []
        perpetrators[character].extend(spans)


corpus = get_corpus(story)
corpus_l = corpus.lower()
tok_spans = get_tokens(corpus_l, span)

print(len(tok_spans))


perpetrator_neighbors_stop = get_neighbor_words_for_character(corpus_l, tok_spans, perpetrators, CHARACTERS_NAMES[story]['perpetrators'], stopwords=STOPWORDS)
# pp.pprint(perpetrator_neighbors_stop)


# Plot top neighboring words
top_n = 10

show = False
for character, freq_modes in perpetrator_neighbors_stop.items():
    for mode, freq_all in freq_modes.items():
        freq = get_frequent_items(freq_all, top_n)
        print(f'{character} - {mode}', freq)
        if freq and show:
            barplot(list(freq.values()), list(freq.keys()))
            plt.show()
