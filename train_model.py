import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

df = pd.read_csv("credit_dataset.csv")

# X = les features (colonnes d'entree)
# y = la cible (ce qu'on veut predire)
X = df.drop(columns=["decision"])
y = df["decision"]

# 80% pour entrainer, 20% pour tester
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=42
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)

# Colonnes numeriques -> on normalise (meme echelle)
colonnes_num = [
	"age",
	"revenu_mensuel",
	"montant_credit_demande",
	"duree_remboursement_mois",
	"nb_credits_anterieurs",
]

# Colonnes categorielles -> on encode en 0/1
colonnes_cat = ["situation_familiale", "type_emploi"]

preprocesseur = ColumnTransformer(
	transformers=[
		("num", StandardScaler(), colonnes_num),
		("cat", OneHotEncoder(handle_unknown="ignore"), colonnes_cat),
	]
)

pipeline = Pipeline(
	steps=[
		("preprocesseur", preprocesseur),
		("modele", RandomForestClassifier(n_estimators=100, random_state=42)),
	]
)

# Entrainement (une seule ligne !)
pipeline.fit(X_train, y_train)

# Prediction sur les donnees de test
y_pred = pipeline.predict(X_test)

# Affichage des resultats
print(f"Accuracy : {accuracy_score(y_test, y_pred):.2%}")
print(classification_report(y_test, y_pred, target_names=["Refuse", "Accorde"]))

with open("model.pkl", "wb") as f:
	pickle.dump(pipeline, f)

print("Modele sauvegarde dans model.pkl")
