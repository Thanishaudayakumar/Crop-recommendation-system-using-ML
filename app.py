import os
import logging
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import numpy as np
import pandas as pd
from ml_model import CropRecommendationModel

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///crop_recommendations.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Initialize ML model
ml_model = CropRecommendationModel()

@app.route('/')
def index():
    """Main page with crop recommendation form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle crop prediction based on form data"""
    try:
        # Extract form data
        nitrogen = float(request.form.get('nitrogen', 0))
        phosphorus = float(request.form.get('phosphorus', 0))
        potassium = float(request.form.get('potassium', 0))
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        ph = float(request.form.get('ph', 0))
        rainfall = float(request.form.get('rainfall', 0))
        
        # Validate input ranges
        if not (0 <= nitrogen <= 200):
            flash('Nitrogen should be between 0 and 200', 'error')
            return redirect(url_for('index'))
        
        if not (0 <= phosphorus <= 200):
            flash('Phosphorus should be between 0 and 200', 'error')
            return redirect(url_for('index'))
            
        if not (0 <= potassium <= 200):
            flash('Potassium should be between 0 and 200', 'error')
            return redirect(url_for('index'))
            
        if not (0 <= temperature <= 50):
            flash('Temperature should be between 0°C and 50°C', 'error')
            return redirect(url_for('index'))
            
        if not (0 <= humidity <= 100):
            flash('Humidity should be between 0% and 100%', 'error')
            return redirect(url_for('index'))
            
        if not (0 <= ph <= 14):
            flash('pH should be between 0 and 14', 'error')
            return redirect(url_for('index'))
            
        if not (0 <= rainfall <= 500):
            flash('Rainfall should be between 0mm and 500mm', 'error')
            return redirect(url_for('index'))
        
        # Prepare features for prediction
        features = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
        
        # Get prediction
        prediction = ml_model.predict(features)
        confidence = ml_model.get_prediction_confidence(features)
        
        if prediction:
            flash(f'Recommended crop: {prediction} (Confidence: {confidence:.1f}%)', 'success')
            return render_template('index.html', 
                                 prediction=prediction, 
                                 confidence=confidence,
                                 features={
                                     'nitrogen': nitrogen,
                                     'phosphorus': phosphorus,
                                     'potassium': potassium,
                                     'temperature': temperature,
                                     'humidity': humidity,
                                     'ph': ph,
                                     'rainfall': rainfall
                                 })
        else:
            flash('Could not determine the best crop with the provided data. Please check your inputs.', 'error')
            return redirect(url_for('index'))
            
    except ValueError as e:
        flash('Please enter valid numeric values for all fields', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        flash('An error occurred while processing your request. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page with information about the system"""
    return render_template('about.html')

with app.app_context():
    # Import models to create tables
    import models
    db.create_all()
    
    # Initialize ML model
    try:
        ml_model.load_or_train_model()
    except Exception as e:
        logging.error(f"Failed to load ML model: {str(e)}")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
