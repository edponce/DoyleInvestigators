import os
import re
import collections
import urllib.request
import urllib.parse
import numpy as np
import seaborn as sns
import pandas
import matplotlib.pyplot as plt


CORPUS_URL = {
    'The Valley of Fear': 'http://www.gutenberg.org/files/3289/3289.txt',
    'A Study of Scarlet': 'http://www.gutenberg.org/files/244/244.txt',
    'The Sign of the Four': 'http://www.gutenberg.org/files/2097/2097.txt',
    'The Hound of the Baskervilles': 'http://www.gutenberg.org/files/2852/2852.txt',
    'The Boscombe Valley Mystery': 'https://www.gutenberg.org/files/1661/1661.txt',
    'A Scandal in Bohemia': 'https://www.gutenberg.org/files/1661/1661.txt',
}


def get_corpus_from_url(url):
    with urllib.request.urlopen(url) as fd:
        text = fd.read()
        try:
            return text.decode('utf-8')
        except UnicodeDecodeError:
            return text.decode('iso-8859-1')


def get_corpus_from_file(file):
    with open(file) as fd:
        return fd.read()


def get_corpus(key):
    def validate_url(url):
        parsed_url = urllib.parse.urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc, parsed_url.path])

    # Check if a filename was provided
    if os.path.isfile(key):
        return get_corpus_from_file(key)
    else:
        if key in CORPUS_URL:
            file = os.path.basename(CORPUS_URL[key])
            if os.path.isfile(file):
                return get_corpus_from_file(file)

    # Check if a URL was provided
    if validate_url(key):
        return get_corpus_from_url(key)
    else:
        if key in CORPUS_URL:
            url = CORPUS_URL[key]
            if validate_url(url):
                return get_corpus_from_url(url)

    raise Exception(f"corpus '{key}' not found")


def get_newline_index(text):
    """Find the index of the first newline in the text.
    This is used to skip/correct one newline at beginning of headings.
    """
    match = re.match(r'[ \t\r]*\n', text)
    return match.end() if match else 0


def get_gutenberg_start_heading(text, span=None):
    """Find Gutenberg's start tag (and producer, if available).

    Notes:
        * re.match() searches at the beginning of strings, but there are
          certain character combinations that are not considered strings,
          and thus need to use re.search(), even if it is at the beginning
          of line. An example are the asterisks in the Gutenberg START
          tag.
    """
    if not span:
        span = (0, len(text))

    match = re.search(
        r'(\s*\n){2,}'  # pre-whitespace, no indentation
        r'\*{3}\s*'  # 3 asterisks
        r'start[^\r\n]+'  # tag text
        r'\s*\*{3}'  # 3 asterisks
        r'(\s*\nproduced by.+)?'  # producer line
        r'(\s*\n){2,}',  # post-whitespace
        text[span[0]:span[1]],
    )

    if match:
        span = match.span()
        offs = get_newline_index(text[span[0]:span[1]])
        return span[0] + offs, span[1]


def get_gutenberg_end_heading(text, span=None):
    """Find Gutenberg's end tag (and transcriber's notes, if available).

    Notes:
        * Duplicate/similar Gutenberg end tags.
        * Use a newline before transcriber note to prevent matching similar
          (but indented) notes at beginning of text.
        * Use DOTALL flag to match transcriber's notes across multiple lines.
          But be wary that using DOTALL prevents the use of '.+' for other
          cases, so use '[^\r\n]' instead.
    """
    if not span:
        span = (0, len(text))

    match = re.search(
        r'('
        r'(\s*\n){2,}'  # pre-whitespace, no indentation
        r'(original transcriber.+\s*\n)?'  # transcriber notes
        r'end[^\r\n]+'  # duplicate/similar tag text
        r')?'
        r'\s*\n'  # pre-whitespace, no indentation
        r'\*{3}\s*'  # 3 asterisks
        r"end[^\r\n]+"  # tag text
        r'\s*\*{3}'  # 3 asterisks
        r'(\s*\n){2,}',  # post-whitespace
        text[span[0]:span[1]],
        flags=re.DOTALL,
    )

    if match:
        span = match.span()
        offs = get_newline_index(text[span[0]:span[1]])
        return span[0] + offs, span[1]


