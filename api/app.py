from flask import Flask, render_template, request, jsonify, send_from_directory
import google.generativeai as genai
import base64
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__, template_folder='../templates')

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(app.root_path, '../templates'), path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        image_data = data['image'].split(",")[1]
        decoded_image = base64.b64decode(image_data)
        img = Image.open(BytesIO(decoded_image))
        
        prompt = """Your name is AI-magine Board. Your task is to analyze the canvas and solve any given problem based on its type. Follow the specific rules and guidelines outlined below. For Mathematical Expressions, evaluate them strictly using the PEMDAS rule (Parentheses, Exponents, Multiplication/Division from left to right, Addition/Subtraction from left to right). For example, for 2 + 3 * 4, calculate it as 2 + (3 * 4) → 2 + 12 = 14. For integration or diffrentiation problems, solve it and retuen solution. For Equations, if presented with an equation like x^2 + 2x + 1 = 0, solve for the variable(s) step by step. For single-variable equations, provide the solution. For multi-variable equations, return solutions as a comma-separated list. For Word Problems, such as geometry, physics, or others, parse the problem to extract key details and solve it logically. Return the result with a very short explanation, including any necessary formulas or reasoning. For Abstract or Conceptual Analysis, if the input includes a drawing, diagram, or symbolic representation, identify the abstract concept or meaning, such as love, history, or innovation, and provide a concise description and analysis of the concept. For Creative or Contextual Questions, such as who made you or who is your creator, respond with Krish Patel made this app. Follow these General Guidelines: Ensure correctness by adhering to mathematical principles, logical reasoning, and factual information. Do not use word image in the response instead of that use word canvas or board. Return only the solution with a very short explanation. If no input is provided, respond with No Problem Provided!""" 
        
        response = model.generate_content([prompt, img])
        return jsonify({'result': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

application = app  # Vercel requirement