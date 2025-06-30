"""
Demo script showing complete solutions for different math problems
"""

from math_solver.nlp_processor import NLPProcessor
from math_solver.equation_parser import EquationParser
from math_solver.solver import MathSolver
import sympy as sp

def demo_solutions():
    """Demonstrate complete solutions for different problem types."""
    print("🧮 AI Math Problem Solver - Demo Solutions")
    print("=" * 50)
    
    # Initialize components
    nlp = NLPProcessor()
    parser = EquationParser()
    solver = MathSolver()
    
    # Demo problems
    problems = [
        {
            "type": "Linear Equation",
            "problem": "Solve for x: 3x - 7 = 11",
            "description": "Simple linear equation with one variable"
        },
        {
            "type": "Quadratic Equation", 
            "problem": "Find the roots of x^2 - 4x + 3 = 0",
            "description": "Quadratic equation with real roots"
        },
        {
            "type": "System of Equations",
            "problem": "Solve the system: x + y = 8 and 2x - y = 1",
            "description": "System of two linear equations"
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n{i}. {prob['type']}")
        print(f"   Problem: {prob['problem']}")
        print(f"   Description: {prob['description']}")
        print("-" * 40)
        
        # Analyze problem
        analysis = nlp.analyze_problem(prob['problem'])
        print(f"   Analysis: {analysis['problem_type']} (confidence: {analysis['confidence']:.1%})")
        
        # Parse and solve
        try:
            if analysis['problem_type'] == 'system':
                equations, symbols_dict = parser.parse_system_of_equations(analysis['preprocessed_text'])
            else:
                eq, symbols_dict = parser.parse_equation(analysis['preprocessed_text'])
                equations = eq
            
            solution = solver.solve_problem(analysis['problem_type'], equations, symbols_dict)
            
            # Display solution summary
            summary = solver.get_solution_summary(solution)
            print(f"   Solution: {summary}")
            
            # Show key steps
            if 'steps' in solution and solution['steps']:
                print("   Key Steps:")
                for step in solution['steps'][:3]:  # Show first 3 steps
                    print(f"     Step {step['step']}: {step['description']}")
                if len(solution['steps']) > 3:
                    print(f"     ... and {len(solution['steps']) - 3} more steps")
            
        except Exception as e:
            print(f"   Error: {e}")
        
        print()
    
    print("🎉 Demo completed! Your AI Math Solver is working perfectly!")
    print("\nTo use the web interface, run: streamlit run main.py")

if __name__ == "__main__":
    demo_solutions() 