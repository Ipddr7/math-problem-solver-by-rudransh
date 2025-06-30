"""
Equation Parser Module for Math Problem Solver

This module handles the conversion of text-based mathematical expressions
into SymPy symbolic expressions for computation.
"""

import re
import sympy as sp
from sympy import symbols, solve, Eq, simplify, expand, factor
from typing import Dict, List, Tuple, Optional, Union
import ast

class EquationParser:
    """
    Parser for converting text-based mathematical expressions to SymPy objects.
    
    This class handles:
    - Text to mathematical expression conversion
    - Variable identification and symbol creation
    - Expression normalization and validation
    - Equation extraction from text
    """
    
    def __init__(self):
        """Initialize the equation parser with common mathematical patterns."""
        self.variables = {}
        self.patterns = {
            'equation': r'([^=]+)\s*=\s*([^=]+)',
            'expression': r'([a-zA-Z]\s*[+\-*/]\s*\d+|\d+\s*[+\-*/]\s*[a-zA-Z]|\d+\s*[+\-*/]\s*\d+)',
            'variable': r'\b([a-zA-Z])\b',
            'number': r'\b(\d+(?:\.\d+)?)\b',
            'power': r'(\w+)\^?(\d+)',
            'fraction': r'(\d+)/(\d+)'
        }
        
        # Common mathematical replacements
        self.replacements = {
            'plus': '+',
            'minus': '-',
            'times': '*',
            'multiplied by': '*',
            'divided by': '/',
            'over': '/',
            'equals': '=',
            'is equal to': '=',
            'squared': '^2',
            'cubed': '^3',
            'to the power of': '^',
            'x²': 'x^2',
            'x³': 'x^3'
        }
    
    def replace_number_words(self, text: str) -> str:
        """
        Replace number words (e.g., 'five') with digits (e.g., '5') in the text.
        """
        number_map = {
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
            'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
            'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20'
        }
        for word, digit in number_map.items():
            # Replace only if the word is a standalone word
            text = re.sub(r'\b' + word + r'\b', digit, text)
        return text

    def extract_math_expression(self, text: str) -> str:
        """
        Extract mathematical expression from text, removing non-mathematical parts.
        Handles unicode exponents, implicit multiplication, and number words.
        """
        # Replace all unicode minus and dash variants at the very start
        text = text.replace('−', '-')  # Unicode minus
        text = text.replace('–', '-')  # En dash
        text = text.replace('—', '-')  # Em dash
        text = text.replace('‐', '-')  # Hyphen
        text = text.replace('‑', '-')  # Non-breaking hyphen
        text = text.replace('‒', '-')  # Figure dash
        text = text.replace('―', '-')  # Horizontal bar
        text = text.replace('⁻', '-')  # Superscript minus
        text = text.replace('﹣', '-')  # Small minus
        text = text.replace('－', '-')  # Fullwidth minus
        text = text.replace('×', '*')  # Unicode multiplication
        text = text.replace('÷', '/')  # Unicode division
        # Remove common non-mathematical phrases
        text = text.lower()
        text = re.sub(r'solve\s+for\s+[a-zA-Z]+\s*:?','', text)
        text = re.sub(r'find\s+[a-zA-Z]+\s*if\s*', '', text)
        text = re.sub(r'find\s+the\s+roots?\s+of\s*', '', text)
        text = re.sub(r'what\s+is\s+[a-zA-Z]+\s*if\s*', '', text)
        text = re.sub(r'what\s+is\s+', '', text)
        text = re.sub(r'calculate\s+', '', text)
        text = re.sub(r'determine\s+', '', text)
        text = re.sub(r'solve\s+the\s+system\s*:', '', text)
        text = re.sub(r'find\s+[a-zA-Z]+:', '', text)
        text = re.sub(r'\?$', '', text)
        # Remove the word "solve" at the beginning
        text = re.sub(r'^solve\s+', '', text)
        # Replace number words with digits
        text = self.replace_number_words(text)
        # Replace unicode exponents
        text = text.replace('²', '^2').replace('³', '^3')
        # Remove commas
        text = text.replace(',', '')
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Look for equation pattern (something = something)
        equation_match = re.search(self.patterns['equation'], text)
        if equation_match:
            left_side = equation_match.group(1).strip()
            right_side = equation_match.group(2).strip()
            return f"{left_side} = {right_side}"
        
        # If no equation found, look for expressions with equals sign
        if '=' in text:
            parts = text.split('=', 1)
            if len(parts) == 2:
                left_side = parts[0].strip()
                right_side = parts[1].strip()
                return f"{left_side} = {right_side}"
        
        # If still nothing, try to extract any mathematical content
        math_content = re.findall(r'[a-zA-Z0-9+\-*/^()=\s]+', text)
        if math_content:
            return ''.join(math_content).strip()
        
        return text.strip()

    def contains_non_numeric_words(self, text: str) -> bool:
        """
        Check if the text contains non-numeric words (e.g., 'five' instead of '5').
        Now skips check if number words are replaced.
        """
        # List of common number words
        number_words = ['zero','one','two','three','four','five','six','seven','eight','nine','ten',
                        'eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen','twenty']
        for word in number_words:
            if re.search(r'\b'+word+r'\b', text):
                return True
        return False

    def normalize_expression(self, text: str) -> str:
        """
        Normalize mathematical expression text.
        Handles implicit multiplication and malformed input.
        """
        # First extract the mathematical part
        text = self.extract_math_expression(text)
        # Replace all unicode minus and dash variants at the very start
        text = text.replace('−', '-')  # Unicode minus
        text = text.replace('–', '-')  # En dash
        text = text.replace('—', '-')  # Em dash
        text = text.replace('‐', '-')  # Hyphen
        text = text.replace('‑', '-')  # Non-breaking hyphen
        text = text.replace('‒', '-')  # Figure dash
        text = text.replace('―', '-')  # Horizontal bar
        text = text.replace('⁻', '-')  # Superscript minus
        text = text.replace('﹣', '-')  # Small minus
        text = text.replace('－', '-')  # Fullwidth minus
        text = text.replace('×', '*')  # Unicode multiplication
        text = text.replace('÷', '/')  # Unicode division
        if self.contains_non_numeric_words(text):
            raise ValueError("Input contains non-numeric words (e.g., 'five x'). Please use digits only.")
        # Apply replacements
        for old, new in self.replacements.items():
            text = text.replace(old, new)
        # Handle implicit multiplication (e.g., 2x -> 2*x, x2 -> x*2)
        text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
        text = re.sub(r'([a-zA-Z])(\d)', r'\1*\2', text)
        # Clean up whitespace around operators
        text = re.sub(r'\s*([+\-*/=^()])\s*', r'\1', text)
        # Add spaces around operators for readability
        text = re.sub(r'([+\-*/=^()])', r' \1 ', text)
        # Remove double operators (e.g., '++', '--')
        text = re.sub(r'([+\-*/=^()])\s+\1', r'\1', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_variables(self, text: str) -> List[str]:
        """
        Extract variables from mathematical text.
        
        Args:
            text (str): Mathematical text
            
        Returns:
            List[str]: List of unique variables
        """
        variables = re.findall(self.patterns['variable'], text)
        return list(set(variables))
    
    def create_symbols(self, variables: List[str]) -> Dict[str, sp.Symbol]:
        """
        Create SymPy symbols for variables.
        
        Args:
            variables (List[str]): List of variable names
            
        Returns:
            Dict[str, sp.Symbol]: Mapping of variable names to SymPy symbols
        """
        symbols_dict = {}
        for var in variables:
            if var not in self.variables:
                self.variables[var] = sp.Symbol(var)
            symbols_dict[var] = self.variables[var]
        return symbols_dict
    
    def parse_expression(self, text: str) -> Tuple[sp.Expr, Dict[str, sp.Symbol]]:
        """
        Parse a mathematical expression into SymPy expression.
        
        Args:
            text (str): Mathematical expression text
            
        Returns:
            Tuple[sp.Expr, Dict[str, sp.Symbol]]: (SymPy expression, variable symbols)
        """
        normalized = self.normalize_expression(text)
        variables = self.extract_variables(normalized)
        symbols_dict = self.create_symbols(variables)
        
        try:
            # Replace variables with their symbol names for SymPy parsing
            expr_text = normalized
            for var, symbol in symbols_dict.items():
                expr_text = expr_text.replace(var, str(symbol))
            
            # Parse the expression
            expr = sp.sympify(expr_text)
            return expr, symbols_dict
            
        except Exception as e:
            raise ValueError(f"Failed to parse expression '{text}': {str(e)}")
    
    def parse_equation(self, text: str) -> Tuple[sp.Eq, Dict[str, sp.Symbol]]:
        """
        Parse a mathematical equation into SymPy equation.
        
        Args:
            text (str): Mathematical equation text
            
        Returns:
            Tuple[sp.Eq, Dict[str, sp.Symbol]]: (SymPy equation, variable symbols)
        """
        # Extract mathematical expression first
        math_text = self.extract_math_expression(text)
        
        # Split equation into left and right sides
        parts = math_text.split('=')
        if len(parts) != 2:
            raise ValueError(f"Invalid equation format: {text}")
        
        left_text, right_text = parts[0].strip(), parts[1].strip()
        
        # Parse both sides
        left_expr, left_symbols = self.parse_expression(left_text)
        right_expr, right_symbols = self.parse_expression(right_text)
        
        # Combine symbols
        all_symbols = {**left_symbols, **right_symbols}
        
        # Create equation
        equation = sp.Eq(left_expr, right_expr)
        
        return equation, all_symbols
    
    def extract_equations_from_text(self, text: str) -> List[Tuple[sp.Eq, Dict[str, sp.Symbol]]]:
        """
        Extract multiple equations from text.
        
        Args:
            text (str): Text containing equations
            
        Returns:
            List[Tuple[sp.Eq, Dict[str, sp.Symbol]]]: List of equations and their symbols
        """
        equations = []
        
        # Clean the text first
        clean_text = text.lower()
        clean_text = re.sub(r'solve\s+the\s+system\s*:', '', clean_text)
        clean_text = re.sub(r'and\s+', '&', clean_text)  # Replace 'and' with separator
        
        # Split by 'and' or '&' to get individual equations
        parts = re.split(r'\s+and\s+|\s*&\s*', clean_text)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # Look for equation pattern in this part
            equation_match = re.search(self.patterns['equation'], part)
            if equation_match:
                left_side = equation_match.group(1).strip()
                right_side = equation_match.group(2).strip()
                equation_text = f"{left_side} = {right_side}"
                
                try:
                    equation, symbols = self.parse_equation(equation_text)
                    equations.append((equation, symbols))
                except Exception as e:
                    print(f"Warning: Could not parse equation '{equation_text}': {e}")
        
        return equations
    
    def parse_quadratic_equation(self, text: str) -> Tuple[sp.Expr, Dict[str, sp.Symbol]]:
        """
        Parse quadratic equation in standard form ax² + bx + c = 0.
        
        Args:
            text (str): Quadratic equation text
            
        Returns:
            Tuple[sp.Expr, Dict[str, sp.Symbol]]: (Quadratic expression, variable symbols)
        """
        # First parse as regular equation
        equation, symbols = self.parse_equation(text)
        
        # Convert to standard form: ax² + bx + c = 0
        standard_form = sp.expand(equation.lhs - equation.rhs)
        
        return standard_form, symbols
    
    def parse_system_of_equations(self, text: str) -> Tuple[List[sp.Eq], Dict[str, sp.Symbol]]:
        """
        Parse a system of equations.
        
        Args:
            text (str): Text containing multiple equations
            
        Returns:
            Tuple[List[sp.Eq], Dict[str, sp.Symbol]]: (List of equations, variable symbols)
        """
        equations = self.extract_equations_from_text(text)
        
        if not equations:
            raise ValueError("No valid equations found in text")
        
        # Combine all symbols
        all_symbols = {}
        equation_list = []
        
        for equation, symbols in equations:
            equation_list.append(equation)
            all_symbols.update(symbols)
        
        return equation_list, all_symbols
    
    def validate_expression(self, expr: sp.Expr) -> Tuple[bool, str]:
        """
        Validate a SymPy expression.
        
        Args:
            expr (sp.Expr): SymPy expression
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # Check if expression is well-formed
            if expr is None:
                return False, "Expression is None"
            
            # Check for division by zero
            if hasattr(expr, 'denominator') and expr.denominator == 0:
                return False, "Division by zero detected"
            
            # Check for complex expressions that might cause issues
            if len(str(expr)) > 1000:
                return False, "Expression too complex"
            
            return True, "Valid expression"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def simplify_expression(self, expr: sp.Expr) -> sp.Expr:
        """
        Simplify a SymPy expression.
        
        Args:
            expr (sp.Expr): SymPy expression
            
        Returns:
            sp.Expr: Simplified expression
        """
        try:
            return sp.simplify(expr)
        except Exception as e:
            print(f"Warning: Could not simplify expression: {e}")
            return expr
    
    def factor_expression(self, expr: sp.Expr) -> sp.Expr:
        """
        Factor a SymPy expression.
        
        Args:
            expr (sp.Expr): SymPy expression
            
        Returns:
            sp.Expr: Factored expression
        """
        try:
            return sp.factor(expr)
        except Exception as e:
            print(f"Warning: Could not factor expression: {e}")
            return expr
    
    def expand_expression(self, expr: sp.Expr) -> sp.Expr:
        """
        Expand a SymPy expression.
        
        Args:
            expr (sp.Expr): SymPy expression
            
        Returns:
            sp.Expr: Expanded expression
        """
        try:
            return sp.expand(expr)
        except Exception as e:
            print(f"Warning: Could not expand expression: {e}")
            return expr
    
    def get_expression_info(self, expr: sp.Expr) -> Dict:
        """
        Get information about a SymPy expression.
        
        Args:
            expr (sp.Expr): SymPy expression
            
        Returns:
            Dict: Information about the expression
        """
        info = {
            'expression': str(expr),
            'degree': None,
            'variables': list(expr.free_symbols),
            'is_polynomial': False,
            'is_linear': False,
            'is_quadratic': False
        }
        
        try:
            # Get degree for polynomial expressions
            if expr.is_polynomial():
                info['is_polynomial'] = True
                info['degree'] = sp.degree(expr)
                
                if info['degree'] == 1:
                    info['is_linear'] = True
                elif info['degree'] == 2:
                    info['is_quadratic'] = True
                    
        except Exception as e:
            print(f"Warning: Could not analyze expression: {e}")
        
        return info 