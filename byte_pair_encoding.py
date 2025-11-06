import sys
from collections import Counter
from typing import List, Tuple, Dict
# sys.path.append("your text processing module path")
# from text_preprocessing import AdvancedTextPreprocessor

class BPETokenizer:
    def __init__(self, vocab_size: int = 1000):
        self.vocab_size = vocab_size
        self.merges: Dict[Tuple[int, int], int] = {}
        self.vocab: Dict[int, bytes] = {}

    def _get_stats(self, ids: List[int]) -> Counter:
        return Counter(zip(ids, ids[1:]))

    def _merge(self, ids: List[int], pair: Tuple[int, int], idx: int) -> List[int]:
        newids = []
        i = 0
        length = len(ids)
        while i < length:
            if i < length - 1 and (ids[i], ids[i + 1]) == pair:
                newids.append(idx)
                i += 2
            else:
                newids.append(ids[i])
                i += 1
        return newids

    def train(self, text: str, verbose: bool = False):
        ids = list(text.encode("utf-8"))
        self.vocab = {i: bytes([i]) for i in range(256)}
        num_merges = self.vocab_size - 256

        for i in range(num_merges):
            stats = self._get_stats(ids)
            if not stats:
                break
            pair, freq = max(stats.items(), key=lambda x: x[1])  

            idx = 256 + i
            ids = self._merge(ids, pair, idx)
            self.merges[pair] = idx
            self.vocab[idx] = self.vocab[pair[0]] + self.vocab[pair[1]]

            if verbose and (i + 1) % 100 == 0:
                print(f"Merge {i+1}/{num_merges}: {pair} -> {idx} (freq: {freq})")

        return ids

# sample_text = """
# #     <html>Hello!!! Check out https://example.com for more info. Delhi 
# #     I can't believe it's 2024! Contact us at info@example.com or call 555-123-4567.
# #     LOL this is gr8! Btw, I'll be there ASAP. There are 123 special chars: @#$%
# #     John Smith is the CEO. I recieve alot of emails daily.</html>
# #     """
# abc = AdvancedTextPreprocessor()
# cleaned_text = abc.preprocess_pipeline(
#         sample_text,
#         expand_contractions=True,
#         remove_numbers=True,
#         normalize_slang=True,
#         remove_stopwords=True,
#         pos_tagging=True,
#         lemmatize=True,
#         extract_ner=True,
#         correct_spelling=True,
#         replace_synonyms=True
#     )
# print("Cleaned Text:", cleaned_text)
# bpe = BPETokenizer(vocab_size=500)
# bpe_ids = bpe.train(cleaned_text, verbose=True)
# print("BPE IDs:", bpe_ids)
