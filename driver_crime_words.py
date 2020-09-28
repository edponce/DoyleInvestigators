import json
from gutenberg import *


pp = pprint.PrettyPrinter(indent=2)


def crime_story_with_chapters(keywords, text, span=None):
    story_spans = {}
    story_counts = {}
    for n, chp_span in enumerate(get_chapters(text, span), start=1):
        story_spans[n] = {}
        story_counts[n] = {}
        for kw in keywords:
            story_spans[n].update(search_entity(kw, text, chp_span))
        story_counts[n] = convert_spans_to_counts_map(story_spans[n])
    return story_spans, story_counts


def crime_story(keywords, text, span=None):
    story_spans = {}
    story_counts = {}
    story_spans[0] = {}
    story_counts[0] = {}
    for kw in keywords:
        story_spans[0].update(search_entity(kw, text, span))
    story_counts[0] = convert_spans_to_counts_map(story_spans[0])
    return story_spans, story_counts


def get_first_crime(story_spans):
    """Get spans of first crime occurrences."""
    firstoccurrences = {}
    for section, keywords in story_spans.items():
        for kw, spans in keywords.items():
            if kw not in firstoccurrences and spans:
                firstoccurrences[kw] = spans[0]
    return firstoccurrences


def plot_crime_counts_story_with_chapters(story, counts, *, show=False):
    ylim = (0, get_max_frequency_from_nested_map(counts))
    ns = int(np.ceil(np.sqrt(len(counts))))
    fig, axes = plt.subplots(ns, ns, constrained_layout=True)
    axes = trim_axes(axes, len(counts))
    for ax, (chp, freq) in zip(axes, counts.items()):
        # Abbreviate names for plots
        labels = []
        data = []
        for k, v in freq.items():
            labels.append(k)
            data.append(v)
        barplot(data, labels, xlabel=f'Chapter {chp}', ylim=ylim, ax=ax)
    print(f'{story}')
    if show:
        plt.show()


# Search keywords
CRIME_KEYWORDS = [
    'dead', 'death', 'murder', 'crime', 'hurt', 'blood', 'treasure', 'suffer',
    'guilty', 'assassin', 'pain', 'theft', 'steal', 'victim', 'poison',
    'gunshot', 'criminal', 'wound', 'attack',
]


###########################

jerry = False
n_story = 1

if n_story == 1:
    story = 'The Valley of Fear'
elif n_story == 2:
    story = 'A Study in Scarlet'
elif n_story == 3:
    story = 'The Sign of the Four'
elif n_story == 4:
    story = 'The Hound of the Baskervilles'
elif n_story == 5:
    story = 'The Boscombe Valley Mystery'


if n_story in (1, 3, 4):
    # Get corpus span
    corpus = get_corpus(story)
    corpus_l = corpus.lower()
    spans = get_text(corpus_l)
    span = spans[0]


    # Full story
    story_spans, story_counts = crime_story_with_chapters(CRIME_KEYWORDS, corpus_l, span)
    # plot_crime_counts_story_with_chapters(story, story_counts, show=True)

    # pp.pprint(story_spans)
    pp.pprint(story_counts)


    # Get span of first occurrence
    first_occurrences = get_first_crime(story_spans)
    # print(first_occurrences)

    # Find location of first span
    first_locations = {}
    for kw, kw_span in first_occurrences.items():
        location = get_span_location(corpus_l, span, kw_span, verbose=False)
        first_locations[kw] = location

    print(story)
    pp.pprint(first_locations)

elif n_story == 2:
    # Get corpus span
    corpus = get_corpus(story)
    corpus_l = corpus.lower()
    spans = get_parts(corpus_l, n=1)  # n = Part
    span = spans[0]


    # Full story
    story_spans, story_counts = crime_story_with_chapters(CRIME_KEYWORDS, corpus_l, span)

    #pp.pprint(story_spans)
    pp.pprint(story_counts)


    # Get span of first occurrence
    first_occurrences = get_first_crime(story_spans)
    # print(first_occurrences)

    # Find location of first span
    first_locations = {}
    for kw, kw_span in first_occurrences.items():
        location = get_span_location(corpus_l, span, kw_span, verbose=False)
        first_locations[kw] = location

    print(story)
    pp.pprint(first_locations)

elif n_story == 5:
    # Get corpus span
    corpus = get_corpus(story)
    corpus_l = corpus.lower()
    spans = get_adventures(corpus_l, n=4)
    span = spans[0]

    # Full story
    story_spans, story_counts = crime_story(CRIME_KEYWORDS, corpus_l, span)

    #pp.pprint(story_spans)
    pp.pprint(story_counts)


    # Get span of first occurrence
    first_occurrences = get_first_crime(story_spans)
    # print(first_occurrences)

    # Find location of first span
    first_locations = {}
    for kw, kw_span in first_occurrences.items():
        location = get_span_location(corpus_l, span, kw_span, verbose=False)
        first_locations[kw] = location

    print(story)
    pp.pprint(first_locations)


##############################################
# Organize Data for Jerry's Visualization Tool
##############################################

if jerry:
    data = []

    item = collections.OrderedDict()
    item['title'] = story
    item['author'] = 'Sir Arthur Conan Doyle'
    item['queryType'] = 'occurrences'
    item['question'] = 'Crime'
    item['numChapters'] = len(story_counts)

    results = collections.defaultdict(collections.OrderedDict)
    for chapter, word_map in story_counts.items():
        for word, freq in word_map.items():
            results[word][str(chapter)] = freq
            
    for word, freq_map in results.items():
        if sum(freq_map.values()) < 5:
            continue
        item['query'] = word
        item['results'] = freq_map
        data.append(copy.deepcopy(item))

    pp.pprint(data)

    with open('conan_doyle.json', 'a') as fd:
        fd.write(json.dumps(data, sort_keys=True, indent=2))
        fd.write('\n')
