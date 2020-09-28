import json
from gutenberg import *


pp = pprint.PrettyPrinter(indent=2)


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


if n_story in (1, 2):
    # Select part(s)
    # spans = get_parts(get_corpus(story).lower(), n=1)  # n = Part
    # span = spans[0]  # [i] = Part i+1
    span = None  # all Parts or if no Parts

    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story, span)
    plot_ner_counts_story_with_chapters(story, story_counts)

    # Full story
    # story_spans, story_counts = ner_story(story, span)
    # plot_ner_counts_story(story, story_counts)

    # pp.pprint(story_spans)
    pp.pprint(story_counts)

elif n_story in (3, 4):
    # Per chapter
    story_spans, story_counts = ner_story_with_chapters(story)
    plot_ner_counts_story_with_chapters(story, story_counts)

    # Full story
    # story_spans, story_counts = ner_story(story)
    # plot_ner_counts_story(story, story_counts)

    # pp.pprint(story_spans)
    pp.pprint(story_counts)

elif n_story == 5:
    span = get_adventures(get_corpus(story).lower(), n=4)[0]

    # Per paragraph
    # story_spans, story_counts = ner_story_with_paragraphs(story, span)
    # plot_ner_counts_story_with_paragraphs(story, story_counts)

    # Full story
    story_spans, story_counts = ner_story(story, span)
    plot_ner_counts_story(story, story_counts)
    #
    # pp.pprint(story_spans)
    pp.pprint(story_counts)


##############################################
# Organize Data for Jerry's Visualization Tool
##############################################

if jerry:
    data = []

    title = story
    author = 'Sir Arthur Conan Doyle'
    query_type = 'occurrences'
    for character_type, chapter_map in story_counts.items():
        if character_type == 'detectives':
            question = 'Detective'
        elif character_type == 'perpetrators':
            question = 'Perpetrator'
        elif character_type == 'suspects':
            question = 'Other Suspects'
        else:
            continue

        item = collections.OrderedDict()
        item['title'] = title
        item['author'] = author
        item['queryType'] = query_type
        item['question'] = question
        item['numChapters'] = len(chapter_map)

        characters = CHARACTERS_NAMES[story][character_type]

        results = collections.defaultdict(collections.OrderedDict)
        aliases = {}
        for chapter, character_map in chapter_map.items():
            for character, freq in character_map.items():
                if character not in results:
                    for c in characters:
                        if c[0] == character:
                            aliases[character] = '|'.join([s.replace('_', ' ') for s in c])
                results[character][str(chapter)] = freq

        for character, freq_map in results.items():
            item['query'] = aliases[character]
            item['results'] = freq_map
            data.append(copy.deepcopy(item))


    pp.pprint(data)

    with open('conan_doyle.json', 'a') as fd:
        fd.write(json.dumps(data, sort_keys=True, indent=2))
        fd.write('\n')
