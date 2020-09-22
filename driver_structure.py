from gutenberg import *


def count_text_structure(text, span=None, structure=None):
    if structure is None:
        structure = collections.defaultdict(int)

    for par_span in get_paragraphs(text, span):
        structure['Paragraphs'] += 1
        for sent_span in get_sentences(text, par_span):
            structure['Sentences'] += 1
            for tok_span in get_tokens(text, sent_span):
                structure['Words'] += 1


structures = {}

story = 'The Valley of Fear'
corpus = get_corpus(story)
text = corpus.lower()
structure = collections.defaultdict(int)
for part_span in get_parts(text):
    structure['Parts'] += 1
    for chp_span in get_chapters(text, part_span):
        structure['Chapters'] += 1
        count_text_structure(text, chp_span, structure)
structure['Epilogue'] = 1
span = get_text(text)[0]
structure['Characters'] = span[1] - span[0]
count_text_structure(text, get_epilogue(text)[0], structure)
structures[story] = structure

story = 'A Study in Scarlet'
corpus = get_corpus(story)
text = corpus.lower()
structure = collections.defaultdict(int)
for part_span in get_parts(text):
    structure['Parts'] += 1
    for chp_span in get_chapters(text, part_span):
        structure['Chapters'] += 1
        count_text_structure(text, chp_span, structure)
span = get_text(text)[0]
structure['Characters'] = span[1] - span[0]
structures[story] = structure

story = 'The Sign of the Four'
corpus = get_corpus(story)
text = corpus.lower()
structure = collections.defaultdict(int)
for chp_span in get_chapters(text):
    structure['Chapters'] += 1
    count_text_structure(text, chp_span, structure)
span = get_text(text)[0]
structure['Characters'] = span[1] - span[0]
structures[story] = structure

story = 'The Hound of the Baskervilles'
corpus = get_corpus(story)
text = corpus.lower()
structure = collections.defaultdict(int)
for chp_span in get_chapters(text):
    structure['Chapters'] += 1
    count_text_structure(text, chp_span, structure)
span = get_text(text)[0]
structure['Characters'] = span[1] - span[0]
structures[story] = structure

story = 'The Boscombe Valley Mystery'
corpus = get_corpus(story)
text = corpus.lower()
structure = collections.defaultdict(int)
span = get_adventures(text, n=4)[0]
count_text_structure(text, span, structure)
structure['Characters'] = span[1] - span[0]
structures[story] = structure

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(structures)
