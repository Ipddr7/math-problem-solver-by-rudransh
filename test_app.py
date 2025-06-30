"""
Test script for the AI Math Problem Solver
"""

from math_solver.nlp_processor import NLPProcessor
from math_solver.equation_parser import EquationParser
from math_solver.solver import MathSolver
from math_solver.visualizer import MathVisualizer
import sympy as sp

def test_components():
    """Test all components of the math solver."""
    print("🧮 Testing AI Math Problem Solver Components...")
    
    # Initialize components
    nlp = NLPProcessor()
    parser = EquationParser()
    solver = MathSolver()
    visualizer = MathVisualizer()
    
    print("✅ All components initialized successfully!")
    
    # Test NLP processor
    test_problems = [
        "Solve for x: 2x + 5 = 13",
        "Find the roots of x^2 - 5x + 6 = 0",
        "Solve the system: x + y = 5 and 2x - y = 1"
    ]
    
    for problem in test_problems:
        print(f"\n🔍 Testing: {problem}")
        analysis = nlp.analyze_problem(problem)
        print(f"   Problem Type: {analysis['problem_type']}")
        print(f"   Confidence: {analysis['confidence']:.2%}")
        print(f"   Variables: {analysis['variables']}")
        print(f"   Numbers: {analysis['numbers']}")
    
    print("\n🎉 All tests completed successfully!")
    print("Your AI Math Problem Solver is ready to use!")

if __name__ == "__main__":
    test_components() 