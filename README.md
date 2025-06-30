# AI Math Problem Solver

## Project Overview
This project implements an AI system that can understand and solve text-based mathematical problems, specifically focusing on **Quadratic Equations** and **Linear Equations**. The system uses Natural Language Processing (NLP) to interpret problem statements and symbolic computation to provide step-by-step solutions.

## Features
- **Text-to-Math Parsing**: Converts natural language math problems into mathematical expressions
- **Step-by-Step Solutions**: Provides detailed explanations for each solving step
- **Support for Multiple Equation Types**:
  - Linear Equations (ax + b = c)
  - Quadratic Equations (ax² + bx + c = 0)
  - Systems of Linear Equations
- **Interactive Web Interface**: User-friendly Streamlit application
- **Visual Solutions**: Graphs and visual representations of solutions

## AI Concepts Implemented
1. **Natural Language Processing (NLP)**: 
   - Text preprocessing and tokenization
   - Mathematical keyword extraction
   - Problem classification
   
2. **Symbolic Computation**:
   - Expression parsing and manipulation
   - Algebraic simplification
   - Step-by-step solution generation

## Project Structure
```
maths project/
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── main.py                  # Main application entry point
├── math_solver/
│   ├── __init__.py
│   ├── nlp_processor.py     # NLP for text processing
│   ├── equation_parser.py   # Mathematical expression parsing
│   ├── solver.py           # Core solving logic
│   └── visualizer.py       # Graphing and visualization
├── data/
│   ├── training_data.json   # Sample problems for testing
│   └── keywords.json        # Mathematical keywords mapping
└── tests/
    └── test_solver.py       # Unit tests
```

## Installation and Setup

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK Data**:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

3. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

## Usage Examples

### Linear Equations
- Input: "Solve for x: 2x + 5 = 13"
- Output: Step-by-step solution showing isolation of variable

### Quadratic Equations
- Input: "Find the roots of x² - 5x + 6 = 0"
- Output: Factorization, quadratic formula application, and solution set

### Systems of Equations
- Input: "Solve the system: x + y = 5 and 2x - y = 1"
- Output: Substitution/elimination method with detailed steps

## Technical Implementation

### NLP Processing Pipeline
1. **Text Preprocessing**: Clean and normalize input text
2. **Keyword Extraction**: Identify mathematical operations and variables
3. **Problem Classification**: Determine equation type (linear, quadratic, system)
4. **Expression Parsing**: Convert text to symbolic mathematical expressions

### Symbolic Computation
- Uses SymPy library for mathematical operations
- Handles variable isolation, factoring, and formula application
- Generates human-readable step explanations

### Solution Generation
- Breaks down complex problems into manageable steps
- Provides explanations for each mathematical operation
- Includes verification of solutions

## Educational Value
This project demonstrates:
- Integration of multiple AI concepts (NLP + Symbolic AI)
- Real-world application of mathematical libraries
- User interface design for educational tools
- Systematic problem-solving approaches

## Future Enhancements
- Support for more equation types (cubic, differential equations)
- Integration with computer vision for handwritten problems
- Multi-language support
- Adaptive difficulty levels
- Performance analytics and learning tracking

## Contributing
Feel free to extend this project with additional features or improvements!

## License
This project is created for educational purposes. 