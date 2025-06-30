"""
Test script for equation parsing
"""

from math_solver.equation_parser import EquationParser
from math_solver.nlp_processor import NLPProcessor

def test_parsing():
    """Test equation parsing with various input formats."""
    print("🔍 Testing Equation Parsing")
    print("=" * 40)
    
    parser = EquationParser()
    nlp = NLPProcessor()
    
    test_cases = [
        "Solve 2x^2 – 8x + 8 = 0",
        "Solve 3x + 7 = 1",
        "Find x if 4x – 16 = 0",
        "What is x if x²+2x=−3?",
        "Calculate 2*(x + 3) = 10"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Input: '{text}'")
        print("-" * 30)
        
        # Test extraction
        extracted = parser.extract_math_expression(text)
        print(f"   Extracted: '{extracted}'")
        
        # Test normalization
        try:
            normalized = parser.normalize_expression(text)
            print(f"   Normalized: '{normalized}'")
            
            # Test parsing
            analysis = nlp.analyze_problem(text)
            if analysis['problem_type'] != 'unknown':
                try:
                    if analysis['problem_type'] == 'system':
                        equations, symbols = parser.parse_system_of_equations(analysis['preprocessed_text'])
                        print(f"   ✅ Parsed: {len(equations)} equations")
                    else:
                        equation, symbols = parser.parse_equation(analysis['preprocessed_text'])
                        print(f"   ✅ Parsed: {equation}")
                except Exception as e:
                    print(f"   ❌ Parse error: {e}")
            else:
                print(f"   ❌ Unknown problem type")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_parsing() 