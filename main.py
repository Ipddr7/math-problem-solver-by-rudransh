import streamlit as st
from math_solver.nlp_processor import NLPProcessor
from math_solver.equation_parser import EquationParser
from math_solver.solver import MathSolver
from math_solver.visualizer import MathVisualizer
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# --- App Config ---
st.set_page_config(
    page_title="AI Math Problem Solver",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Professional Theme ---
st.markdown("""
<style>
    body, .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }
    .header-container {
        background: #fff;
        border-radius: 18px;
        padding: 2.5rem 2rem 1.5rem 2rem;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .main-title {
        color: #1e293b;
        font-size: 2.7rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    .subtitle {
        color: #1e293b;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .how-to-card {
        background: #fff;
        border-radius: 14px;
        padding: 1.5rem 2rem;
        margin: 0 0 2rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        color: #1e293b;
        font-size: 1.08rem;
    }
    .section-card {
        background: #fff;
        border-radius: 14px;
        padding: 2rem;
        margin: 2rem 0 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        color: #1e293b;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .solution-summary {
        background: #e0f7fa;
        border-radius: 10px;
        padding: 1.2rem;
        color: #065f46;
        font-size: 1.15rem;
        font-weight: 600;
        margin: 1.5rem 0 0.5rem 0;
        border: 1.5px solid #4F46E5;
        box-shadow: 0 2px 8px rgba(79,70,229,0.07);
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1.5px solid #6366f1 !important;
        background: #fff !important;
        color: #1e293b !important;
        font-size: 1.08rem !important;
        transition: border-color 0.2s;
        min-height: 90px !important;
    }
    .stTextArea textarea::placeholder {
        color: #374151 !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 2px #6366f122 !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6366f1 0%, #4F46E5 100%);
        color: #fff;
        border: none;
        border-radius: 10px;
        padding: 0.9rem 2.2rem;
        font-size: 1.15rem;
        font-weight: 700;
        transition: background 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08);
        margin-top: 0.7rem;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #4F46E5 0%, #6366f1 100%);
        box-shadow: 0 4px 16px rgba(99,102,241,0.13);
    }
    .footer {
        background: #fff;
        border-radius: 14px;
        padding: 1.2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e5e7eb;
        color: #1e293b;
        font-size: 1rem;
    }
    @media (max-width: 768px) {
        .main-title { font-size: 1.3rem; }
        .section-header { font-size: 1.05rem; }
        .section-card, .how-to-card { padding: 1rem; }
        .header-container { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("""
<div class="header-container">
    <div style="font-size:2.5rem;">🧮</div>
    <div class="main-title">AI Math Problem Solver</div>
    <div class="subtitle">Enter your algebra problem below and get a step-by-step solution with explanations!</div>
</div>
""", unsafe_allow_html=True)

# --- How to Use Card ---
st.markdown("""
<div class="how-to-card">
    <div class="section-header">📖 How to Use</div>
    <ol style="margin-left:1.2rem;">
        <li>Type your math problem in plain English (e.g., <span style='color:#4F46E5;'>Solve for x: 2x + 5 = 13</span>).</li>
        <li>Click <b>Solve</b> to get a step-by-step solution.</li>
        <li>Try linear, quadratic, or system of equations!</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# --- Sidebar with Clean Markdown ---
st.sidebar.title("🚀 Features")
st.sidebar.markdown("""
- **NLP Processing**: Understands natural language
- **Step-by-Step Solutions**: Detailed explanations
- **Multiple Problem Types**: Linear, Quadratic, Systems
- **AI-Powered**: Advanced algorithms

---
**Instructions:**

1. Enter a math problem in plain English  
   _e.g., "Solve for x: 2x + 5 = 13"_
2. Click **Solve** to see step-by-step solutions.
3. Try linear, quadratic, or system of equations!

---
**Developer:** Rudransh Gupta  
**Project:** Math Equation Solver
""")

# --- Initialize AI Components ---
@st.cache_resource
def load_ai_components():
    """Load AI components with caching for better performance."""
    return {
        'nlp': NLPProcessor(),
        'parser': EquationParser(),
        'solver': MathSolver(),
        'visualizer': MathVisualizer()
    }

components = load_ai_components()

# --- Main Content Area ---
# Input Card
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🎯 Enter Your Math Problem</div>', unsafe_allow_html=True)
user_input = st.text_area(
    "Type your algebra problem here...",
    height=110,
    placeholder="Examples:\n• Solve for x: 2x + 5 = 13\n• Find the roots of x² - 5x + 6 = 0\n• Solve the system: x + y = 5 and 2x - y = 1"
)
solve_button = st.button("🚀 Solve Problem", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if solve_button and user_input and len(user_input.strip()) > 4:
    with st.spinner("Analyzing and solving your problem..."):
        try:
            # NLP Analysis
            analysis = components['nlp'].analyze_problem(user_input)
            if analysis['problem_type'] != 'unknown':
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-header">🔎 Problem Analysis</div>', unsafe_allow_html=True)
                colA, colB, colC, colD = st.columns(4)
                colA.metric("Type", analysis['problem_type'].title())
                colB.metric("Confidence", f"{analysis['confidence']:.0%}")
                colC.metric("Variables", len(analysis['variables']))
                colD.metric("Numbers", len(analysis['numbers']))
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Sorry, I couldn't recognize the type of math problem. Please try rephrasing.")
                st.info("Examples: 'Solve for x: 2x + 5 = 13', 'Find the roots of x^2 - 5x + 6 = 0'")
                analysis = None
            if analysis and analysis['problem_type'] != 'unknown':
                # Parse equations
                try:
                    if analysis['problem_type'] == 'system':
                        equations, symbols_dict = components['parser'].parse_system_of_equations(analysis['preprocessed_text'])
                    elif analysis['problem_type'] == 'quadratic':
                        eq, symbols_dict = components['parser'].parse_equation(analysis['preprocessed_text'])
                        equations = eq
                    else:  # linear
                        eq, symbols_dict = components['parser'].parse_equation(analysis['preprocessed_text'])
                        equations = eq
                except Exception as e:
                    st.error(f"Equation parsing error: {e}")
                    st.info("Please check your equation format and try again.")

                # Solve
                try:
                    solution = components['solver'].solve_problem(analysis['problem_type'], equations, symbols_dict)
                except Exception as e:
                    st.error(f"Solving error: {e}")

                # Display solution steps if available
                if solution.get('steps'):
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-header">📝 Step-by-Step Solution</div>', unsafe_allow_html=True)
                    components['visualizer'].display_solution_steps(solution)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Display solution summary if available, in a green card with checkmark
                summary = components['solver'].get_solution_summary(solution)
                if summary and 'Unknown problem type' not in summary:
                    st.markdown('''
                    <div style="background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%); border-radius: 14px; padding: 1.5rem 2rem; margin: 2rem 0 1.5rem 0; box-shadow: 0 2px 8px rgba(67,233,123,0.10); display: flex; align-items: flex-start; gap: 1.2rem;">
                        <div style="font-size:2.1rem; margin-right:0.7rem;">✅</div>
                        <div>
                            <div style="font-size:1.6rem; font-weight:800; color:#1e293b; margin-bottom:0.5rem;">Solution Summary</div>
                            <div style="font-size:1.15rem; color:#065f46; font-weight:600;">{}</div>
                        </div>
                    </div>
                    '''.format(summary), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try a different problem or check your input format.")

# --- Footer ---
st.markdown("""
<div class="footer">
    <p style="margin: 0; color: var(--text-secondary);">
        Made by <strong style="color: var(--primary-color);">Rudransh Gupta</strong> | 
        Powered by <strong style="color: var(--accent-color);">Streamlit</strong>, 
        <strong style="color: var(--secondary-color);">SymPy</strong>, and 
        <strong style="color: var(--primary-color);">AI</strong>
    </p>
</div>
""", unsafe_allow_html=True) 