def get_named_headings(text, name, span=None):
    """Find named headings with title."""
    if not span:
        span = (0, len(text))

    spans = [
        (match.start() + span[0], match.end() + span[0])
        for match in re.finditer(
            r'(\s*\n){2,}'  # pre-whitespace, no indentation
            r'('
            fr'{name}[ \t]+(\d+|[ivxlcd]+)'  # label with Arabic or Roman numbering
            r'(-+|\.)?'  # label-title delimiter
            r'((\s*\n){2})?'  # whitespace for titles two line apart
            r'.*(\r?\n.*)?'  # title (muti-line support)
            r'|'  # cases: name # \s* label, # name/label
            r'(\d+|[ivxlcd]+)'  # label with Arabic or Roman numbering
            r'(-+|\.)?'  # label-title delimiter
            fr'[ \t]+.*{name}.*'  # label with name
            r')'
            r'(\s*\n){2,}',  # post-whitespace
            text[span[0]:span[1]],
        )
    ]

    if spans:
        _spans = []
        for _span in spans:
            offs = get_newline_index(text[_span[0]:_span[1]])
            _spans.append((_span[0] + offs, _span[1]))
        return _spans


def get_numbered_headings(text, span=None):
    """Find numbered headings with no title."""
    if not span:
        span = (0, len(text))

    spans = [
        (match.start() + span[0], match.end() + span[0])
        for match in re.finditer(
            r'(\s*\n){2,}'  # pre-whitespace, no indentation
            fr'(\d+|[ivxlcd]+)'  # label with Arabic or Roman numbering
            r'(-+|\.)'  # label-title delimiter
            r'(\s*\n){2,}',  # post-whitespace
            text[span[0]:span[1]]
        )
    ]

    if spans:
        _spans = []
        for _span in spans:
            offs = get_newline_index(text[_span[0]:_span[1]])
            _spans.append((_span[0] + offs, _span[1]))
        return _spans


def get_epilogue_heading(text, span=None):
    if not span:
        span = (0, len(text))

    match = re.search(
        r'(\s*\n){2,}'  # pre-whitespace, no indentation
        r'epilogue'  # tag text
        r'(\s*\n){2,}',  # post-whitespace
        text[span[0]:span[1]]
    )

    if match:
        span = match.span()
        offs = get_newline_index(text[span[0]:span[1]])
        return span[0] + offs, span[1]


def get_headings_map(
    text,
    headings=['part', 'chapter', 'adventure', 'epilogue', 'numbered'],
):
    """Create a list of all heading spans, guarantees at least one set
    of bounding spans.

    Args:
        headings (str, List[str]): Heading names to search for.
    """
    if not isinstance(headings, list):
        headings = [headings]

    headings_map = {}
    _headings_map = {}

    # Always available heading, all text
    text_heading = '_text_'

    # Ensure there is always a begin "span"
    start_span = get_gutenberg_start_heading(text)
    if not start_span:
        start_span = 0, 0

    # Ensure there is always an end "span"
    end_span = get_gutenberg_end_heading(text)
    if not end_span:
        end_span = len(text), len(text)
    headings_map[text_heading] = [start_span, end_span]
    if text_heading in headings:
        headings.remove(text_heading)

    # Optional
    span = get_epilogue_heading(text)
    if span:
        heading = 'epilogue'
        _headings_map[heading] = [span, headings_map[text_heading][1]]
        if heading in headings:
            headings_map[heading] = _headings_map[heading]
            headings.remove(heading)

    # Optional
    spans = get_numbered_headings(text)
    if spans:
        heading = 'numbered'
        _headings_map[heading] = spans
        if heading in headings:
            headings_map[heading] = _headings_map[heading]
            headings.remove(heading)

    # Optional
    if headings:
        for heading in headings:
            spans = get_named_headings(text, heading)
            if spans:
                headings_map[heading] = spans
                if 'epilogue' in _headings_map:
                    headings_map[heading].append(_headings_map['epilogue'][0])
                else:
                    headings_map[heading].append(headings_map[text_heading][1])
    return headings_map


def get_rois(text, name=None, num=None, *, headings_map=None):
    """Get span bounding a ROI.

    Args:
        name (str): ROI

        num (int, Iterable[int]): Number of ROI, [1,N]
    """
    if not headings_map:
        headings_map = get_headings_map(text)

    # Always available heading, all text
    text_heading = '_text_'

    rois = []
    if not name:
        rois = [(headings_map[text_heading][0][1], headings_map[text_heading][1][0])]
    elif name in headings_map:
        spans = headings_map[name]
        if num is None:
            rois = [
                (spans[i][1], spans[i + 1][0])
                for i in range(len(spans) - 1)
            ]
        else:
            rois = [
                (spans[i - 1][1], spans[i][0])
                for i in ([num] if isinstance(num, int) else num)
                if i >= 1 and i < (len(spans))
            ]

    if rois:
        # If necessary, skip last inner heading
        _rois = []
        for roi in rois:
            value = roi[1]
            for spans in headings_map.values():
                for span in spans:
                    if roi[1] > span[0] and roi[1] <= span[1]:
                        value = span[0]
            _rois.append((roi[0], value))
        return _rois


