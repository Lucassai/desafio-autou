from flask import Flask, request, render_template
from src.ai import process_email_message
import os 
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        result = process_email_message(email_text=message, use_openai_for_reply=True)
        print(result)
        return render_template('index.html', result_text=result.get('suggested_reply', 'No reply generated.'))
    except Exception as e:
        print(f"Erro processando seu email: {e}")
        
        return render_template('index.html', error="Erro processando sua mensagem.")

if __name__ == '__main__':
    print ("Starting Flask app...")
    app.run(debug=True)