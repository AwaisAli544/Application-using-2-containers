import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

# Generate synthetic data for height (in cm) and weight (in kg)
np.random.seed(0)
height = np.random.uniform(150, 200, 100)  # 100 samples between 150cm and 200cm
weight = 0.5 * height + np.random.normal(0, 10, 100)  # Linear relationship with some noise

# Convert to DataFrame
df = pd.DataFrame(data={'Height': height, 'Weight': weight})

# Split the data into training and testing sets
X = df[['Height']]  # Features (independent variable)
y = df['Weight']    # Target (dependent variable)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Create directory for model if it does not exist
os.makedirs('model', exist_ok=True)

# Save the model to a file
joblib.dump(model, 'model/model_file.pkl')
print("Model saved as model/model_file.pkl")
