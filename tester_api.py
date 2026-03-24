import requests

# Cas 1 : profil susceptible d'etre accorde

demande_1 = {
    "age": 38,
    "revenu_mensuel": 18000,
    "montant_credit_demande": 40000,
    "duree_remboursement_mois": 24,
    "nb_credits_anterieurs": 0,
    "situation_familiale": "marie",
    "type_emploi": "fonctionnaire",
}

reponse = requests.post("http://127.0.0.1:5000/predire", json=demande_1, timeout=10)
print("Demande 1 :", reponse.json())

# Cas 2 : profil susceptible d'etre refuse

demande_2 = {
    "age": 24,
    "revenu_mensuel": 4000,
    "montant_credit_demande": 150000,
    "duree_remboursement_mois": 60,
    "nb_credits_anterieurs": 3,
    "situation_familiale": "celibataire",
    "type_emploi": "sans_emploi",
}

reponse2 = requests.post("http://127.0.0.1:5000/predire", json=demande_2, timeout=10)
print("Demande 2 :", reponse2.json())
