from gutenberg import *


def process_text_with_parts_chapters(text, num=None):
    for part_span in get_parts(text, n=num):
        for chp_span in get_chapters(text, part_span):
            for par_span in get_paragraphs(text, chp_span):
                for sent_span in get_sentences(text, par_span):
                    for tok_span in get_tokens(text, sent_span):
                        pass


def process_text_with_chapters(text, num=None):
    for chp_span in get_chapters(text, n=num):
        for par_span in get_paragraphs(text, chp_span):
            for sent_span in get_sentences(text, par_span):
                for tok_span in get_tokens(text, sent_span):
                    pass


def process_text_with_adventures(text, num=None):
    for adv_span in get_adventures(text, n=num):
        for par_span in get_paragraphs(text, adv_span):
            for sent_span in get_sentences(text, par_span):
                for tok_span in get_tokens(text, sent_span):
                    pass


def process_text_with_adventures_sections(text, num=None):
    for adv_span in get_adventures(text, n=num):
        for sec_span in get_numbered_sections(text, adv_span):
            for par_span in get_paragraphs(text, sec_span):
                for sent_span in get_sentences(text, par_span):
                    for tok_span in get_tokens(text, sent_span):
                        pass


def process_text(text, num1=None, num2=None):
    """Process text in a general fashion to support arbitrary story-like
    corpus.

    Corpus types:
        * Parts and chapters - single story (parts may stand by themselves)
        * Chapters - single story
        * Adventures - multiple stories
        * Adventures and numbered sections - multiple stories
        * Have epilogue - single story

    Generic structure:
        * Level 1 - parts or adventures
        * Level 2 - chapters or numbered sections
        * Paragraphs
        * Sentences
        * Tokens

    Args:
        num1 (int, List[int]): Selection for Level 1 structure.

        num2 (int, List[int]): Selection for Level 2 structure.
    """
    # Level 1 detection
    has_level1 = True
    parts = get_parts(text, n=num1)
    if parts:
        level1 = get_parts
    else:
        adventures = get_adventures(text, n=num1)
        if adventures:
            level1 = get_adventures
        else:
            has_level1 = False
            level1 = get_text

    # Level 2 detection
    if not has_level1:
        num2 = num1
        num1 = None

    chapters = get_chapters(text, n=num2)
    if chapters:
        level2 = get_chapters
    else:
        sections = get_numbered_sections(text, n=num2)
        if sections:
            level2 = get_numbered_sections
        else:
            import functools
            level2 = functools.partial(get_roi, name='_text_')

    for l1_span in level1(text, n=num1):
        for l2_span in level2(text, span=l1_span, n=num2):
            for par_span in get_paragraphs(text, l2_span):
                for sent_span in get_sentences(text, par_span):
                    for tok_span in get_tokens(text, sent_span):
                        pass


def process_epilogue(text):
    for epi_span in get_epilogue(text):
        for par_span in get_paragraphs(text, epi_span):
            for sent_span in get_sentences(text, par_span):
                for tok_span in get_tokens(text, sent_span):
                    pass


# Parts, chapters, and epilogue
# corpus = get_corpus('The Valley of Fear')
# process_text(corpus.lower())
# process_epilogue(corpus.lower())

# Parts and chapters
# corpus = get_corpus('A Study in Scarlet')
# process_text(corpus.lower())

# Chapters
# corpus = get_corpus('The Sign of the Four')
# corpus = get_corpus('The Hound of the Baskervilles')
# process_text(corpus.lower())

# Adventures
# 4 - The Boscombe Valley Mystery
# corpus = get_corpus('The Boscombe Valley Mystery')
# process_text(corpus.lower(), 4)
