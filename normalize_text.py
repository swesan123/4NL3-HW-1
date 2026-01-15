import nltk
import re
import argparse
import os
import matplotlib.pyplot as plt
import string

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter



def read_file(file_path: str) -> str:
    with open(f"{file_path}", "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text

def write_file(filename: str, header: str, lines: list[str]):
    os.makedirs("output", exist_ok=True)
    with open(f"output/{filename}", "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for line in lines:
            f.write(line + "\n")

def write_token_counts(counts: list[tuple[str, int]], total: int, suffix: str):
    lines = [f"{token}\t{freq}" for token, freq in counts]

    write_file(
        filename=f"tokens_{suffix}.log",
        header=f"The total # of tokens: {total}",
        lines=lines
    )

    print(f"Saved token counts to output/tokens_{suffix}.log")
def analyze_tokens(counts: list[tuple[str, int]], suffix: str):
    freqs = [freq for _, freq in counts]
    ranks = range(1, len(freqs) + 1)

    out_path = f"output/zipf_{suffix}.png"

    plt.figure(figsize=(8, 6))
    plt.loglog(ranks, freqs)
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.title(f"Zipf Plot ({suffix})")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Saved plot to {out_path}")


def tokenize(text: str) -> list[str]:
    tokens: list[str] = re.split(r"\s+", text)
    tokens = [t for t in tokens if t]
    return tokens

def count_tokens(tokens: list[str]) -> list[tuple[str, int]]:
    counts = Counter(tokens)
    return counts.most_common()


def apply_lowercase(tokens: list[str]) -> list[str]:
    before = tokens
    after = [t.lower() for t in tokens]

    changed = [
        f"{b} -> {a}"
        for b, a in zip(before, after)
        if b != a
    ]

    write_file(
        "lowercase.log",
        "Tokens changed by lowercase normalization:",
        changed
    )

    return after

def remove_punctuation_only(tokens: list[str]) -> list[str]:
    before = tokens
    after = [
        t for t in tokens
        if not all(c in string.punctuation for c in t)
    ]

    removed = sorted(set(before) - set(after))

    write_file(
        "punctuation_removed.log",
        "Punctuation-only tokens removed:",
        removed
    )

    return after

def remove_stopwords(tokens: list[str]) -> list[str]:
    stop_words = set(stopwords.words("english"))
    before = tokens
    after = [t for t in tokens if t not in stop_words]

    removed = sorted(set(before) - set(after))

    write_file(
        "stopwords_removed.log",
        "Stopwords removed:",
        removed
    )

    return after

def apply_stemming(tokens: list[str]) -> list[str]:
    stemmer = PorterStemmer()
    before = tokens
    after = [stemmer.stem(t) for t in tokens]

    changes = sorted(set(
        f"{b} -> {a}"
        for b, a in zip(before, after)
        if b != a
    ))

    write_file(
        "stem.log",
        "Tokens changed by stemming:",
        changes
    )

    return after

def apply_lemmatization(tokens: list[str]) -> list[str]:
    lemmatizer = WordNetLemmatizer()
    before = tokens
    after = [lemmatizer.lemmatize(t) for t in tokens]

    changes = sorted(set(
        f"{b} -> {a}"
        for b, a in zip(before, after)
        if b != a
    ))

    write_file(
        "lemmatize.log",
        "Tokens changed by lemmatization:",
        changes
    )

    return after



def parse_args():
    parser = argparse.ArgumentParser(
        description="Normalize text and count token frequencies from a plain text file."
    )
    
    # Positional argument
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input text file (plain text, UTF-8 encoded)"
    )
    

    # Boolean flags
    parser.add_argument(
        "-analyze",
        action="store_true",
        help="Generate Zipf (log-log) frequency plot and save to output directory"
    )

    parser.add_argument(
        "-lowercase",
        action="store_true",
        help="Convert all tokens to lowercase before further processing"
    )

    parser.add_argument(
        "-stem",
        action="store_true",
        help="Apply stemming to tokens using a stemmer (e.g., PorterStemmer)"
    )

    parser.add_argument(
        "-lemmatize",
        action="store_true",
        help="Apply lemmatization to tokens using a lemmatizer (e.g., WordNetLemmatizer)"
    )

    parser.add_argument(
        "-stopwords",
        action="store_true",
        help="Remove common English stopwords from the token list"
    )

    parser.add_argument(
        "-myopt",
        action="store_true",
        help="Remove punctuation-only tokens"
    )

    args = parser.parse_args()

    if args.stem and args.lemmatize:
        parser.error("Please choose only one of -stem or -lemmatize.")

    return args

def main():
    args = parse_args()
    path = args.input_file

    text = read_file(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    suffix = [filename]

    tokens = tokenize(text)

    if args.lowercase:
        suffix.append("lowercase")
        tokens = apply_lowercase(tokens)

    if args.myopt:
        suffix.append("myopt")
        tokens = remove_punctuation_only(tokens)

    if args.stopwords:
        suffix.append("stopwords")
        tokens = remove_stopwords(tokens)

    if args.stem:
        suffix.append("stem")
        tokens = apply_stemming(tokens)
    elif args.lemmatize:
        suffix.append("lemmatize")
        tokens = apply_lemmatization(tokens)

    counts = count_tokens(tokens)
    total = len(tokens)

    print(f"The total # of tokens: {total}")

    suffix = "_".join(suffix) if suffix else "raw"
    write_token_counts(counts, total, suffix)

    if args.analyze:
        analyze_tokens(counts, suffix)



if __name__ == "__main__":

    # Doesnt get installed with package
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")

    try:
        WordNetLemmatizer().lemmatize("test")
    except LookupError:
        nltk.download("wordnet")

    main()