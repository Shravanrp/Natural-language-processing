import re
import string
from typing import List, Set, Dict, Optional
from collections import defaultdict
import unicodedata 
class TextPreprocessor:
    """Comprehensive text preprocessing with optimal implementations."""
    
    def __init__(self):
        # Common English stopwords
        self.stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
            'had', 'what', 'when', 'where', 'who', 'which', 'why', 'how'
        }
        
        # Common contractions
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
        
        # Stemming rules (Porter Stemmer simplified)
        self.stemming_rules = self._initialize_stemming_rules()
        
        # Lemmatization dictionary (common irregular words)
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
            'went': 'go', 'gone': 'go', 'going': 'go', 'goes': 'go'
        }
    
    def _initialize_stemming_rules(self) -> List[tuple]:
        """Initialize Porter Stemmer rules (simplified version)."""
        return [
            (r'sses$', 'ss'),     #resses -> ress
            (r'ies$', 'i'),      # ponies -> poni
            (r'ss$', 'ss'),      # stress -> stress
            (r's$', ''),         # cats -> cat
            (r'eed$', 'ee'),     # agreed -> agree
            (r'ing$', ''),       # running -> run
            (r'ed$', ''),        # played -> play
            (r'ational$', 'ate'), # rational -> rate
            (r'tional$', 'tion'), # conditional -> condition
            (r'enci$', 'ence'),  # valenci -> valence
            (r'anci$', 'ance'),  # hesitanci -> hesitance
            (r'izer$', 'ize'),   # digitizer -> digitize
            (r'ation$', 'ate'),  # exploration -> explore
            (r'ator$', 'ate'),   # operator -> operate
            (r'alism$', 'al'),   # feudalism -> feudal
            (r'iveness$', 'ive'), # decisiveness -> decisive
            (r'fulness$', 'ful'), # hopefulness -> hopeful
            (r'ousness$', 'ous'), # callousness -> callous
            (r'aliti$', 'al'),   # formality -> formal
            (r'iviti$', 'ive'),  # sensitivity -> sensitive
            (r'ement$', ''),     # replacement -> replac
            (r'ment$', ''),      # adjustment -> adjust
            (r'ent$', ''),       # dependent -> depend
            (r'able$', ''),      # adjustable -> adjust
            (r'ible$', ''),      # possible -> poss
            (r'ly$', ''),        # quickly -> quick
        ]
    
    # ==================== 1. LOWERCASING ====================
    def lowercase(self, text: str) -> str:
        return text.lower()
    
    # ==================== 2. STOPWORD REMOVAL ====================
    def remove_stopwords(self, text: str, custom_stopwords: Optional[Set[str]] = None) -> str:
        stopwords = self.stopwords
        if custom_stopwords:
            stopwords = stopwords.union(custom_stopwords)
        
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        return ' '.join(filtered_words)
    
    # ==================== 3. PUNCTUATION REMOVAL ====================
    def remove_punctuation(self, text: str, keep_chars: str = '') -> str:
        # Create translation table for fast removal
        punctuation_to_remove = ''.join(c for c in string.punctuation if c not in keep_chars)
        translator = str.maketrans('', '', punctuation_to_remove)
        return text.translate(translator)
    # ============================= or =================================
    def remove_punctuation_regex(self, text: str) -> str:
        """Alternative: Remove punctuation using regex (slower but more flexible)."""
        return re.sub(r'[^\w\s]', '', text)
    
    # ==================== 4. STEMMING ====================
    def stem(self, word: str) -> str:# for single word
        word = word.lower()
        
        # Apply stemming rules in order
        for pattern, replacement in self.stemming_rules:
            if re.search(pattern, word):
                word = re.sub(pattern, replacement, word)
                break
        
        return word
    
    def stem_text(self, text: str) -> str:# for complete text
        """Apply stemming to entire text."""
        words = text.split()
        stemmed_words = [self.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    # ==================== 5. LEMMATIZATION ====================
    def lemmatize(self, word: str, pos: str = 'n') -> str:# for single word
        word_lower = word.lower()
        
        # Check lemmatization dictionary
        if word_lower in self.lemma_dict:
            return self.lemma_dict[word_lower]
        
        # Simple rule-based lemmatization
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
    
    def lemmatize_text(self, text: str) -> str:# for complete text
        """Apply lemmatization to entire text."""
        words = text.split()
        lemmatized_words = [self.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)
    
    # ==================== 6. TEXT NORMALIZATION ====================
    
    def expand_contractions(self, text: str) -> str:
        words = text.split()
        expanded_words = []
        
        for word in words:
            word_lower = word.lower()
            # Check if word is a contraction
            if word_lower in self.contractions:
                expanded_words.append(self.contractions[word_lower])
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def remove_extra_whitespace(self, text: str) -> str:
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def remove_numbers(self, text: str) -> str:
        """Remove all numbers from text."""
        return re.sub(r'\d+', '', text)
    
    def remove_special_characters(self, text: str, keep_chars: str = '') -> str:
        """
        Remove special characters, keeping only alphanumeric and specified chars.
        
        Args:
            text: Input text
            keep_chars: Characters to keep (e.g., ' -' for spaces and hyphens)
        """
        pattern = f'[^a-zA-Z0-9{re.escape(keep_chars)}\s]'
        return re.sub(pattern, '', text)
    
    def normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters to ASCII."""
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    def correct_spelling_simple(self, text: str) -> str:
        # Common misspellings dictionary
        common_mistakes = {
            'teh': 'the', 'recieve': 'receive', 'occured': 'occurred',
            'seperate': 'separate', 'definately': 'definitely',
            'untill': 'until', 'thier': 'their', 'freind': 'friend'
        }
        
        words = text.split()
        corrected_words = [common_mistakes.get(word.lower(), word) for word in words]
        return ' '.join(corrected_words)
    
    # ==================== COMPLETE PIPELINE ====================
    
    def preprocess(self, text: str, 
                     lowercase: bool = True,
                     remove_stopwords: bool = True,
                     remove_punctuation: bool = True,
                     expand_contractions: bool = True,
                     remove_numbers: bool = False,
                     stem: bool = False,
                     lemmatize: bool = False,
                     normalize_whitespace: bool = True) -> str:#change the parameters according to your requirements
        """
        Complete preprocessing pipeline.
        
        Order of operations matters:
        1. Expand contractions (before lowercasing)
        2. Lowercase
        3. Remove special characters/punctuation
        4. Remove numbers (optional)
        5. Normalize whitespace
        6. Remove stopwords
        7. Stem OR Lemmatize (not both)
        """
        if expand_contractions:
            text = self.expand_contractions(text)
        
        if lowercase:
            text = self.lowercase(text)
        
        if remove_punctuation:
            text = self.remove_punctuation(text)
        
        if remove_numbers:
            text = self.remove_numbers(text)
        
        if normalize_whitespace:
            text = self.remove_extra_whitespace(text)
        
        if remove_stopwords:
            text = self.remove_stopwords(text)
        
        # Apply either stemming or lemmatization (not both)
        if stem and not lemmatize:
            text = self.stem_text(text)
        elif lemmatize:
            text = self.lemmatize_text(text)
        
        return text
