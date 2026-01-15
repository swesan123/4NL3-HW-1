import nltk
import re
import argparse
import os
import matplotlib.pyplot as plt

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter



def read_text(file_path: str) -> str:
    with open(f"{file_path}", "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    return text

def tokenize(text: str) -> list[str]:
    tokens: list[str] = re.split(r"\s+", text)
    tokens = [t for t in tokens if t]
    return tokens

def count_tokens(tokens: list[str]) -> list[tuple[str, int]]:
    counts = Counter(tokens)
    return counts.most_common()


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
        help="Remove tokens containing digits (e.g., timestamps, PIDs, numeric identifiers)"
    )

    args = parser.parse_args()

    if args.stem and args.lemmatize:
        parser.error("Please choose only one of -stem or -lemmatize.")

    return args

def build_suffix(args) -> str:
    parts = []
    if args.lowercase:
        parts.append("lowercase")
    if args.myopt:
        parts.append("myopt")
    if args.stopwords:
        parts.append("stopwords")
    if args.stem:
        parts.append("stem")
    if args.lemmatize:
        parts.append("lemmatize")
    return "_".join(parts) if parts else "raw"


def main():
    args = parse_args()
    
    path: str = args.input_file
    text: str = read_text(path)
    tokens: list[str] = tokenize(text)

    os.makedirs("output", exist_ok=True)


    # Lowercasing
    if args.lowercase:
        tokens = [t.lower() for t in tokens]

    # my option to remove numbers
    if args.myopt:
        tokens = [t for t in tokens if not any(c.isdigit() for c in t)]

    # Stopword removal
    if args.stopwords:
        stop_words = set(stopwords.words("english"))
        tokens = [t for t in tokens if t not in stop_words]

    # Stemming OR lemmatization
    
    if args.stem:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    elif args.lemmatize:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]

    counts: list[tuple[str, int]] = count_tokens(tokens)

    for token, freq in counts:
        print(token, freq)
    
    suffix = build_suffix(args)

    out_file = f"output/tokens_{suffix}.txt"

    with open(out_file, "w", encoding="utf-8") as f:
        for token, freq in counts:
            f.write(f"{token}\t{freq}\n")
    
    print(f"Saved token counts to {out_file}")

    if args.analyze:
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


    