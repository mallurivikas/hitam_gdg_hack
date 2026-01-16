# Import required libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

# 1 Load dataset (example: diabetes.csv or heart.csv)
df = pd.read_csv("C:\\Users\\vikas\\OneDrive\\Desktop\\Projects\\GDG HACK\\dataset\\hypertension_dataset.csv")   # replace with your dataset

# 2️ Check the data
print(df.head())

# 3️ Define features and target
X = df.drop('Hypertension', axis=1)  # Drop target column
y = df['Hypertension']  # Target column
X = df.drop('Hypertension', axis=1)  # Drop target column
y = df['Hypertension']  # Target column

# Encode categorical features and target
X = pd.get_dummies(X, drop_first=True)  # One-hot encode categorical features
y = y.astype('category').cat.codes  # Encode target as numerical categories

# 4️ Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5️ Initialize Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 6️ Train the model
model.fit(X_train, y_train)

# 7️ Make predictions
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

# 8️ Evaluate performance
train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print("Training Accuracy:", train_accuracy)
print("Testing Accuracy:", test_accuracy)

# Fix: Use the correct column name for target_names
print("\nClassification Report (Test Data):\n", classification_report(y_test, y_test_pred, target_names=df['Hypertension'].unique()))
print("\nConfusion Matrix (Test Data):\n", confusion_matrix(y_test, y_test_pred))

# 9️ Plot training and testing accuracy
plt.figure(figsize=(8, 5))
plt.bar(['Training Accuracy', 'Testing Accuracy'], [train_accuracy, test_accuracy], color=['blue', 'green'])
plt.ylim(0, 1)
plt.ylabel('Accuracy')
plt.title('Training vs Testing Accuracy')
plt.tight_layout()
plt.savefig('train_vs_test_accuracy.png', dpi=300, bbox_inches='tight')
print("\nGraph saved as 'train_vs_test_accuracy.png'")
plt.show()

# 10️ Optional: Check feature importance
feature_importance = pd.Series(model.feature_importances_, index=X.columns)
feature_importance.sort_values(ascending=True).plot(kind='barh', color='teal')
plt.title("Feature Importance in hypertension Prediction")
plt.show()