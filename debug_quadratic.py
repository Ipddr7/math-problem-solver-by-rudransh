"""
Debug script specifically for quadratic equations
"""

from math_solver.nlp_processor import NLPProcessor
from math_solver.equation_parser import EquationParser
from math_solver.solver import MathSolver
import sympy as sp

def debug_quadratic():
    """Debug quadratic equation solving step by step."""
    print("🔍 Debugging Quadratic Equation")
    print("=" * 40)
    
    nlp = NLPProcessor()
    parser = EquationParser()
    solver = MathSolver()
    
    problem = "Find the roots of x^2 - 5x + 6 = 0"
    print(f"Problem: {problem}")
    print("-" * 30)
    
    # Step 1: NLP Analysis
    analysis = nlp.analyze_problem(problem)
    print(f"1. NLP Analysis: {analysis['problem_type']}")
    print(f"   Preprocessed: '{analysis['preprocessed_text']}'")
    
    # Step 2: Parse equation
    try:
        equation, symbols_dict = parser.parse_equation(analysis['preprocessed_text'])
        print(f"2. Parsed Equation: {equation}")
        print(f"   Symbols: {symbols_dict}")
        
        # Step 3: Solve
        solution = solver.solve_quadratic_equation(equation, symbols_dict)
        print(f"3. Solution Type: {solution['type']}")
        
        if 'error' in solution:
            print(f"   Error: {solution['error']}")
        else:
            print(f"   Solutions: {solution.get('solutions', 'No solutions')}")
            print(f"   Steps: {len(solution.get('steps', []))} steps")
            
    except Exception as e:
        print(f"Error during solving: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_quadratic() 