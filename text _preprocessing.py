import re
import string
from typing import List, Set, Dict, Optional, Tuple
from collections import defaultdict

class AdvancedTextPreprocessor:
    """
    Complete text preprocessing pipeline following industry best practices.
    
    Pipeline Order:
    1. Remove unwanted characters / HTML / URLs
    2. Expand contractions (optional)
    3. Remove special symbols / numbers (optional)
    4. Lowercase text
    5. Remove punctuation
    6. Normalize whitespace
    7. Normalize slang or abbreviations (optional)
    8. Tokenize text
    9. Remove stopwords
    10. POS tagging (optional)
    11. Lemmatize or Stem words
    12. Apply NER (optional)
    13. Correct spelling (optional)
    14. Replace synonyms (optional)
    15. Vectorize / Encode text for model input
    """
    
    def __init__(self):
        self._initialize_dictionaries()
    
    def _initialize_dictionaries(self):
        """Initialize all lookup dictionaries."""
        
        # Stopwords
        self.stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have',
            'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how',
            'she', 'her', 'him', 'his', 'their', 'them', 'we', 'us', 'our'
        }
        
        # Contractions
        self.contractions = {
            "ain't": "am not", "aren't": "are not", "can't": "cannot",
            "can't've": "cannot have", "could've": "could have",
            "couldn't": "could not", "didn't": "did not",
            "doesn't": "does not", "don't": "do not",
            "hadn't": "had not", "hasn't": "has not",
            "haven't": "have not", "he'd": "he would",
            "he'll": "he will", "he's": "he is",
            "i'd": "i would", "i'll": "i will",
            "i'm": "i am", "i've": "i have",
            "isn't": "is not", "it's": "it is",
            "let's": "let us", "shouldn't": "should not",
            "that's": "that is", "there's": "there is",
            "they'd": "they would", "they'll": "they will",
            "they're": "they are", "they've": "they have",
            "wasn't": "was not", "we'd": "we would",
            "we'll": "we will", "we're": "we are",
            "we've": "we have", "weren't": "were not",
            "what's": "what is", "won't": "will not",
            "wouldn't": "would not", "you'd": "you would",
            "you'll": "you will", "you're": "you are",
            "you've": "you have"
        }
        
        # Slang and abbreviations
        self.slang_dict = {
            'lol': 'laugh out loud', 'omg': 'oh my god',
            'btw': 'by the way', 'idk': 'i do not know',
            'brb': 'be right back', 'imo': 'in my opinion',
            'imho': 'in my humble opinion', 'fyi': 'for your information',
            'asap': 'as soon as possible', 'tbd': 'to be determined',
            'aka': 'also known as', 'fomo': 'fear of missing out',
            'bff': 'best friend forever', 'dm': 'direct message',
            'rt': 'retweet', 'thx': 'thanks', 'pls': 'please',
            'u': 'you', 'ur': 'your', 'r': 'are', 'n': 'and',
            'b4': 'before', '2day': 'today', '2morrow': 'tomorrow',
            'msg': 'message', 'txt': 'text', 'gr8': 'great'
        }
        
        # Lemmatization dictionary
        self.lemma_dict = {
            'running': 'run', 'ran': 'run', 'runs': 'run',
            'better': 'good', 'best': 'good',
            'worse': 'bad', 'worst': 'bad',
            'children': 'child', 'teeth': 'tooth', 'feet': 'foot',
            'mice': 'mouse', 'geese': 'goose', 'men': 'man',
            'women': 'woman', 'people': 'person',
            'was': 'be', 'were': 'be', 'been': 'be', 'being': 'be',
            'am': 'be', 'are': 'be', 'is': 'be',
            'has': 'have', 'had': 'have', 'having': 'have',
            'does': 'do', 'did': 'do', 'doing': 'do', 'done': 'do',
            'went': 'go', 'gone': 'go', 'going': 'go', 'goes': 'go',
            'said': 'say', 'says': 'say', 'saying': 'say'
        }
        
        # POS tag patterns (simplified)
        self.pos_patterns = {
            'verb_endings': ['ing', 'ed', 's'],
            'noun_endings': ['tion', 'ness', 'ment', 'ship'],
            'adj_endings': ['ful', 'less', 'ous', 'ive', 'able']
        }
        
        # Named entities (simple patterns)
        self.ner_patterns = {
            'person': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        }
        
        # Spelling corrections (common mistakes)
        self.spelling_dict = {
            'teh': 'the', 'recieve': 'receive', 'occured': 'occurred',
            'seperate': 'separate', 'definately': 'definitely',
            'untill': 'until', 'thier': 'their', 'freind': 'friend',
            'wierd': 'weird', 'beleive': 'believe', 'acheive': 'achieve',
            'goverment': 'government', 'sucessful': 'successful'
        }
        
        # Synonyms (for text augmentation)
        self.synonym_dict = {
            'good': ['excellent', 'great', 'wonderful', 'positive'],
            'bad': ['terrible', 'awful', 'poor', 'negative'],
            'big': ['large', 'huge', 'enormous', 'massive'],
            'small': ['tiny', 'little', 'miniature', 'compact'],
            'happy': ['joyful', 'delighted', 'pleased', 'content'],
            'sad': ['unhappy', 'sorrowful', 'melancholy', 'depressed']
        }
        
        # Stemming rules
        self.stemming_rules = [
            (r'sses$', 'ss'), (r'ies$', 'i'), (r'ss$', 'ss'),
            (r's$', ''), (r'eed$', 'ee'), (r'ing$', ''),
            (r'ed$', ''), (r'ational$', 'ate'), (r'tional$', 'tion'),
            (r'ator$', 'ate'), (r'alism$', 'al'), (r'ness$', ''),
            (r'ment$', ''), (r'able$', ''), (r'ible$', ''),
            (r'ly$', '')
        ]
