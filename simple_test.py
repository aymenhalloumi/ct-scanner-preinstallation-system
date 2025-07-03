#!/usr/bin/env python3
"""
Simple test to verify Flask is working
"""

from flask import Flask, render_template_string

app = Flask(__name__)
app.secret_key = 'test-key'

@app.route('/')
def home():
    return '''
    <h1>🏥 CT Scanner System - WORKING!</h1>
    <p>✅ Flask is installed and running</p>
    <p>✅ Virtual environment is working</p>
    <a href="/test">Test Page</a>
    '''

@app.route('/test')
def test():
    return '''
    <h1>🧪 Test Page</h1>
    <p>✅ Routing is working</p>
    <a href="/">Back to Home</a>
    '''

if __name__ == '__main__':
    print("🚀 Starting Simple Test App...")
    print("🔗 Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)