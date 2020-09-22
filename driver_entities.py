from gutenberg import *


story = 'The Valley of Fear'
# story = 'A Study in Scarlet'

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

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(story_spans)
pp.pprint(story_counts)

#######################

# story = 'The Sign of the Four'
# story = 'The Hound of the Baskervilles'

# Per chapter
# story_spans, story_counts = ner_story_with_chapters(story)
# plot_ner_counts_story_with_chapters(story, story_counts)

# Full story
# story_spans, story_counts = ner_story(story)
# plot_ner_counts_story(story, story_counts)

# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(story_spans)
# pp.pprint(story_counts)

#######################

# story = 'The Boscombe Valley Mystery'
# span = get_adventures(get_corpus(story).lower(), n=4)[0]

# Per paragraph
# story_spans, story_counts = ner_story_with_paragraphs(story, span)
# plot_ner_counts_story_with_paragraphs(story, story_counts)

# Full story
# story_spans, story_counts = ner_story(story, span)
# plot_ner_counts_story(story, story_counts)
#
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(story_spans)
# pp.pprint(story_counts)
