"""
Naive Bayes Sentiment Classifier - From Scratch
Assignment 1 - NLU, Problem 3
Ashutosh (P25CS0002)
Uses only Python standard library.
"""

import random
import math


def tokenize(text):
    """Whitespace tokenization, lowercase."""
    return text.strip().lower().split()


def load_data(pos_path='pos.txt', neg_path='neg.txt'):
    """Load positive and negative sentences."""
    pos_sentences = []
    with open(pos_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                pos_sentences.append(line)
    
    neg_sentences = []
    with open(neg_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                neg_sentences.append(line)
    
    return pos_sentences, neg_sentences


def train_test_split(pos_sentences, neg_sentences, test_ratio=0.2, seed=42):
    """Split data into train and validation sets."""
    random.seed(seed)
    
    pos_shuffled = pos_sentences.copy()
    neg_shuffled = neg_sentences.copy()
    random.shuffle(pos_shuffled)
    random.shuffle(neg_shuffled)
    
    n_pos = len(pos_shuffled)
    n_neg = len(neg_shuffled)
    n_pos_test = max(1, int(n_pos * test_ratio))
    n_neg_test = max(1, int(n_neg * test_ratio))
    
    pos_train = pos_shuffled[:-n_pos_test]
    pos_test = pos_shuffled[-n_pos_test:]
    neg_train = neg_shuffled[:-n_neg_test]
    neg_test = neg_shuffled[-n_neg_test:]
    
    return pos_train, pos_test, neg_train, neg_test


class NaiveBayesClassifier:
    """Naive Bayes for sentiment classification with Laplace smoothing."""
    
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # Laplace smoothing
        self.p_pos = 0.0
        self.p_neg = 0.0
        self.word_count_pos = {}  # word -> count in positive
        self.word_count_neg = {}  # word -> count in negative
        self.total_words_pos = 0
        self.total_words_neg = 0
        self.vocab = set()
    
    def fit(self, pos_sentences, neg_sentences):
        """Train the classifier."""
        # Tokenize and count
        for sent in pos_sentences:
            words = tokenize(sent)
            for w in words:
                self.word_count_pos[w] = self.word_count_pos.get(w, 0) + 1
                self.total_words_pos += 1
                self.vocab.add(w)
        
        for sent in neg_sentences:
            words = tokenize(sent)
            for w in words:
                self.word_count_neg[w] = self.word_count_neg.get(w, 0) + 1
                self.total_words_neg += 1
                self.vocab.add(w)
        
        # Prior probabilities
        n_pos = len(pos_sentences)
        n_neg = len(neg_sentences)
        self.p_pos = n_pos / (n_pos + n_neg)
        self.p_neg = n_neg / (n_pos + n_neg)
        
        self.vocab_size = len(self.vocab)
    
    def _log_prob_word_given_class(self, word, is_positive):
        """P(word | class) with Laplace smoothing, in log space."""
        if is_positive:
            count = self.word_count_pos.get(word, 0)
            total = self.total_words_pos
        else:
            count = self.word_count_neg.get(word, 0)
            total = self.total_words_neg
        
        # Laplace: (count + alpha) / (total + alpha * vocab_size)
        prob = (count + self.alpha) / (total + self.alpha * self.vocab_size)
        return math.log(prob)
    
    def predict(self, sentence):
        """Predict sentiment: POSITIVE or NEGATIVE."""
        words = tokenize(sentence)
        if not words:
            return "POSITIVE" if self.p_pos >= self.p_neg else "NEGATIVE"
        
        log_prob_pos = math.log(self.p_pos)
        log_prob_neg = math.log(self.p_neg)
        
        for w in words:
            log_prob_pos += self._log_prob_word_given_class(w, True)
            log_prob_neg += self._log_prob_word_given_class(w, False)
        
        return "POSITIVE" if log_prob_pos >= log_prob_neg else "NEGATIVE"
    
    def evaluate(self, pos_sentences, neg_sentences):
        """Compute accuracy on validation set."""
        correct = 0
        total = 0
        for sent in pos_sentences:
            if self.predict(sent) == "POSITIVE":
                correct += 1
            total += 1
        for sent in neg_sentences:
            if self.predict(sent) == "NEGATIVE":
                correct += 1
            total += 1
        return correct / total if total > 0 else 0.0


def main():
    print("Naive Bayes Sentiment Classifier")
    print("=" * 40)
    
    # Load data
    pos_sentences, neg_sentences = load_data()
    print(f"Loaded {len(pos_sentences)} positive, {len(neg_sentences)} negative sentences")
    
    # Split
    pos_train, pos_val, neg_train, neg_val = train_test_split(
        pos_sentences, neg_sentences, test_ratio=0.2
    )
    print(f"Train: {len(pos_train)} pos, {len(neg_train)} neg")
    print(f"Validation: {len(pos_val)} pos, {len(neg_val)} neg")
    
    # Train
    clf = NaiveBayesClassifier(alpha=1.0)
    clf.fit(pos_train, neg_train)
    
    # Validation accuracy
    acc = clf.evaluate(pos_val, neg_val)
    print(f"Validation accuracy: {acc:.2%}")
    print("=" * 40)
    print("\nEnter a sentence for sentiment prediction (empty to quit):\n")
    
    # Interactive mode
    while True:
        try:
            sentence = input("You: ").strip()
        except EOFError:
            break
        if not sentence:
            print("Goodbye!")
            break
        pred = clf.predict(sentence)
        print(f"Sentiment: {pred}\n")


if __name__ == "__main__":
    main()
