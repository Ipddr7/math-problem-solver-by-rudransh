"""
Math Visualizer Module

This module provides visualization capabilities for mathematical expressions,
equations, and solutions.
"""

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from typing import Dict, List, Optional, Union
import streamlit as st

class MathVisualizer:
    """
    Visualizer for mathematical expressions and solutions.
    
    This class handles:
    - Plotting equations and functions
    - Visualizing solutions and roots
    - Creating interactive graphs
    - Generating mathematical diagrams
    """
    
    def __init__(self):
        """Initialize the math visualizer."""
        self.default_colors = ['#4F8BF9', '#F97C4F', '#4FBF97', '#BF4F8B', '#8B4FBF']
        self.default_style = {
            'figure.figsize': (10, 6),
            'axes.grid': True,
            'grid.alpha': 0.3
        }
    
    def plot_linear_equation(self, equation: sp.Eq, variable: sp.Symbol, 
                           solution: Optional[sp.Expr] = None, 
                           x_range: tuple = (-10, 10)) -> plt.Figure:
        """
        Plot a linear equation.
        
        Args:
            equation (sp.Eq): Linear equation
            variable (sp.Symbol): Variable symbol
            solution (Optional[sp.Expr]): Solution point to highlight
            x_range (tuple): Range for x-axis
            
        Returns:
            plt.Figure: Matplotlib figure
        """
        # Convert equation to standard form: y = mx + b
        left_side = equation.lhs - equation.rhs
        expr = sp.simplify(left_side)
        
        # Create function for plotting
        f = sp.lambdify(variable, expr, modules=['numpy'])
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        y_vals = f(x_vals)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, label=f"y = {expr}", color=self.default_colors[0], linewidth=2)
        ax.axhline(0, color='gray', linestyle='-', alpha=0.5)
        ax.axvline(0, color='gray', linestyle='-', alpha=0.5)
        
        # Plot solution point if provided
        if solution is not None:
            ax.plot(float(solution), 0, 'ro', markersize=8, label=f'Solution: {variable} = {solution}')
        
        ax.set_xlabel(str(variable))
        ax.set_ylabel('y')
        ax.set_title('Linear Equation Graph')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_quadratic_equation(self, equation: sp.Eq, variable: sp.Symbol,
                              solutions: Optional[List[sp.Expr]] = None,
                              x_range: tuple = (-10, 10)) -> plt.Figure:
        """
        Plot a quadratic equation.
        
        Args:
            equation (sp.Eq): Quadratic equation
            variable (sp.Symbol): Variable symbol
            solutions (Optional[List[sp.Expr]]): Solution points to highlight
            x_range (tuple): Range for x-axis
            
        Returns:
            plt.Figure: Matplotlib figure
        """
        # Convert to standard form: ax² + bx + c = 0
        left_side = equation.lhs - equation.rhs
        expr = sp.expand(left_side)
        
        # Create function for plotting
        f = sp.lambdify(variable, expr, modules=['numpy'])
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        y_vals = f(x_vals)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, label=f"y = {expr}", color=self.default_colors[0], linewidth=2)
        ax.axhline(0, color='gray', linestyle='-', alpha=0.5)
        ax.axvline(0, color='gray', linestyle='-', alpha=0.5)
        
        # Plot solution points if provided
        if solutions:
            for i, solution in enumerate(solutions):
                if sp.im(solution) == 0:  # Only plot real solutions
                    ax.plot(float(solution), 0, 'ro', markersize=8, 
                           label=f'Root {i+1}: {variable} = {solution}')
        
        ax.set_xlabel(str(variable))
        ax.set_ylabel('y')
        ax.set_title('Quadratic Equation Graph')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def plot_system_of_equations(self, equations: List[sp.Eq], 
                                variables: List[sp.Symbol],
                                solution: Optional[Dict] = None,
                                x_range: tuple = (-10, 10)) -> plt.Figure:
        """
        Plot a system of equations (2D only).
        
        Args:
            equations (List[sp.Eq]): List of equations
            variables (List[sp.Symbol]): Variable symbols
            solution (Optional[Dict]): Solution point to highlight
            x_range (tuple): Range for x-axis
            
        Returns:
            plt.Figure: Matplotlib figure
        """
        if len(variables) != 2:
            raise ValueError("Only 2D systems are supported for visualization")
        
        x, y = variables[0], variables[1]
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot each equation
        for i, equation in enumerate(equations):
            try:
                # Solve for y in terms of x
                y_expr = sp.solve(equation, y)[0]
                f = sp.lambdify(x, y_expr, modules=['numpy'])
                y_vals = f(x_vals)
                
                ax.plot(x_vals, y_vals, label=f"Eq {i+1}: {equation}", 
                       color=self.default_colors[i % len(self.default_colors)], linewidth=2)
            except Exception as e:
                # If we can't solve for y, try solving for x
                try:
                    x_expr = sp.solve(equation, x)[0]
                    f = sp.lambdify(y, x_expr, modules=['numpy'])
                    y_vals = np.linspace(x_range[0], x_range[1], 400)
                    x_vals_plot = f(y_vals)
                    
                    ax.plot(x_vals_plot, y_vals, label=f"Eq {i+1}: {equation}", 
                           color=self.default_colors[i % len(self.default_colors)], linewidth=2)
                except:
                    continue
        
        # Plot solution point if provided
        if solution and isinstance(solution, dict):
            try:
                x_sol = float(solution[x])
                y_sol = float(solution[y])
                ax.plot(x_sol, y_sol, 'ro', markersize=8, label='Solution')
            except:
                pass
        
        ax.axhline(0, color='gray', linestyle='-', alpha=0.5)
        ax.axvline(0, color='gray', linestyle='-', alpha=0.5)
        ax.set_xlabel(str(x))
        ax.set_ylabel(str(y))
        ax.set_title('System of Equations')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def create_solution_summary(self, solution: Dict) -> str:
        """
        Create a formatted summary of the solution.
        
        Args:
            solution (Dict): Solution dictionary
            
        Returns:
            str: Formatted solution summary
        """
        if 'error' in solution:
            return f"❌ **Error:** {solution['error']}"
        
        summary = "✅ **Solution Summary:**\n\n"
        
        if solution['type'] == 'linear':
            summary += f"**Equation:** {solution['equation']}\n"
            summary += f"**Variable:** {solution['variable']}\n"
            summary += f"**Solution:** {solution['variable']} = {solution['solution']}\n"
            summary += f"**Verification:** {'✅ Correct' if solution['verification'] else '❌ Incorrect'}"
            
        elif solution['type'] == 'quadratic':
            summary += f"**Equation:** {solution['equation']}\n"
            summary += f"**Variable:** {solution['variable']}\n"
            if 'coefficients' in solution:
                coeffs = solution['coefficients']
                summary += f"**Coefficients:** a = {coeffs['a']}, b = {coeffs['b']}, c = {coeffs['c']}\n"
            if 'discriminant' in solution and solution['discriminant'] is not None:
                summary += f"**Discriminant:** Δ = {solution['discriminant']}\n"
            summary += f"**Solutions:** {solution['variable']} = {solution['solutions']}\n"
            summary += f"**Verification:** {'✅ Correct' if solution['verification'] else '❌ Incorrect'}"
            
        elif solution['type'] == 'system':
            summary += f"**Equations:**\n"
            for i, eq in enumerate(solution['equations']):
                summary += f"  {i+1}. {eq}\n"
            summary += f"**Variables:** {', '.join(solution['variables'])}\n"
            summary += f"**Solutions:** {solution['solutions']}\n"
            summary += f"**Verification:** {'✅ Correct' if solution['verification'] else '❌ Incorrect'}"
        
        return summary
    
    def display_solution_steps(self, solution: Dict) -> None:
        """
        Display solution steps in a formatted way.
        
        Args:
            solution (Dict): Solution dictionary with steps
        """
        if 'steps' not in solution:
            st.warning("No steps available for this solution.")
            return
        
        st.subheader("📝 Step-by-Step Solution")
        
        for step in solution['steps']:
            with st.expander(f"Step {step['step']}: {step['description']}", expanded=True):
                st.markdown(f"**{step['content']}**")
    
    def display_visualization(self, solution: Dict, equation_parser, symbols_dict: Dict) -> None:
        """
        Display appropriate visualization based on solution type.
        
        Args:
            solution (Dict): Solution dictionary
            equation_parser: Equation parser instance
            symbols_dict (Dict): Variable symbols dictionary
        """
        st.subheader("📈 Visualization")
        
        try:
            # Check if we have the necessary data
            if not solution or 'type' not in solution:
                st.info("No solution data available for visualization.")
                return
                
            if not symbols_dict:
                st.info("No variable symbols found for visualization.")
                return
            
            if solution['type'] == 'linear':
                if not symbols_dict:
                    st.info("No variable symbols found for linear equation visualization.")
                    return
                    
                variable = list(symbols_dict.values())[0]
                if 'equation' not in solution:
                    st.info("No equation data available for visualization.")
                    return
                    
                # Parse equation safely
                try:
                    eq_parts = solution['equation'].split('=')
                    if len(eq_parts) != 2:
                        st.info("Invalid equation format for visualization.")
                        return
                        
                    left_side = sp.sympify(eq_parts[0].strip())
                    right_side = sp.sympify(eq_parts[1].strip())
                    equation = sp.Eq(left_side, right_side)
                    
                    fig = self.plot_linear_equation(
                        equation=equation,
                        variable=variable,
                        solution=solution.get('solution')
                    )
                    st.pyplot(fig)
                except Exception as e:
                    st.info(f"Could not parse equation for visualization: {str(e)}")
                
            elif solution['type'] == 'quadratic':
                if not symbols_dict:
                    st.info("No variable symbols found for quadratic equation visualization.")
                    return
                    
                variable = list(symbols_dict.values())[0]
                if 'equation' not in solution:
                    st.info("No equation data available for visualization.")
                    return
                    
                # Parse equation safely
                try:
                    eq_parts = solution['equation'].split('=')
                    if len(eq_parts) != 2:
                        st.info("Invalid equation format for visualization.")
                        return
                        
                    left_side = sp.sympify(eq_parts[0].strip())
                    right_side = sp.sympify(eq_parts[1].strip())
                    equation = sp.Eq(left_side, right_side)
                    
                    fig = self.plot_quadratic_equation(
                        equation=equation,
                        variable=variable,
                        solutions=solution.get('solutions')
                    )
                    st.pyplot(fig)
                except Exception as e:
                    st.info(f"Could not parse equation for visualization: {str(e)}")
                
            elif solution['type'] == 'system':
                if len(symbols_dict) != 2:
                    st.info("Visualization for systems with more than 2 variables is not supported.")
                    return
                    
                if 'equations' not in solution:
                    st.info("No equations data available for system visualization.")
                    return
                    
                variables = list(symbols_dict.values())
                
                # Parse equations safely
                try:
                    equations = []
                    for eq_str in solution['equations']:
                        eq_parts = eq_str.split('=')
                        if len(eq_parts) != 2:
                            continue
                        left_side = sp.sympify(eq_parts[0].strip())
                        right_side = sp.sympify(eq_parts[1].strip())
                        equations.append(sp.Eq(left_side, right_side))
                    
                    if not equations:
                        st.info("Could not parse any equations for system visualization.")
                        return
                        
                    fig = self.plot_system_of_equations(
                        equations=equations,
                        variables=variables,
                        solution=solution.get('solutions')
                    )
                    st.pyplot(fig)
                except Exception as e:
                    st.info(f"Could not parse equations for system visualization: {str(e)}")
            else:
                st.info(f"Visualization not supported for problem type: {solution['type']}")
                    
        except Exception as e:
            st.info(f"Visualization not available: {str(e)}")
    
    def create_problem_analysis_display(self, analysis: Dict) -> None:
        """
        Display problem analysis in a formatted way.
        
        Args:
            analysis (Dict): Problem analysis dictionary
        """
        st.subheader("🔎 Problem Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Problem Type", analysis['problem_type'].title())
            st.metric("Confidence", f"{analysis['confidence']:.2%}")
        
        with col2:
            st.metric("Variables Found", len(analysis['variables']))
            st.metric("Numbers Found", len(analysis['numbers']))
        
        with st.expander("Detailed Analysis", expanded=False):
            st.json(analysis) 