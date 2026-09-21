import re
import sys

# Maximum size of the grams to search; the flag --max N changes it (default 5)
MAX_GRAM = 5

filename = None
max_size = MAX_GRAM
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--max":
        max_size = int(sys.argv[i + 1])
        i += 2
    else:
        filename = sys.argv[i]
        i += 1

cryptogram = open(filename, "r").read()

# If the cryptogram contains numbers (cryptogram B), each number is one symbol;
# otherwise each letter is one symbol (cryptograms A and C)
if re.search(r"\d", cryptogram):
    symbols = re.findall(r"\d+", cryptogram)
else:
    symbols = [c.upper() for c in cryptogram if c.isalpha()]

# Count the frequency of each symbol in the cryptogram
frequencies = {}
for symbol in symbols:
    if symbol in frequencies:
        frequencies[symbol] += 1
    else:
        frequencies[symbol] = 1

# Calculate the total length of the cryptogram
length = len(symbols)

# Sort the frequencies in descending order
sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

# Most frequent symbols
most_frequent = [symbol for symbol, _ in sorted_frequencies[:10]]

# Index of coincidence
ic = sum(count * (count - 1) for count in frequencies.values()) / (
    length * (length - 1)
)

# Repeated bigrams, trigrams and longer grams, with their positions and the
# distances between consecutive occurrences
repetitions = {}
for size in range(2, max_size + 1):
    positions = {}
    for i in range(length - size + 1):
        gram = tuple(symbols[i : i + size])
        positions.setdefault(gram, []).append(i)

    repetitions[size] = [
        (gram, hits) for gram, hits in positions.items() if len(hits) >= 2
    ]
    repetitions[size].sort(key=lambda x: (-len(x[1]), x[0]))

# Summary statistics
print(f"Total cryptogram length: {length}")
print(f"Number of different symbols: {len(frequencies)}")
print(f"Index of coincidence: {ic:.4f}")
print(f"Most frequent symbols: {' '.join(most_frequent)}")

# Detailed information: frequency table
print("\nFrequency table (symbol | count | relative frequency):")
for symbol, count in sorted_frequencies:
    print(f"{symbol} | {count} | {count / length:.2%}")

# Detailed information: repeated bigrams, trigrams and longer grams
print("\nRepeated grams (gram | occurrences | positions | distances):")
for size in range(2, max_size + 1):
    for gram, hits in repetitions[size]:
        distances = [hits[j + 1] - hits[j] for j in range(len(hits) - 1)]
        if all(len(symbol) == 1 for symbol in gram):
            gram_text = "".join(gram)
        else:
            gram_text = " ".join(gram)
        print(
            f"[{size}-gram] {gram_text!r} | {len(hits)} | {hits} | {distances}"
        )