# ===============================
# 📦 Import Required Libraries
# ===============================

# Flask framework for creating the web application
from flask import Flask, request, render_template  

# Data manipulation libraries
import numpy as np
import pandas as pd  

# Data preprocessing from scikit-learn
from sklearn.preprocessing import StandardScaler  

# Importing custom modules for data and prediction pipeline
# (These are from your local 'src/pipeline' folder)
from src.pipeline.predict_pipeline import CustomData, PredictPipeline  


# ===============================
# 🚀 Flask App Initialization
# ===============================

# Create Flask application instance
application = Flask(__name__)  

# Assign alias for easier reference
app = application  


# ===============================
# 🏠 Route for Home Page
# ===============================

@app.route('/')
def index():
    """
    When user visits the root URL ("/"), 
    render and show the 'index.html' page.
    """
    return render_template('index.html')  


# ===============================
# 🔮 Route for Prediction Page
# ===============================

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    """
    Handles both GET and POST requests for prediction.
    
    - GET: Shows the input form (home.html)
    - POST: Takes user input, preprocesses it, 
            runs prediction using ML model, and
            displays the predicted result.
    """

    # -------------------------------
    # Case 1️⃣: GET request → Show form
    # -------------------------------
    if request.method == 'GET':
        return render_template('home.html')  

    # -------------------------------
    # Case 2️⃣: POST request → Predict result
    # -------------------------------
    else:
        # Create CustomData object from form inputs
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )

        # Convert input data into a Pandas DataFrame
        pred_df = data.get_data_as_data_frame()  
        print(pred_df)  # Debugging purpose: print input data

        # Initialize PredictPipeline object
        predict_pipeline = PredictPipeline()  

        # Run the ML model prediction
        results = predict_pipeline.predict(pred_df)  

        # Return the result to the home.html template
        return render_template('home.html', results=results[0])  


# ===============================
# ⚙️ Run Flask App (Entry Point)
# ===============================

if __name__ == "__main__":
    
    app.run(host="0.0.0.0")  
