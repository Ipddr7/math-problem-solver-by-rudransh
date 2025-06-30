"""
AI Math Problem Solver Package

This package provides functionality to solve mathematical problems
using Natural Language Processing and Symbolic Computation.
"""

from .nlp_processor import NLPProcessor
from .equation_parser import EquationParser
from .solver import MathSolver
from .visualizer import MathVisualizer

__version__ = "1.0.0"
__author__ = "Student Project"

__all__ = ['NLPProcessor', 'EquationParser', 'MathSolver', 'MathVisualizer'] 