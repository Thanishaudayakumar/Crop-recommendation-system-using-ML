import os
import pickle
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib

class CropRecommendationModel:
    """Machine Learning model for crop recommendation"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.minmax_scaler = None
        self.crop_dict = {
            0: "Rice", 1: "Maize", 2: "Jute", 3: "Cotton", 4: "Coconut", 
            5: "Papaya", 6: "Orange", 7: "Apple", 8: "Muskmelon", 9: "Watermelon", 
            10: "Grapes", 11: "Mango", 12: "Banana", 13: "Pomegranate", 14: "Lentil", 
            15: "Blackgram", 16: "Mungbean", 17: "Mothbeans", 18: "Pigeonpeas", 
            19: "Kidneybeans", 20: "Chickpea", 21: "Coffee"
        }
        self.feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        try:
            # Try to load existing models
            if (os.path.exists('model.pkl') and 
                os.path.exists('standscaler.pkl') and 
                os.path.exists('minmaxscaler.pkl')):
                
                self.model = pickle.load(open('model.pkl', 'rb'))
                self.scaler = pickle.load(open('standscaler.pkl', 'rb'))
                self.minmax_scaler = pickle.load(open('minmaxscaler.pkl', 'rb'))
                logging.info("Loaded existing models successfully")
            else:
                # Train new model
                logging.info("Training new model...")
                self.train_model()
                
        except Exception as e:
            logging.error(f"Error loading models: {str(e)}")
            # Train new model as fallback
            self.train_model()
    
    def train_model(self):
        """Train the crop recommendation model"""
        try:
            # Load or create sample data
            if os.path.exists('data/crop_recommendation.csv'):
                df = pd.read_csv('data/crop_recommendation.csv')
            else:
                # Create sample dataset for demonstration
                df = self.create_sample_dataset()
            
            # Prepare features and target
            X = df[self.feature_names].values
            y = df['label'].values
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale the features
            self.minmax_scaler = MinMaxScaler()
            X_train_minmax = self.minmax_scaler.fit_transform(X_train)
            X_test_minmax = self.minmax_scaler.transform(X_test)
            
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train_minmax)
            X_test_scaled = self.scaler.transform(X_test_minmax)
            
            # Train the model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate the model
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            logging.info(f"Model accuracy: {accuracy:.3f}")
            
            # Save the models
            self.save_models()
            
        except Exception as e:
            logging.error(f"Error training model: {str(e)}")
            raise
    
    def create_sample_dataset(self):
        """Create a sample dataset for demonstration purposes"""
        # This creates a sample dataset with realistic ranges for crop recommendation
        np.random.seed(42)
        n_samples = 2200  # 100 samples per crop
        
        data = []
        for crop_id, crop_name in self.crop_dict.items():
            for _ in range(100):
                # Generate realistic values based on crop requirements
                if crop_name in ['Rice', 'Coconut']:
                    # High water requirement crops
                    sample = [
                        np.random.normal(80, 20),   # N
                        np.random.normal(40, 15),   # P
                        np.random.normal(40, 15),   # K
                        np.random.normal(25, 5),    # temperature
                        np.random.normal(80, 10),   # humidity
                        np.random.normal(6.5, 1),   # ph
                        np.random.normal(200, 50)   # rainfall
                    ]
                elif crop_name in ['Cotton', 'Maize']:
                    # Moderate water requirement crops
                    sample = [
                        np.random.normal(120, 25),  # N
                        np.random.normal(60, 20),   # P
                        np.random.normal(60, 20),   # K
                        np.random.normal(30, 5),    # temperature
                        np.random.normal(65, 15),   # humidity
                        np.random.normal(7, 1),     # ph
                        np.random.normal(100, 30)   # rainfall
                    ]
                else:
                    # Default ranges for other crops
                    sample = [
                        np.random.normal(100, 30),  # N
                        np.random.normal(50, 20),   # P
                        np.random.normal(50, 20),   # K
                        np.random.normal(25, 8),    # temperature
                        np.random.normal(70, 20),   # humidity
                        np.random.normal(6.8, 1.2), # ph
                        np.random.normal(150, 60)   # rainfall
                    ]
                
                # Ensure values are within realistic ranges
                sample = [max(0, val) for val in sample]
                sample[3] = max(10, min(45, sample[3]))  # temperature
                sample[4] = max(20, min(100, sample[4])) # humidity
                sample[5] = max(4, min(9, sample[5]))    # ph
                
                data.append(sample + [crop_id])
        
        columns = self.feature_names + ['label']
        df = pd.DataFrame(data, columns=columns)
        
        # Save the dataset
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/crop_recommendation.csv', index=False)
        
        return df
    
    def save_models(self):
        """Save trained models to pickle files"""
        try:
            pickle.dump(self.model, open('model.pkl', 'wb'))
            pickle.dump(self.scaler, open('standscaler.pkl', 'wb'))
            pickle.dump(self.minmax_scaler, open('minmaxscaler.pkl', 'wb'))
            logging.info("Models saved successfully")
        except Exception as e:
            logging.error(f"Error saving models: {str(e)}")
    
    def predict(self, features):
        """Predict crop recommendation based on input features"""
        try:
            if self.model is None or self.scaler is None or self.minmax_scaler is None:
                raise ValueError("Model not loaded or trained")
            
            # Prepare features
            features_array = np.array(features).reshape(1, -1)
            
            # Scale features
            features_minmax = self.minmax_scaler.transform(features_array)
            features_scaled = self.scaler.transform(features_minmax)
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            
            # Return crop name
            return self.crop_dict.get(prediction, "Unknown")
            
        except Exception as e:
            logging.error(f"Prediction error: {str(e)}")
            return None
    
    def get_prediction_confidence(self, features):
        """Get prediction confidence/probability"""
        try:
            if self.model is None or self.scaler is None or self.minmax_scaler is None:
                return 0.0
            
            # Prepare features
            features_array = np.array(features).reshape(1, -1)
            
            # Scale features
            features_minmax = self.minmax_scaler.transform(features_array)
            features_scaled = self.scaler.transform(features_minmax)
            
            # Get prediction probabilities
            probabilities = self.model.predict_proba(features_scaled)[0]
            
            # Return max probability as confidence percentage
            return max(probabilities) * 100
            
        except Exception as e:
            logging.error(f"Confidence calculation error: {str(e)}")
            return 0.0
