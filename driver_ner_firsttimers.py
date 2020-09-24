from gutenberg import *


pp = pprint.PrettyPrinter(indent=2)

#######################

story = 'The Valley of Fear'

# Select part(s)
spans = get_parts(get_corpus(story).lower())  # n = Part
span = spans[0]  # [i] = Part i+1
# span = None  # all Parts or if no Parts

# Per chapter
story_spans, story_counts = ner_story_with_chapters(story, span)
plot_ner_counts_story_with_chapters(story, story_counts, show=True)

# Full story
# story_spans, story_counts = ner_story(story, span)
# plot_ner_counts_story(story, story_counts, show=True)

# pp.pprint(story_spans)
# pp.pprint(story_counts)

#######################

# story = 'A Study in Scarlet'

# Select part(s)
# spans = get_parts(get_corpus(story).lower())  # n = Part
# span = spans[0]  # [i] = Part i+1

# Per chapter
# story_spans, story_counts = ner_story_with_chapters(story, span)
# plot_ner_counts_story_with_chapters(story, story_counts, show=True)

# Full story
# story_spans, story_counts = ner_story(story, span, show=True)
# plot_ner_counts_story(story, story_counts)

# pp.pprint(story_spans)
# pp.pprint(story_counts)

#######################

# story = 'The Sign of the Four'
# story = 'The Hound of the Baskervilles'

# Per chapter
# story_spans, story_counts = ner_story_with_chapters(story)
# plot_ner_counts_story_with_chapters(story, story_counts, show=True)

# Full story
# story_spans, story_counts = ner_story(story)
# plot_ner_counts_story(story, story_counts, show=False)

# pp.pprint(story_spans)
# pp.pprint(story_counts)

#######################

# story = 'The Boscombe Valley Mystery'
# span = get_adventures(get_corpus(story).lower(), n=4)[0]

# Per paragraph
# story_spans, story_counts = ner_story_with_paragraphs(story, span)
# plot_ner_counts_story_with_paragraphs(story, story_counts, show=False)

# Full story
# story_spans, story_counts = ner_story(story, span)
# plot_ner_counts_story(story, story_counts, show=True)

# pp.pprint(story_spans)
# pp.pprint(story_counts)


########################
# First-Time Occurrences
########################

# story = 'The Valley of Fear'
# story = 'The Sign of the Four'
# story = 'The Hound of the Baskervilles'

# Get span of first occurrence
# first_occurrences = get_first_occurrences(story_spans)
# print(first_occurrences)

# Get corpus span
# text = get_corpus(story).lower()
# spans = get_text(text)
# span = spans[0]

# Find location of first span
# first_locations = {}
# for character_type, characters in first_occurrences.items():
#     first_locations[character_type] = {}
#     for character in characters:
#         location = get_span_location_with_chapters(text, span, first_occurrences[character_type][character], verbose=False)
#         first_locations[character_type][character] = location
#
# pp.pprint(first_locations)

#######################

# story = 'A Study in Scarlet'

# Get span of first occurrence
# first_occurrences = get_first_occurrences(story_spans)
# print(first_occurrences)

# Get corpus span
# text = get_corpus(story).lower()
# spans = get_parts(text)  # n = Part
# span = spans[0]  # [i] = Part i+1

# Find location of first span
# first_locations = {}
# for character_type, characters in first_occurrences.items():
#     first_locations[character_type] = {}
#     for character in characters:
#         location = get_span_location_with_chapters(text, span, first_occurrences[character_type][character], verbose=False)
#         first_locations[character_type][character] = location
#
# pp.pprint(first_locations)

#######################

# story = 'The Boscombe Valley Mystery'

# Get span of first occurrence
# first_occurrences = get_first_occurrences(story_spans)
# print(first_occurrences)

# Get corpus span
# text = get_corpus(story).lower()
# spans = get_adventures(text, n=4)
# span = spans[0]

# Find location of first span
# first_locations = {}
# for character_type, characters in first_occurrences.items():
#     first_locations[character_type] = {}
#     for character in characters:
#         location = get_span_location(text, span, first_occurrences[character_type][character], verbose=False)
#         first_locations[character_type][character] = location
#
# pp.pprint(first_locations)
