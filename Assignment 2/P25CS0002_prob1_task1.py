"""
PA1 Task 1 — clean up IITJ text files, print stats, save a word cloud.

Put your .txt files in IITJ_corpus/ next to this script, then:
    pip install -r requirements.txt
    python PA1_Task1.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from langdetect import LangDetectException, detect
from wordcloud import STOPWORDS, WordCloud

# I used regex for tokens instead of NLTK — less setup, and it still counts as
# tokenization for the lab. Swap in nltk.word_tokenize if your instructor wants it.

BASE = Path(__file__).resolve().parent
CORPUS_DIR = BASE / "IITJ_corpus"
OUTPUT_DIR = BASE / "PA1_Task1_output"

# paragraphs shorter than this are usually garbage (headers, "na", etc.)
MIN_PARAGRAPH_CHARS = 40
# skip token lists that are basically nothing after cleaning
MIN_TOKENS_PER_CHUNK = 5

# junk you see a lot in scraped pages / PDFs — strip before we count words
BOILERPLATE_PATTERNS = [
    r"cookie[s]?\s+policy",
    r"privacy\s+policy",
    r"all\s+rights\s+reserved",
    r"copyright\s+©?\s*\d{4}",
    r"skip\s+to\s+(main\s+)?content",
    r"javascript\s+is\s+(disabled|required)",
    r"loading\.\.\.",
    r"\bpage\s+\d+\s+of\s+\d+\b",
    r"https?://\S+",
    r"\S+@\S+\.\S+",
    r"\+?[\d\s\-\(\)]{7,}",
    r"[^\x00-\x7F]+",
]


def scrub_boilerplate(text: str):
    out = text
    for pat in BOILERPLATE_PATTERNS:
        out = re.sub(pat, " ", out, flags=re.IGNORECASE)
    return out


def words_from_text(s: str):
    # grab letter runs; already lowercased and punctuation mostly gone
    return re.findall(r"[a-z]{2,}", s)


def clean_paragraph(para: str):
    t = scrub_boilerplate(para)
    t = t.lower()
    t = re.sub(r"[^a-z0-9\s']", " ", t)
    t = re.sub(r"'\s", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return words_from_text(t)


def paragraphs_from_file(raw: str):
    bits = re.split(r"\n{2,}|\r\n", raw)
    return [b.strip() for b in bits if len(b.strip()) >= MIN_PARAGRAPH_CHARS]


def load_txts(folder: Path):
    if not folder.is_dir():
        raise FileNotFoundError(f"Can't find folder: {folder}")

    docs = []
    for p in sorted(folder.glob("*.txt")):
        text = p.read_text(encoding="utf-8", errors="replace")
        docs.append(
            {
                "id": p.stem,
                "path": str(p),
                "raw": text,
            }
        )
    return docs


def build_corpus(docs: list[dict]):
    """Returns (lines of tokens, one stat dict per input file)."""
    all_lines: list[list[str]] = []
    per_file = []

    for d in docs:
        chunks: list[list[str]] = []
        tokens_here = 0

        for para in paragraphs_from_file(d["raw"]):
            toks = clean_paragraph(para)
            if len(toks) < MIN_TOKENS_PER_CHUNK:
                continue
            chunks.append(toks)
            tokens_here += len(toks)

        all_lines.extend(chunks)
        per_file.append(
            {
                "file": d["id"],
                "chunks": len(chunks),
                "tokens": tokens_here,
            }
        )

    return all_lines, per_file


def stopwords_for_report():
    """English stopwords + a few site-specific token"""
    s = set(STOPWORDS)
    s.update(["iit", "jodhpur", "iitj", "www", "http", "https", "ac", "in"])
    return s


def top_content_words(freq: Counter, stop: set[str], n: int = 50):
    """
    Most common words after dropping stopwords.

    Raw frequency lists are dominated by the/is/and — that's normal. For the
    write-up and JSON we report *content* words instead.
    """
    # Make a list of (word, count) pairs, ignoring stopwords and short words
    ranked = []
    for word, count in freq.items():
        if word not in stop and len(word) > 2:
            ranked.append((word, count))
    # Sort by count, highest first
    ranked.sort(key=lambda x: -x[1])
    # Return the top n
    return ranked[:n]


def stats(lines: list[list[str]], per_file: list[dict]):
    flat = [w for line in lines for w in line]
    freq = Counter(flat)
    stop = stopwords_for_report()

    return {
        "total_documents": len(per_file),
        "total_chunks": len(lines),
        "total_tokens": len(flat),
        "vocabulary_size": len(set(flat)),
        # still saved for reference (will be noisy with function words)
        "top_50_including_stopwords": freq.most_common(50),
        "top_50": top_content_words(freq, stop, 50),
        "per_file": per_file,
    }


def make_wordcloud(freq: Counter, out: Path):
    banned = stopwords_for_report()
    filtered = {w: n for w, n in freq.items() if w not in banned and len(w) > 2}

    cloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        max_words=150,
        colormap="ocean",
    ).generate_from_frequencies(filtered)

    plt.figure(figsize=(14, 7))
    plt.imshow(cloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("IIT Jodhpur Ashu corpus — common words", fontsize=14)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"  saved word cloud: {out}")


def main():


    print(f"\nReading .txt from Ashu Corpus")
    docs = load_txts(CORPUS_DIR)

    print("\nRemoval of the boilerplate text and the formating artifacts + tokenization + English processing(lowercase + removal of the punctuation) ")
    lines, per_file = build_corpus(docs)

    s = stats(lines, per_file)

    print("\n------ corpus details ------")
    print(f"total documents:     {s['total_documents']}")
    print(f"total chunks:        {s['total_chunks']}")
    print(f"total tokens:        {s['total_tokens']:,}")
    print(f"vocabulary size:    {s['vocabulary_size']:,}")
    print("\nper file:")
   
   
    for row in s["per_file"]:
        print(f"  {row['file'][:36]:<36}  chunks={row['chunks']:<5}  tokens={row['tokens']:,}")
   
    print("\nTop 15 content words:")
    for w, c in s["top_50"][:15]:
        print(f"  {w:<20} {c}")
    

    txt_out = OUTPUT_DIR / "clean_corpus.txt"
    with open(txt_out, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(" ".join(line) + "\n")
    print(f"\nWrote {txt_out}")

    json_out = OUTPUT_DIR / "corpus_statistics.json"
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_documents": s["total_documents"],
                "total_chunks": s["total_chunks"],
                "total_tokens": s["total_tokens"],
                "vocabulary_size": s["vocabulary_size"],
                "top_50_words_content_only": s["top_50"],
                "top_50_words_including_stopwords": s["top_50_including_stopwords"],
                "per_document": s["per_file"],
            },
            f,
            indent=2,
        )
    print(f"Wrote {json_out}")

    freq = Counter(w for line in lines for w in line)
    make_wordcloud(freq, OUTPUT_DIR / "wordcloud.png")

    print(f"\nAll done. Look in: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
