"""
Byte Pair Encoding (BPE) Tokenization - From Scratch
Assignment 1 - NLU, Problem 2
Ashutosh (P25CS0002)
Uses only: collections, re, sys (standard library)
"""

import re
import sys
from collections import Counter


def get_pairs(word_tokens):
    """Get all adjacent pairs of tokens in a word."""
    pairs = []
    for i in range(len(word_tokens) - 1):
        pairs.append((word_tokens[i], word_tokens[i + 1]))
    return pairs


def train_bpe(corpus_path, K):
    """
    Train BPE tokenizer on corpus.
    
    Args:
        corpus_path: Path to corpus file (one sentence/line per line)
        K: Number of merge operations
    
    Returns:
        vocabulary: dict mapping token_id -> token_string
    """
    # Read corpus
    with open(corpus_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pre-tokenize: split each line into words, each word as list of chars + </w>
    END_TOKEN = '</w>'
    word_tokens_list = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        words = re.split(r'\s+', line)
        for word in words:
            if word:
                tokens = list(word) + [END_TOKEN]
                word_tokens_list.append(tokens)
    
    # Initial vocabulary: unique characters + end token
    all_chars = set()
    for tokens in word_tokens_list:
        for t in tokens:
            all_chars.add(t)
    
    vocab = {}
    for i, char in enumerate(sorted(all_chars)):
        vocab[i] = char
    
    next_id = len(vocab)
    
    # BPE merge loop
    for _ in range(K):
        # Count all pairs
        pair_counts = Counter()
        for tokens in word_tokens_list:
            for pair in get_pairs(tokens):
                pair_counts[pair] += 1
        
        if not pair_counts:
            break
        
        # Most frequent pair
        best_pair, best_count = pair_counts.most_common(1)[0]
        if best_count < 1:
            break
        
        # Merge: replace pair with new token in all words
        merged_token = best_pair[0] + best_pair[1]
        vocab[next_id] = merged_token
        
        new_word_tokens_list = []
        for tokens in word_tokens_list:
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == best_pair:
                    new_tokens.append(merged_token)
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_word_tokens_list.append(new_tokens)
        
        word_tokens_list = new_word_tokens_list
        next_id += 1
    
    return vocab


def main():
    if len(sys.argv) < 2:
        print("Usage: python P25CS0002_prob2.py corpus.txt [K]")
        print("  corpus.txt: training corpus (one sentence per line)")
        print("  K: number of merges (default: 100)")
        sys.exit(1)
    
    corpus_path = sys.argv[1]
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    
    vocab = train_bpe(corpus_path, K)
    
    print("Vocabulary (token_id -> token_string):")
    print("-" * 40)
    for tid, token in sorted(vocab.items()):
        # Show special chars escaped for readability
        display = repr(token) if token in (' ', '\n', '\t') or token == '</w>' else token
        print(f"  {tid}: {display}")
    print("-" * 40)
    print(f"Vocabulary size: {len(vocab)}")


if __name__ == "__main__":
    main()
