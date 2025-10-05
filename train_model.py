import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load data
data = pd.read_csv("training_data.csv")

# Convert text features to numeric codes
data['difficulty'] = data['difficulty'].astype('category').cat.codes
data['next_step'] = data['next_step'].astype('category')

# Features (inputs) and labels (outputs)
X = data[['score', 'time_per_question', 'difficulty']]
y = data['next_step'].cat.codes

# Train a small decision tree
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model and category mappings
joblib.dump(model, "model.pkl")
joblib.dump(data['next_step'].cat.categories, "labels.pkl")

print("✅ Model trained and saved!")