#                       RAW TEXT CLEANING  
# ==================== STEP 1: REMOVE UNWANTED CONTENT ==================== 
    def remove_html(self, text: str) -> str:
        """Remove HTML tags from text."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove HTML entities
        text = re.sub(r'&[a-z]+;', '', text)
        return text
    
    def remove_urls(self, text: str) -> str:
        """Remove URLs from text."""
        # Remove http/https URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        # Remove www URLs
        text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        return text
    
    def remove_emails(self, text: str) -> str:
        """Remove email addresses."""
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    def remove_unwanted_chars(self, text: str) -> str:
        """Step 1: Remove HTML, URLs, emails, and other unwanted content."""
        text = self.remove_html(text)
        text = self.remove_urls(text)
        text = self.remove_emails(text)
        # Remove extra special patterns
        text = re.sub(r'[\r\t\n]', ' ', text)  # Replace newlines/tabs with space
        return text
# ==================== STEP 2: EXPAND CONTRACTIONS ====================
    def expand_contractions(self, text: str) -> str:
        """Step 2: Expand contractions (can't -> cannot)."""
        words = text.split()
        expanded_words = []
        
        for word in words:
            word_lower = word.lower()
            if word_lower in self.contractions:
                expanded_words.append(self.contractions[word_lower])
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
# ==================== STEP 3: REMOVE SPECIAL SYMBOLS/NUMBERS ====================
    def remove_special_symbols(self, text: str, keep_chars: str = '') -> str:
        """Step 3a: Remove special symbols."""
        pattern = r'[^a-zA-Z0-9{re.escape(keep_chars)}\s]'
        return re.sub(pattern, '', text)
    
    def remove_numbers(self, text: str, replace_with: str = '') -> str:
        """Step 3b: Remove or replace numbers."""
        if replace_with:
            return re.sub(r'\d+', replace_with, text)
        return re.sub(r'\d+', '', text)
#                       NORMALIZATION
# ==================== STEP 1: LOWERCASE TEXT ====================
    def lowercase(self, text: str) -> str:
        """Step 1: Convert text to lowercase."""
        return text.lower()
# ==================== STEP 2: REMOVE PUNCTUATION ====================
    
    def remove_punctuation(self, text: str, keep_chars: str = '') -> str:
        """Step 2: Remove punctuation marks."""
        punctuation_to_remove = ''.join(c for c in string.punctuation if c not in keep_chars)
        translator = str.maketrans('', '', punctuation_to_remove)
        return text.translate(translator)
# ==================== STEP 3: NORMALIZE WHITESPACE ====================
    
    def normalize_whitespace(self, text: str) -> str:
        """Step 3: Normalize whitespace (multiple spaces -> single space)."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
# ==================== STEP 4: NORMALIZE SLANG/ABBREVIATIONS ====================
    
    def normalize_slang(self, text: str) -> str:
        """Step 4: Normalize slang and abbreviations."""
        words = text.split()
        normalized_words = []
        
        for word in words:
            word_lower = word.lower()
            if word_lower in self.slang_dict:
                normalized_words.append(self.slang_dict[word_lower])
            else:
                normalized_words.append(word)
        
        return ' '.join(normalized_words)
#                     TOKENIZE  

    def tokenize(self, text: str, method: str = 'whitespace') -> List[str]:
        """
        Step 8: Tokenize text into words.
        
        Methods:
        - 'whitespace': Simple split by whitespace
        - 'word': Word tokenization (alphanumeric)
        - 'sentence': Sentence tokenization
        """
        if method == 'whitespace':
            return text.split()
        elif method == 'word':
            return re.findall(r'\b\w+\b', text)
        elif method == 'sentence':
            return re.split(r'[.!?]+', text)
        else:
            return text.split()
#                     LINGUISTIC PROCESSING
# ==================== STEP 1: REMOVE STOPWORDS ====================
    def remove_stopwords(self, tokens: List[str], custom_stopwords: Optional[Set[str]] = None) -> List[str]:
        """Step 1: Remove stopwords from token list."""
        stopwords = self.stopwords
        if custom_stopwords:
            stopwords = stopwords.union(custom_stopwords)
        
        return [token for token in tokens if token.lower() not in stopwords]
# ==================== STEP 2: POS TAGGING ====================
    def pos_tag_simple(self, tokens: List[str]) -> List[Tuple[str, str]]:
        """
        Step 2: Simple POS tagging based on patterns.
        Returns list of (word, pos_tag) tuples.
        
        Tags: NOUN, VERB, ADJ, OTHER
        Note: This is simplified. Use nltk.pos_tag for production.
        """
        tagged = []
        
        for token in tokens:
            if any(token.endswith(end) for end in self.pos_patterns['verb_endings']):
                tagged.append((token, 'VERB'))
            elif any(token.endswith(end) for end in self.pos_patterns['noun_endings']):
                tagged.append((token, 'NOUN'))
            elif any(token.endswith(end) for end in self.pos_patterns['adj_endings']):
                tagged.append((token, 'ADJ'))
            else:
                tagged.append((token, 'OTHER'))
        
        return tagged
# ==================== STEP 3: LEMMATIZATION OR STEMMING ====================
    def lemmatize(self, word: str, pos: str = 'n') -> str:
        """Lemmatize a single word."""
        word_lower = word.lower()
        
        # Check dictionary first
        if word_lower in self.lemma_dict:
            return self.lemma_dict[word_lower]
        
        # Apply rules based on POS
        if pos == 'v':  # Verb
            if word_lower.endswith('ing'):
                return word_lower[:-3]
            elif word_lower.endswith('ed'):
                return word_lower[:-2]
            elif word_lower.endswith('s') and len(word_lower) > 2:
                return word_lower[:-1]
        elif pos == 'n':  # Noun
            if word_lower.endswith('es'):
                return word_lower[:-2]
            elif word_lower.endswith('s') and len(word_lower) > 2:
                return word_lower[:-1]
        
        return word_lower
    def lemmatize_tokens(self, tokens: List[str], pos_tags: Optional[List[Tuple[str, str]]] = None) -> List[str]:
        """Step 11: Lemmatize token list."""
        if pos_tags:
            lemmatized = []
            for (word, pos), token in zip(pos_tags, tokens):
                if pos == 'VERB':
                    lemmatized.append(self.lemmatize(token, 'v'))
                elif pos == 'NOUN':
                    lemmatized.append(self.lemmatize(token, 'n'))
                else:
                    lemmatized.append(self.lemmatize(token))
            return lemmatized
        else:
            return [self.lemmatize(token) for token in tokens]
# ==================== OR ====================  
    def stem(self, word: str) -> str:
        """Stem a single word using Porter Stemmer rules."""
        word = word.lower()
        
        for pattern, replacement in self.stemming_rules:
            if re.search(pattern, word):
                word = re.sub(pattern, replacement, word)
                break
        
        return word
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Step 11: Stem token list."""
        return [self.stem(token) for token in tokens]
# ==================== STEP 4: NER ====================
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Step 4: Extract named entities.
        Returns dictionary of entity types and their values.
        """
        entities = defaultdict(list)
        
        for entity_type, pattern in self.ner_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type].extend(matches)
        
        return dict(entities)
    def mask_entities(self, text: str, entity_type: str = 'all') -> str:
        """Replace entities with tags like <PERSON>, <EMAIL>."""
        if entity_type == 'all':
            for ent_type, pattern in self.ner_patterns.items():
                text = re.sub(pattern, f'<{ent_type.upper()}>', text)
        else:
            pattern = self.ner_patterns.get(entity_type)
            if pattern:
                text = re.sub(pattern, f'<{entity_type.upper()}>', text)
        
        return text
# ==================== STEP 5: SPELL CORRECTION ====================
    
    def correct_spelling(self, tokens: List[str]) -> List[str]:
        """
        Step 5: Correct common spelling mistakes.
        Note: Use pyspellchecker or autocorrect for production.
        """
        return [self.spelling_dict.get(token.lower(), token) for token in tokens]
# ==================== STEP 6: SYNONYM REPLACEMENT ====================
    def replace_with_synonyms(self, tokens: List[str], replacement_prob: float = 0.3) -> List[str]:
        """
        Step 6: Replace words with synonyms (for data augmentation).

        Args:
            tokens: Input tokens
            replacement_prob: Probability of replacing each word (0.0 - 1.0)
        """
        import random
        replaced = []
        
        for token in tokens:
            if token.lower() in self.synonym_dict and random.random() < replacement_prob:
                synonyms = self.synonym_dict[token.lower()]
                replaced.append(random.choice(synonyms))
            else:
                replaced.append(token)
        
        return replaced
    def preprocess_pipeline(self, 
                           text: str,
                           expand_contractions: bool = True,
                           remove_numbers: bool = True,
                           normalize_slang: bool = True,
                           remove_stopwords: bool = True,
                           pos_tagging: bool = False,
                           lemmatize: bool = True,
                           stem: bool = False,
                           extract_ner: bool = False,
                           correct_spelling: bool = True,
                           replace_synonyms: bool = False) -> Dict:
        results = {'original': text}
        text = self.remove_unwanted_chars(text)
        results['step1_cleaned'] = text
        
        # Step 2: Expand contractions
        if expand_contractions:
            text = self.expand_contractions(text)
            results['step2_contractions'] = text
        
        # Step 3: Remove special symbols and numbers
        text = self.remove_special_symbols(text)
        if remove_numbers:
            text = self.remove_numbers(text)
            results['step3_special_removed'] = text
        
        # Step 4: Lowercase
        text = self.lowercase(text)
        results['step4_lowercase'] = text
        
        # Step 5: Remove punctuation
        text = self.remove_punctuation(text)
        results['step5_no_punct'] = text
        
        # Step 6: Normalize whitespace
        text = self.normalize_whitespace(text)
        results['step6_normalized'] = text
        
        # Step 7: Normalize slang
        if normalize_slang:
            text = self.normalize_slang(text)
            results['step7_slang_normalized'] = text
        
        # Step 8: Tokenize
        tokens = self.tokenize(text, method='whitespace')
        results['step8_tokens'] = tokens
        
        # Step 9: Remove stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
            results['step9_no_stopwords'] = tokens
        
        # Step 10: POS tagging
        pos_tags = None
        if pos_tagging:
            pos_tags = self.pos_tag_simple(tokens)
            results['step10_pos_tags'] = pos_tags
        
        # Step 11: Lemmatize or Stem
        if lemmatize and not stem:
            tokens = self.lemmatize_tokens(tokens, pos_tags)
            results['step11_lemmatized'] = tokens
        elif stem:
            tokens = self.stem_tokens(tokens)
            results['step11_stemmed'] = tokens
        
        # Step 12: NER
        if extract_ner:
            entities = self.extract_entities(results['step6_normalized'])
            results['step12_entities'] = entities
        
        # Step 13: Spell correction
        if correct_spelling:
            tokens = self.correct_spelling(tokens)
            results['step13_spelling_corrected'] = tokens
        
        # Step 14: Synonym replacement
        if replace_synonyms:
            tokens = self.replace_with_synonyms(tokens)
            results['step14_synonyms'] = tokens
        
        # Final tokens
        results['final_tokens'] = tokens
        results['final_text'] = ' '.join(tokens)
        return results
# if __name__ == "__main__":
#     preprocessor = AdvancedTextPreprocessor()
#     sample_text = """
#     <html>Hello!!! Check out https://example.com for more info. Delhi 
#     I can't believe it's 2024! Contact us at info@example.com or call 555-123-4567.
#     LOL this is gr8! Btw, I'll be there ASAP. There are 123 special chars: @#$%
#     John Smith is the CEO. I recieve alot of emails daily.</html>
#     """
    
#     print("="*80)
#     print("ORIGINAL TEXT:")
#     print("="*80)
#     print(sample_text)
#     results = preprocessor.preprocess_pipeline(
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
#     print("\n" + "="*80)
#     print("PIPELINE RESULTS:")
#     print("="*80)
#     steps = [
#         ('step1_cleaned', 'Step 1: Removed HTML/URLs/Emails'),
#         ('step2_contractions', 'Step 2: Expanded Contractions'),
#         ('step3_special_removed', 'Step 3: Removed Special Chars/Numbers'),
#         ('step4_lowercase', 'Step 4: Lowercased'),
#         ('step5_no_punct', 'Step 5: Removed Punctuation'),
#         ('step6_normalized', 'Step 6: Normalized Whitespace'),
#         ('step7_slang_normalized', 'Step 7: Normalized Slang'),
#         ('step8_tokens', 'Step 8: Tokenized'),
#         ('step9_no_stopwords', 'Step 9: Removed Stopwords'),
#         ('step10_pos_tags', 'Step 10: POS Tagged'),
#         ('step11_lemmatized', 'Step 11: Lemmatized'),
#         ('step12_entities', 'Step 12: Named Entities'),
#         ('step13_spelling_corrected', 'Step 13: Spelling Corrected'),
#         ('step14_synonyms', 'Step 14: Synonyms Replaced'),
#         ('final_tokens', 'Final Tokens'),
#         ('final_text', 'Final Text')
#     ]

#     for key, description in steps:
#         if key in results:
#             print(f"\n{description}:")
#             print("-" * 80)
#             if isinstance(results[key], list):
#                 if key == 'step10_pos_tags':
#                     print(results[key])  # Show all POS tags
#                 else:
#                     print(results[key])
#             elif isinstance(results[key], dict):
#                 for k, v in results[key].items():
#                     print(f"  {k}: {v}")
#             else:
#                 print(results[key])
#     print("="*80)
