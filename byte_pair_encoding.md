# Byte Pair Encoding (BPE) Tokenizer

A fast, memory-efficient implementation of the Byte Pair Encoding algorithm for subword tokenization. This implementation works directly on UTF-8 bytes, making it language-agnostic and efficient for handling any Unicode text.

## Overview

Byte Pair Encoding (BPE) is a data compression technique that iteratively replaces the most frequent pair of bytes in a sequence with a single, unused byte. In the context of NLP, it's adapted to create a subword vocabulary by:

1. Starting with raw bytes (0-255) as the base vocabulary
2. Iteratively finding and merging the most frequent adjacent token pairs
3. Adding each merged pair to the vocabulary until the desired vocabulary size is reached

## Features

- Pure Python implementation with minimal dependencies
- Works directly on UTF-8 bytes (no character encoding issues)
- Memory-efficient storage of merges and vocabulary
- Configurable vocabulary size
- Progress tracking during training
- O(n) encoding complexity for input text

## Installation

No installation required - single file implementation. Just copy `BEP.py` to your project.

Requirements:

- Python 3.7+
- Standard library only (no external dependencies)

## Quick Start

```python
from byte_pair_encode.BEP import BPETokenizer

# Initialize tokenizer
bpe = BPETokenizer(vocab_size=500)

# Train on your text
text = "Hello world! This is an example text."
bpe_ids = bpe.train(text, verbose=True)

print("Tokenized IDs:", bpe_ids)
```

## API Reference

### `BPETokenizer`

```python
class BPETokenizer:
    def __init__(self, vocab_size: int = 1000):
        """
        Initialize BPE tokenizer.

        Args:
            vocab_size: Target vocabulary size (must be > 256 as first 256 are bytes)
        """

    def train(self, text: str, verbose: bool = False) -> List[int]:
        """
        Train BPE on input text and return encoded tokens.

        Args:
            text: Input text to train on
            verbose: If True, print progress every 100 merges

        Returns:
            List of token IDs for the input text
        """
```

### Internal Methods

- `_get_stats(ids: List[int]) -> Counter`: Compute frequencies of adjacent pairs
- `_merge(ids: List[int], pair: Tuple[int, int], idx: int) -> List[int]`: Apply a merge operation

## Implementation Details

1. **Initialization** (`__init__`):

   - Sets target vocabulary size
   - Initializes empty merges dictionary and vocabulary

2. **Statistics** (`_get_stats`):

   - Uses `Counter` for efficient pair frequency counting
   - Processes adjacent token pairs in a single pass

3. **Merging** (`_merge`):

   - Single-pass token merging
   - In-place updates for memory efficiency
   - O(n) complexity where n is sequence length

4. **Training** (`train`):
   - Starts with UTF-8 byte vocabulary (0-255)
   - Iteratively finds most frequent pairs
   - Updates vocabulary and merge rules
   - Returns encoded sequence

## Memory Usage

The implementation is optimized for memory efficiency:

- Vocabulary: O(V) where V is vocab_size
- Merge rules: O(V-256) for learned merges
- Working memory during training: O(N) where N is text length

## Performance Characteristics

- Training: O(V×N) where V is desired vocab size, N is text length
- Encoding: O(N) for input text length
- Memory: O(V+N) for vocab size V and text length N

## Usage with Text Preprocessing

For best results, combine with text preprocessing:

```python
from text_preprocessing import AdvancedTextPreprocessor
from byte_pair_encode.BEP import BPETokenizer

# Preprocess text first
preprocessor = AdvancedTextPreprocessor()
clean_text = preprocessor.preprocess_pipeline(
    text,
    expand_contractions=True,
    remove_numbers=True,
    normalize_slang=True
)

# Then apply BPE
bpe = BPETokenizer(vocab_size=500)
tokens = bpe.train(clean_text, verbose=True)
```

## Limitations

1. **Vocabulary Size**

   - Must be > 256 (base byte vocabulary)
   - Practical upper limit depends on training data size

2. **Training Data**

   - Needs representative text sample
   - More data → better subword units
   - Memory usage scales with input size

3. **Current Implementation**
   - No persistence (vocabulary saving/loading)
   - No parallel processing
   - Basic progress reporting

## Future Improvements

Planned enhancements:

1. Add vocabulary persistence (save/load)
2. Implement parallel training for large datasets
3. Add support for pre-tokenization rules
4. Add vocabulary pruning options
5. Implement efficient caching for frequent sequences


## License

MIT



