🌾 Crop Recommendation System
Welcome to the Crop Recommendation System, a web app that helps farmers, students, and agriculture enthusiasts choose the best crop to grow based on soil and climate conditions. It’s powered by machine learning and designed for ease of use, whether you’re using it for learning or real-world decision-making.

🚀 What It Does
Enter values for your soil and environment — like nitrogen, pH, rainfall, and temperature — and the system predicts the most suitable crop from a list of 22 types using a trained Random Forest model.

🧩 How It Works (Simple Version)
🧑‍🌾 You fill out the form with your soil and weather info

✅ The app checks your input to make sure it’s valid

🤖 The machine learning model processes it

🌱 The best crop for your condition is shown instantly

💾 The system stores your predictions (locally)

🖥️ Tech Stack (For the Curious)
🔧 Backend (What powers it)
Python Flask: Handles the web app

scikit-learn: Powers the machine learning model

SQLite: Stores your past predictions

pandas / numpy: Helps with data prep

joblib / pickle: For saving the model

🎨 Frontend (What you see)
HTML + Bootstrap 5: Clean, responsive layout

JavaScript: For real-time input checking

Font Awesome: Icons for a nicer user experience

🗂️ Pages and Features
🌍 Home Page: A clean interface where you enter your data

📊 Prediction Result: Displays the best crop and model confidence

🕒 History: Tracks past predictions (for internal review or expansion)

⚙️ Running Locally
To run it on your own system:

Make sure all Python requirements are installed

Activate your virtual environment

Run:

bash
Copy
Edit
python main.py
Visit http://localhost:5000 in your browser

🔒 Notes
Runs locally with an SQLite database by default

Secure session and database settings can be customized in .env

Model retraining and updating supported if needed

This app is currently deployed on localhost for demo or internal use. Let us know if you’d like to deploy it to the cloud or integrate additional crop data!