def get_text(text, span):
    if isinstance(span[0], int):
        span = [span]

    roi = ''
    for _span in span:
        roi += text[_span[0]:_span[1]]
    return roi


def tokenize(text, span, regex, *, use_remaining=False):
    def _get_tokens(text):
        return [
            match.span()
            for match in re.finditer(regex, text)
        ]

    # Get tokens from text
    # Add base offset to tokens' spans
    tokens = [
        (tok_span[0]+span[0], tok_span[1]+span[0])
        for tok_span in _get_tokens(text[span[0]:span[1]])
    ]

    if use_remaining:
        if tokens:
            # Extend last token to end of text
            tokens[-1] = tokens[-1][0], span[1]
        else:
            # Consider all text as the token
            tokens = [span]

    return tokens


def get_paragraphs(text, span):
    return tokenize(
        text,
        span,
        r'('
        r'([^\r\n]+\r?\n)+'  # (regular text with newline)+
        r'('
        r'(\r?\n)+'  # (newline)+
        r'[^a-zA-Z]'  # non-alpha character: quote, number, etc.
        r')?'  # handles case of multiple newlines but still same paragraph
        r')+',  # (full regex)+
        use_remaining=True,
    )


def get_sentences(text, span):
    return tokenize(
        text,
        span,
        # r'[^.;!?\s]+'  # sentence begins without punctuations nor whitespace
        # r'('
        # r'((\r?\n)?[^.;!?\r\n]+)?'  # sentence can be across newlines
        # r'[.;!?][\'"]?'  # sentence ends with a punctuation (and quotes)

        # r'(M[rR][sS]?\.\s)?M?'
        # r')',

        r'(([^\.\r\n;M!]+\n?)+(.")?(M[rR][sS]?\.\s)?(M)?)+|M[rR][sS]?\.\s([^\.;M!]+(.")?(M[rR][sS]?\.\s)?(M)?)+',
    )


def get_tokens(text, span):
    return tokenize(
        text,
        span,
        r'\w+'  # compound alphanumeric words
        r'('
        r"'\w+"  # contractions
        r'|(-\w+)+'  # tokens with inlined dashes
        r')'
        r'|\w+'  # single alphanumeric words
        r'|\$?-?\d+(,\d+)*(\.\d+)?',  # numbers, decimals, monetary
    )


def get_keywords_map(text, span, keywords, *, spans_map=None):
    if spans_map is None:
        spans_map = collections.defaultdict(list)

    # NOTE: Doesn't handle cases where keyword is a subpart of a non-keyword token)
    for kw in keywords:
        spans_map[kw].extend(tokenize(
            text,
            span,
            fr'{kw}',  # exact search
        ))
    return spans_map


def generate_frequency_map(spans_map, *, threshold=None):
    freq = collections.defaultdict(int)
    for k, v in spans_map.items():
        if threshold is None or len(v) >= threshold:
            freq[k] = len(v)
    return freq


def get_vocabulary(text, span, *, vocab=None):
    return (
        list(vocab) if vocab else []
    ) + [
        get_text(text, token_span)
        for token_span in get_tokens(text, span)
    ]


def get_vocabulary_map(text, span, *, spans_map=None):
    if spans_map is None:
        spans_map = collections.defaultdict(list)

    for token_span in get_tokens(text, span):
        token = get_text(text, token_span)
        spans_map[token].append(token_span)
    return spans_map


def visualize_co_occurrence(data, keywords_rows, closeness_words_columns):

    #create a dataframe from the provided data
    df = pandas.DataFrame(data, index=keywords_rows, columns=closeness_words_columns)

    #set plot size according to the number of cols and rows
    plt.figure(figsize=(len(columns_example),len(rows_example)))

    #set color of heatmap
    heatmap = sns.heatmap(df, cmap="YlGnBu", annot=True, linewidths=.5)

    #rotate text
    loc_x, labels_x = plt.xticks()
    loc_y, labels_y = plt.yticks()
    heatmap.set_xticklabels(labels_x, rotation=58)
    heatmap.set_yticklabels(labels_y, rotation=0)


def histogram_words(data, labels):
    #prepare the data to pandas
    data_ = [labels, data]
    data_ = np.asarray(data_).transpose()

    #create a dataframe from the provided data
    df = pandas.DataFrame(data_, columns=["Word", "Frequency"])
    sns.barplot(x="Word", y="Frequency", data=df, palette="Blues_d")
    plt.show()
