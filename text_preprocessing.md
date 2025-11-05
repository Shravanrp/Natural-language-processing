
---

# 🧠 Advanced Text Preprocessor

A **complete, production-ready text preprocessing pipeline** for Natural Language Processing (NLP) tasks — implemented in pure Python using best industry practices.

This module provides **cleaning**, **normalization**, **tokenization**, **linguistic processing**, and **text augmentation** in a single, modular class: `AdvancedTextPreprocessor`.

---

## 🚀 Features

✅ **Raw Text Cleaning**

* Removes HTML, URLs, emails, and unwanted characters
* Expands contractions (e.g., *can’t → cannot*)
* Handles special symbols and numbers

✅ **Normalization**

* Converts to lowercase
* Removes punctuation
* Normalizes whitespace
* Replaces slang and abbreviations (*e.g., omg → oh my god*)

✅ **Tokenization**

* Supports multiple methods: `whitespace`, `word`, and `sentence`
* Produces clean, consistent tokens for modeling

✅ **Linguistic Processing**

* Removes stopwords
* Performs simple POS tagging
* Lemmatizes or stems words
* Extracts Named Entities (NER) like names, emails, dates, and phone numbers

✅ **Text Enhancement**

* Spell correction (basic dictionary-based)
* Synonym replacement for data augmentation
* Configurable full preprocessing pipeline

---

## 🏗️ Project Structure

```
advanced_text_preprocessor/
│
├── 📄 advanced_text_preprocessor.py     # Core module (the class you provided)
├── 📘 README.md                         # This documentation              
```

---

## 📦 Installation

```bash
git clone https://github.com/Shravanrp/advanced-text-preprocessor.git
cd advanced-text-preprocessor
```

---

## 🧩 Usage

### ▶️ Basic Example

```python
from advanced_text_preprocessor import AdvancedTextPreprocessor

preprocessor = AdvancedTextPreprocessor()

text = "OMG! I can't believe this happened 2day 😱. Email me at test@example.com."

results = preprocessor.preprocess_pipeline(
    text,
    expand_contractions=True,
    normalize_slang=True,
    lemmatize=True,
    correct_spelling=True,
    extract_ner=True
)

print("Final Tokens:", results['final_tokens'])
print("Clean Text:", results['final_text'])
print("Named Entities:", results.get('step12_entities', {}))
```

---

### 🧾 Example Output

```
Original: OMG! I can't believe this happened 2day 😱. Email me at test@example.com.

Step 1 (Cleaned): OMG! I can't believe this happened 2day . Email me at 
Step 2 (Contractions): OMG! I cannot believe this happened 2day . Email me at 
Step 4 (Lowercase): omg! i cannot believe this happened 2day . email me at 
Step 7 (Slang normalized): oh my god i cannot believe this happened today email me at
Step 8 (Tokens): ['oh', 'my', 'god', 'i', 'cannot', 'believe', 'this', 'happened', 'today', 'email', 'me', 'at']
Step 9 (Stopwords removed): ['god', 'cannot', 'believe', 'happened', 'today', 'email']
Step 11 (Lemmatized): ['god', 'cannot', 'believe', 'happen', 'today', 'email']
Step 13 (Spelling corrected): ['god', 'cannot', 'believe', 'happen', 'today', 'email']

✅ Final Tokens: ['god', 'cannot', 'believe', 'happen', 'today', 'email']
✅ Final Text: "god cannot believe happen today email"
```

---

## ⚙️ Customization

You can toggle features in the pipeline:

```python
results = preprocessor.preprocess_pipeline(
    text,
    expand_contractions=False,
    remove_numbers=True,
    normalize_slang=False,
    pos_tagging=True,
    stem=True,
    replace_synonyms=True
)
```

You can also call individual steps manually:

```python
clean_text = preprocessor.remove_unwanted_chars(text)
tokens = preprocessor.tokenize(clean_text, method='word')
filtered = preprocessor.remove_stopwords(tokens)
lemmas = preprocessor.lemmatize_tokens(filtered)
```

---

## 🧠 Pipeline Order (Summary)

| Step | Task                     | Function                               | Example                         |
| ---- | ------------------------ | -------------------------------------- | ------------------------------- |
| 1    | Remove unwanted chars    | `remove_unwanted_chars()`              | remove HTML, URLs               |
| 2    | Expand contractions      | `expand_contractions()`                | can’t → cannot                  |
| 3    | Remove symbols/numbers   | `remove_special_symbols()`             | `@#12` →                        |
| 4    | Lowercase                | `lowercase()`                          | NLP → nlp                       |
| 5    | Remove punctuation       | `remove_punctuation()`                 | wow! → wow                      |
| 6    | Normalize whitespace     | `normalize_whitespace()`               | “hello   world” → “hello world” |
| 7    | Normalize slang          | `normalize_slang()`                    | omg → oh my god                 |
| 8    | Tokenize                 | `tokenize()`                           | split text into words           |
| 9    | Remove stopwords         | `remove_stopwords()`                   | “the”, “is”, “and” removed      |
| 10   | POS tagging              | `pos_tag_simple()`                     | simple grammar-based tags       |
| 11   | Lemmatize / Stem         | `lemmatize_tokens()` / `stem_tokens()` | “running” → “run”               |
| 12   | Named Entity Recognition | `extract_entities()`                   | detect emails, names, etc.      |
| 13   | Spell correction         | `correct_spelling()`                   | “teh” → “the”                   |
| 14   | Synonym replacement      | `replace_with_synonyms()`              | “good” → “great”                |
                                 |

---


---

## 🧩 Future Improvements

* Integrate spaCy / NLTK POS tagging and lemmatization
* Add configurable stemming rules (Porter / Snowball)
* Extend synonym replacement via WordNet
* Add multilingual support

---

## 🧑‍💻 Author

**Shravan Pattar**
📘 NLP Developer | Machine Learning Enthusiast

---
