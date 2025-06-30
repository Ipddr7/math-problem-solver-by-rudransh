"""
Debug script for equation parser
"""

from math_solver.equation_parser import EquationParser
from math_solver.nlp_processor import NLPProcessor

def debug_parsing():
    """Debug the equation parsing step by step."""
    print("🔍 Debugging Equation Parser")
    print("=" * 40)
    
    parser = EquationParser()
    nlp = NLPProcessor()
    
    test_cases = [
        "Solve for x: 2x + 5 = 13",
        "Find the roots of x^2 - 5x + 6 = 0",
        "Solve the system: x + y = 5 and 2x - y = 1"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{text}'")
        print("-" * 30)
        
        # Step 1: NLP Analysis
        analysis = nlp.analyze_problem(text)
        print(f"   NLP Analysis: {analysis['problem_type']}")
        print(f"   Preprocessed: '{analysis['preprocessed_text']}'")
        
        # Step 2: Extract math expression
        math_expr = parser.extract_math_expression(text)
        print(f"   Math Expression: '{math_expr}'")
        
        # Step 3: Normalize
        normalized = parser.normalize_expression(text)
        print(f"   Normalized: '{normalized}'")
        
        # Step 4: Try parsing
        try:
            if analysis['problem_type'] == 'system':
                equations, symbols = parser.parse_system_of_equations(analysis['preprocessed_text'])
                print(f"   ✅ System parsed: {len(equations)} equations")
            else:
                equation, symbols = parser.parse_equation(analysis['preprocessed_text'])
                print(f"   ✅ Equation parsed: {equation}")
        except Exception as e:
            print(f"   ❌ Parse error: {e}")

if __name__ == "__main__":
    debug_parsing() 