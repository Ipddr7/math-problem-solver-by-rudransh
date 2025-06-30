"""
Natural Language Processing Module for Math Problem Solver

This module handles text preprocessing, keyword extraction, and problem classification
for mathematical problems expressed in natural language.
"""

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from typing import Dict, List, Tuple, Optional
import json
import os

class NLPProcessor:
    """
    NLP processor for mathematical problem text analysis.
    
    This class handles:
    - Text preprocessing and normalization
    - Mathematical keyword extraction
    - Problem type classification
    - Variable and constant identification
    """
    
    def __init__(self):
        """Initialize the NLP processor with mathematical keywords and patterns."""
        # Initialize NLTK data
        self._initialize_nltk()
        
        self.stop_words = set(stopwords.words('english'))
        
        # Mathematical keywords mapping
        self.math_keywords = {
            'linear': ['linear', 'first degree', 'simple equation'],
            'quadratic': ['quadratic', 'second degree', 'squared', 'x²', 'x^2'],
            'system': ['system', 'simultaneous', 'both', 'and', 'together'],
            'solve': ['solve', 'find', 'calculate', 'determine', 'what is'],
            'roots': ['roots', 'solutions', 'zeros', 'x-intercepts'],
            'variables': ['x', 'y', 'z', 'a', 'b', 'c', 'variable'],
            'operations': ['plus', 'minus', 'times', 'divided by', 'equals', '='],
            'numbers': ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        }
        
        # Mathematical patterns
        self.patterns = {
            'equation': r'([a-zA-Z]\s*[+\-*/]\s*\d+|\d+\s*[+\-*/]\s*[a-zA-Z]|\d+\s*=\s*\d+)',
            'variable': r'\b([a-zA-Z])\b',
            'number': r'\b(\d+(?:\.\d+)?)\b',
            'power': r'(\w+\^?\d+|\w+²)',
            'fraction': r'(\d+)/(\d+)'
        }
        
        # Load additional keywords from file if available
        self._load_keywords()
    
    def _initialize_nltk(self):
        """Initialize NLTK data with error handling."""
        try:
            # Try to download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt_tab', quiet=True)
        except Exception as e:
            print(f"Warning: Could not download NLTK data: {e}")
            # Continue without NLTK features if download fails
    
    def _load_keywords(self):
        """Load additional mathematical keywords from JSON file."""
        try:
            keywords_path = os.path.join('data', 'keywords.json')
            if os.path.exists(keywords_path):
                with open(keywords_path, 'r') as f:
                    additional_keywords = json.load(f)
                    self.math_keywords.update(additional_keywords)
        except Exception as e:
            print(f"Warning: Could not load keywords file: {e}")
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess and normalize input text.
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Preprocessed text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Normalize mathematical symbols
        text = text.replace('×', '*').replace('÷', '/')
        text = text.replace('²', '^2').replace('³', '^3')
        
        # Handle common mathematical phrases
        text = text.replace('plus', '+').replace('minus', '-')
        text = text.replace('times', '*').replace('multiplied by', '*')
        text = text.replace('divided by', '/').replace('over', '/')
        text = text.replace('equals', '=').replace('is equal to', '=')
        
        return text
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Extract mathematical keywords from text.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            Dict[str, List[str]]: Dictionary of keyword categories and found keywords
        """
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple word splitting if NLTK tokenization fails
            tokens = text.split()
        
        extracted_keywords = {category: [] for category in self.math_keywords.keys()}
        
        for token in tokens:
            for category, keywords in self.math_keywords.items():
                if token in keywords or any(keyword in token for keyword in keywords):
                    extracted_keywords[category].append(token)
        
        return extracted_keywords
    
    def classify_problem_type(self, text: str) -> str:
        """
        Classify the type of mathematical problem.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            str: Problem type ('linear', 'quadratic', 'system', 'unknown')
        """
        keywords = self.extract_keywords(text)
        
        # Check for system of equations
        if keywords['system'] or ('and' in text and '=' in text):
            return 'system'
        
        # Check for quadratic equations
        if keywords['quadratic'] or re.search(r'\^2|²', text):
            return 'quadratic'
        
        # Check for linear equations - expanded patterns
        if (keywords['linear'] or 
            re.search(r'[a-zA-Z]\s*[+\-*/]\s*\d+|\d+\s*[+\-*/]\s*[a-zA-Z]', text) or
            re.search(r'find\s+[a-zA-Z]+\s*if', text) or
            re.search(r'what\s+is\s+[a-zA-Z]+\s*if', text) or
            re.search(r'[a-zA-Z]\s*=\s*\d+|\d+\s*=\s*[a-zA-Z]', text)):
            return 'linear'
        
        return 'unknown'
    
    def extract_variables(self, text: str) -> List[str]:
        """
        Extract variables from the text.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            List[str]: List of found variables
        """
        variables = re.findall(self.patterns['variable'], text)
        return list(set(variables))
    
    def extract_numbers(self, text: str) -> List[float]:
        """
        Extract numbers from the text.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            List[float]: List of found numbers
        """
        numbers = re.findall(self.patterns['number'], text)
        return [float(num) for num in numbers]
    
    def extract_equations(self, text: str) -> List[str]:
        """
        Extract mathematical expressions from text.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            List[str]: List of found equations/expressions
        """
        equations = re.findall(self.patterns['equation'], text)
        return equations
    
    def analyze_problem(self, text: str) -> Dict:
        """
        Comprehensive analysis of a mathematical problem.
        
        Args:
            text (str): Raw input text
            
        Returns:
            Dict: Complete analysis including problem type, variables, numbers, etc.
        """
        preprocessed = self.preprocess_text(text)
        
        analysis = {
            'original_text': text,
            'preprocessed_text': preprocessed,
            'problem_type': self.classify_problem_type(preprocessed),
            'keywords': self.extract_keywords(preprocessed),
            'variables': self.extract_variables(preprocessed),
            'numbers': self.extract_numbers(preprocessed),
            'equations': self.extract_equations(preprocessed),
            'confidence': self._calculate_confidence(preprocessed)
        }
        
        return analysis
    
    def _calculate_confidence(self, text: str) -> float:
        """
        Calculate confidence score for the analysis.
        
        Args:
            text (str): Preprocessed text
            
        Returns:
            float: Confidence score between 0 and 1
        """
        confidence = 0.0
        
        # Base confidence for having mathematical content
        if re.search(r'[+\-*/=]', text):
            confidence += 0.3
        
        # Confidence for having variables
        if re.search(r'\b[a-zA-Z]\b', text):
            confidence += 0.2
        
        # Confidence for having numbers
        if re.search(r'\b\d+\b', text):
            confidence += 0.2
        
        # Confidence for clear problem type
        problem_type = self.classify_problem_type(text)
        if problem_type != 'unknown':
            confidence += 0.3
        
        return min(confidence, 1.0)
    
    def validate_input(self, text: str) -> Tuple[bool, str]:
        """
        Validate if the input text contains a valid mathematical problem.
        
        Args:
            text (str): Input text
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not text or len(text.strip()) < 5:
            return False, "Input text is too short"
        
        analysis = self.analyze_problem(text)
        
        if analysis['confidence'] < 0.3:
            return False, "Text doesn't appear to contain a mathematical problem"
        
        if not analysis['variables']:
            return False, "No variables found in the problem"
        
        if not analysis['numbers']:
            return False, "No numbers found in the problem"
        
        return True, "Valid mathematical problem" 