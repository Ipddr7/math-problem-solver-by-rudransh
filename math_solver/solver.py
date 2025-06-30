"""
Core Math Solver Module

This module provides step-by-step solutions for various types of mathematical problems
including linear equations, quadratic equations, and systems of equations.
"""

import sympy as sp
from sympy import solve, Eq, symbols, simplify, expand, factor, sqrt
from typing import Dict, List, Tuple, Optional, Union
import math

class MathSolver:
    """
    Core mathematical problem solver with step-by-step solutions.
    
    This class handles:
    - Linear equation solving
    - Quadratic equation solving
    - System of equations solving
    - Step-by-step solution generation
    - Solution verification
    """
    
    def __init__(self):
        """Initialize the math solver."""
        self.solution_steps = []
        self.current_step = 0
    
    def solve_linear_equation(self, equation: sp.Eq, symbols_dict: Dict[str, sp.Symbol]) -> Dict:
        """
        Solve a linear equation step by step.
        
        Args:
            equation (sp.Eq): Linear equation
            symbols_dict (Dict[str, sp.Symbol]): Variable symbols
            
        Returns:
            Dict: Complete solution with steps and answer
        """
        self.solution_steps = []
        self.current_step = 0
        
        # Get the variable to solve for
        variable = list(symbols_dict.values())[0]
        
        # Step 1: Original equation
        self._add_step("Original equation", str(equation))
        
        # Step 2: Move all terms to left side
        left_side = equation.lhs - equation.rhs
        self._add_step("Move all terms to left side", f"{left_side} = 0")
        
        # Step 3: Simplify
        simplified = sp.simplify(left_side)
        self._add_step("Simplify", f"{simplified} = 0")
        
        # Step 4: Isolate variable
        try:
            solution = sp.solve(simplified, variable)
            # Infinite solutions: equation simplifies to 0 = 0
            if simplified == 0:
                self._add_step("Infinite solutions", "The equation is always true. All real values of x are solutions.")
                return {
                    'type': 'linear',
                    'equation': str(equation),
                    'variable': str(variable),
                    'solution': 'all real x',
                    'steps': self.solution_steps,
                    'verification': True
                }
            # No solution: equation simplifies to a contradiction (e.g., 0 = 5)
            if not solution:
                if not variable in simplified.free_symbols and simplified != 0:
                    self._add_step("No solution", "The equation has no solution (contradiction).")
                    return {
                        'type': 'linear',
                        'equation': str(equation),
                        'variable': str(variable),
                        'solution': 'no real x',
                        'steps': self.solution_steps,
                        'verification': False
                    }
                else:
                    self._add_step("No solution", "No solution found.")
                    return {
                        'type': 'linear',
                        'equation': str(equation),
                        'variable': str(variable),
                        'solution': None,
                        'steps': self.solution_steps,
                        'verification': False
                    }
            self._add_step("Solve for variable", f"{variable} = {solution[0]}")
            
            # Step 5: Verify solution
            verification = simplified.subs(variable, solution[0])
            self._add_step("Verify solution", f"Substituting {variable} = {solution[0]}: {verification} = 0")
            
            return {
                'type': 'linear',
                'equation': str(equation),
                'variable': str(variable),
                'solution': solution[0],
                'steps': self.solution_steps,
                'verification': verification == 0
            }
        except Exception as e:
            self._add_step("Error", f"Could not solve equation: {str(e)}")
            return {
                'type': 'linear',
                'equation': str(equation),
                'variable': str(variable),
                'solution': None,
                'steps': self.solution_steps,
                'error': str(e)
            }
    
    def solve_quadratic_equation(self, equation: sp.Eq, symbols_dict: Dict[str, sp.Symbol]) -> Dict:
        """
        Solve a quadratic equation step by step.
        
        Args:
            equation (sp.Eq): Quadratic equation
            symbols_dict (Dict[str, sp.Symbol]): Variable symbols
            
        Returns:
            Dict: Complete solution with steps and answer
        """
        self.solution_steps = []
        self.current_step = 0
        
        variable = list(symbols_dict.values())[0]
        
        # Step 1: Original equation
        self._add_step("Original equation", str(equation))
        
        # Step 2: Convert to standard form ax² + bx + c = 0
        standard_form = sp.expand(equation.lhs - equation.rhs)
        self._add_step("Standard form", f"{standard_form} = 0")
        
        # Step 3: Identify coefficients
        try:
            # Get coefficients
            poly = sp.Poly(standard_form, variable)
            coeffs = poly.all_coeffs()
            # Ensure a, b, c are always present
            while len(coeffs) < 3:
                coeffs.insert(0, 0)
            a, b, c = coeffs[-3], coeffs[-2], coeffs[-1]
            self._add_step("Coefficients", f"a = {a}, b = {b}, c = {c}")
            
            # Check if it's actually quadratic
            if a == 0:
                self._add_step("Degenerate quadratic", "a=0, treating as linear equation.")
                return self.solve_linear_equation(sp.Eq(standard_form, 0), symbols_dict)
            
            # Step-by-step factorization
            factored = sp.factor(standard_form)
            if factored != standard_form:
                # Step 1: Factor out GCD if present
                gcd = sp.gcd_terms(standard_form)
                if gcd != standard_form:
                    self._add_step("Factor out GCD", f"{standard_form} = {gcd}")
                # Step 2: Show full factorization
                self._add_step("Full factorization", f"{standard_form} = {factored}")
                # Step 3: Set each factor to zero and solve
                factors = sp.factor_list(standard_form)[1]
                roots = []
                for base, exp in factors:
                    for _ in range(exp):
                        eq = sp.Eq(base, 0)
                        sol = sp.solve(eq, variable)
                        self._add_step(f"Solve factor: {sp.pretty(eq)}", f"{variable} = {sol}")
                        roots.extend(sol)
                solutions = roots
            else:
                # Step 5: Use quadratic formula
                self._add_step("Method", "Using quadratic formula: x = (-b ± √(b² - 4ac)) / (2a)")
                
                # Calculate discriminant
                discriminant = b**2 - 4*a*c
                self._add_step("Discriminant", f"Δ = b² - 4ac = {b}² - 4({a})({c}) = {discriminant}")
                
                if discriminant > 0:
                    # Two real solutions
                    x1 = (-b + sp.sqrt(discriminant)) / (2*a)
                    x2 = (-b - sp.sqrt(discriminant)) / (2*a)
                    
                    self._add_step("Two real solutions", 
                                 f"x₁ = (-{b} + √{discriminant}) / (2×{a}) = {x1}")
                    self._add_step("", f"x₂ = (-{b} - √{discriminant}) / (2×{a}) = {x2}")
                    
                    solutions = [x1, x2]
                    
                elif discriminant == 0:
                    # One real solution
                    x = -b / (2*a)
                    self._add_step("One real solution (repeated root)", f"x = -{b} / (2×{a}) = {x}")
                    solutions = [x]
                    
                else:
                    # Complex solutions
                    self._add_step("Complex solutions", "Discriminant is negative, solutions are complex")
                    solutions = sp.solve(standard_form, variable)
                    self._add_step("Complex solutions", f"{variable} = {solutions}")
            
            # Step 6: Verify solutions
            for i, solution in enumerate(solutions):
                verification = standard_form.subs(variable, solution)
                self._add_step(f"Verify solution {i+1}", 
                             f"Substituting {variable} = {solution}: {verification} = 0")
            
            return {
                'type': 'quadratic',
                'equation': str(equation),
                'variable': str(variable),
                'coefficients': {'a': a, 'b': b, 'c': c},
                'discriminant': discriminant if 'discriminant' in locals() else None,
                'solutions': solutions,
                'steps': self.solution_steps,
                'verification': all(standard_form.subs(variable, sol) == 0 for sol in solutions)
            }
            
        except Exception as e:
            self._add_step("Error", f"Could not solve quadratic equation: {str(e)}")
            return {
                'type': 'quadratic',
                'equation': str(equation),
                'variable': str(variable),
                'solution': None,
                'steps': self.solution_steps,
                'error': str(e)
            }
    
    def solve_system_of_equations(self, equations: List[sp.Eq], symbols_dict: Dict[str, sp.Symbol]) -> Dict:
        """
        Solve a system of equations step by step.
        
        Args:
            equations (List[sp.Eq]): List of equations
            symbols_dict (Dict[str, sp.Symbol]): Variable symbols
            
        Returns:
            Dict: Complete solution with steps and answer
        """
        self.solution_steps = []
        self.current_step = 0
        
        variables = list(symbols_dict.values())
        
        # Step 1: Original system
        self._add_step("Original system", "\n".join([str(eq) for eq in equations]))
        
        try:
            # Step 2: Solve system
            solutions = sp.solve(equations, variables)
            
            if solutions:
                if isinstance(solutions, list):
                    # Multiple solutions
                    self._add_step("Solutions", f"System has {len(solutions)} solution(s)")
                    for i, solution in enumerate(solutions):
                        self._add_step(f"Solution {i+1}", str(solution))
                else:
                    # Single solution
                    self._add_step("Solution", str(solutions))
                
                # Step 3: Verify solutions
                for i, eq in enumerate(equations):
                    if isinstance(solutions, list):
                        for j, solution in enumerate(solutions):
                            verification = eq.subs(solution)
                            self._add_step(f"Verify equation {i+1}, solution {j+1}", 
                                         f"Substituting: {verification} = 0")
                    else:
                        verification = eq.subs(solutions)
                        self._add_step(f"Verify equation {i+1}", 
                                     f"Substituting: {verification} = 0")
                
                return {
                    'type': 'system',
                    'equations': [str(eq) for eq in equations],
                    'variables': [str(var) for var in variables],
                    'solutions': solutions,
                    'steps': self.solution_steps,
                    'verification': True
                }
            else:
                self._add_step("No solution", "The system has no solution")
                return {
                    'type': 'system',
                    'equations': [str(eq) for eq in equations],
                    'variables': [str(var) for var in variables],
                    'solutions': None,
                    'steps': self.solution_steps,
                    'verification': False
                }
                
        except Exception as e:
            self._add_step("Error", f"Could not solve system: {str(e)}")
            return {
                'type': 'system',
                'equations': [str(eq) for eq in equations],
                'variables': [str(var) for var in variables],
                'solutions': None,
                'steps': self.solution_steps,
                'error': str(e)
            }
    
    def solve_problem(self, problem_type: str, equations: Union[sp.Eq, List[sp.Eq]], 
                     symbols_dict: Dict[str, sp.Symbol]) -> Dict:
        """
        Main solving method that routes to appropriate solver based on problem type.
        
        Args:
            problem_type (str): Type of problem ('linear', 'quadratic', 'system')
            equations (Union[sp.Eq, List[sp.Eq]]): Equation(s) to solve
            symbols_dict (Dict[str, sp.Symbol]): Variable symbols
            
        Returns:
            Dict: Complete solution
        """
        if problem_type == 'linear':
            return self.solve_linear_equation(equations, symbols_dict)
        elif problem_type == 'quadratic':
            return self.solve_quadratic_equation(equations, symbols_dict)
        elif problem_type == 'system':
            return self.solve_system_of_equations(equations, symbols_dict)
        else:
            return {
                'type': 'unknown',
                'error': f"Unknown problem type: {problem_type}",
                'steps': []
            }
    
    def _add_step(self, description: str, content: str):
        """
        Add a step to the solution.
        
        Args:
            description (str): Step description
            content (str): Step content
        """
        self.current_step += 1
        self.solution_steps.append({
            'step': self.current_step,
            'description': description,
            'content': content
        })
    
    def get_solution_summary(self, solution: Dict) -> str:
        """
        Generate a summary of the solution.
        
        Args:
            solution (Dict): Solution dictionary
            
        Returns:
            str: Formatted solution summary
        """
        if 'error' in solution:
            return f"Error: {solution['error']}"
        
        if solution['type'] == 'linear':
            return f"Solution: {solution['variable']} = {solution['solution']}"
        elif solution['type'] == 'quadratic':
            if len(solution['solutions']) == 1:
                return f"Solution: {solution['variable']} = {solution['solutions'][0]}"
            else:
                return f"Solutions: {solution['variable']} = {solution['solutions']}"
        elif solution['type'] == 'system':
            return f"Solutions: {solution['solutions']}"
        else:
            return "Unknown problem type"
    
    def verify_solution(self, equation: sp.Eq, solution: Union[sp.Expr, Dict], 
                       variable: sp.Symbol) -> bool:
        """
        Verify if a solution is correct.
        
        Args:
            equation (sp.Eq): Original equation
            solution (Union[sp.Expr, Dict]): Solution to verify
            variable (sp.Symbol): Variable symbol
            
        Returns:
            bool: True if solution is correct
        """
        try:
            if isinstance(solution, dict):
                # Handle system of equations
                verification = equation.subs(solution)
            else:
                # Handle single equation
                verification = equation.subs(variable, solution)
            
            return sp.simplify(verification) == 0
        except Exception:
            return False 