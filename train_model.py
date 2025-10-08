import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import random

# -----------------------------
# SIMULATE QUIZ DATA
# -----------------------------
num_questions = 20  # your actual quiz length
num_samples = 200   # number of simulated quiz attempts

data = []
for _ in range(num_samples):
    score = random.randint(0, num_questions)  # 0 to 20 correct
    time_per_question = random.randint(5, 15)  # seconds
    difficulty = random.randint(0, 2)  # 0=easy,1=medium,2=hard

    # Define recommendation based on raw score
    if score <= num_questions * 0.3:      # 0–30% → review
        label = "review"
    elif score <= num_questions * 0.7:    # 31–70% → practice
        label = "practice"
    else:                                 # 71–100% → advance
        label = "advance"

    data.append([score, time_per_question, difficulty, label])

df = pd.DataFrame(data, columns=["score", "time", "difficulty", "label"])

# -----------------------------
# TRAIN THE MODEL
# -----------------------------
X = df[["score", "time", "difficulty"]]
y = df["label"]

model = LogisticRegression(multi_class='multinomial', max_iter=500)
model.fit(X, y)

# -----------------------------
# SAVE MODEL AND LABELS
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(["review", "practice", "advance"], "labels.pkl")

print("✅ AI model trained for 20-question quiz!")
