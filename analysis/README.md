### Setup
1. Install Python 3.8: https://www.python.org/downloads/release/python-3810/. When installing, do not add Python 3.8 to PATH.
2. Install virtualenv: `pip install virtualenv`
3. Create a virtual environment: `virtualenv --python=python3.8 .\venv`
4. Activate the virtual environment:
   - For Windows: `.\venv\Scripts\activate`
   - For macOS/Linux: `source venv/bin/activate`
5. Install the required dependencies: `pip install -r requirements.txt`

### Usage
1. Activate the virtual environment:
   - For Windows: `.\venv\Scripts\activate`
   - For macOS/Linux: `source venv/bin/activate`
2. Start the development server: `python analysis.py`
