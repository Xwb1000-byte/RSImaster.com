from flask import Flask,Blueprint,jsonify
from flask import render_template
import sys
import os
sys.path.insert(0, os.path.expanduser('~/OneDrive/Desktop/Project'))

from your_code import get_approved_list, get_symbol_list, analyze_rsi



# Create a Blueprint named 'main'
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['GET'])
def analyze():
    try:
        approved_list = get_approved_list(r"C:\Users\arkgn\OneDrive\Desktop\kucoin_spot.xlsx")
        symbols = get_symbol_list(approved_list)
        results = analyze_rsi(symbols)
        if results == "Nothing to buy or sell yet ):":
            results = []
        return render_template('analyze.html', results=results)
    except Exception as e:
        return render_template('analyze.html', results=[], error=str(e))