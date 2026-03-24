from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Creer l'application Flask
app = Flask(__name__)

# Charger le modele une seule fois au demarrage
# (pas a chaque requete, pour des raisons de performance)
with open("model.pkl", "rb") as f:
	modele = pickle.load(f)


@app.route("/", methods=["GET"])
def accueil():
	return jsonify(
		{
			"message": "API crédit — opérationnelle ✅",
			"routes_disponibles": {
				"POST /predire": "Soumettre une demande de crédit",
				"GET /demo": "Voir un exemple de requête",
			},
		}
	)


@app.route("/predire", methods=["POST"])
def predire():
	# Recuperer les donnees JSON envoyees
	donnees = request.get_json()

	# Verification basique
	if not donnees:
		return jsonify({"erreur": "Aucune donnée reçue"}), 400

	# Convertir en DataFrame pour Scikit-learn
	df_demande = pd.DataFrame([donnees])

	# Prediction et probabilite de confiance
	prediction = modele.predict(df_demande)[0]
	probabilites = modele.predict_proba(df_demande)[0]
	confiance = round(float(max(probabilites)) * 100, 1)

	# Construire la reponse
	decision = "ACCORDÉ" if prediction == 1 else "REFUSÉ"
	return jsonify({"decision": decision, "confiance": f"{confiance}%"}), 200


@app.route("/demo", methods=["GET"])
def demo():
	return jsonify(
		{
			"exemples": {
				"demande_accord_possible": {
					"age": 38,
					"revenu_mensuel": 18000,
					"montant_credit_demande": 40000,
					"duree_remboursement_mois": 24,
					"nb_credits_anterieurs": 0,
					"situation_familiale": "marie",
					"type_emploi": "fonctionnaire",
				},
				"demande_refus_possible": {
					"age": 24,
					"revenu_mensuel": 4000,
					"montant_credit_demande": 150000,
					"duree_remboursement_mois": 60,
					"nb_credits_anterieurs": 3,
					"situation_familiale": "celibataire",
					"type_emploi": "sans_emploi",
				},
			},
			"utilisation": "Envoyez ces objets JSON a POST /predire",
		}
	)


if __name__ == "__main__":
	app.run(debug=True)  # debug=True : affiche les erreurs en detail
