
import streamlit as st

# --- Données simulées pour démonstration ---
# Recettes : combien d'ingrédients nécessaires pour 1 gel
recettes = {
    "HIGHWATT45": {
        "Maltodextrine": 0.020,
        "Fructose": 0.025,
        "Eau": 0.010,
        "Sodium": 0.0002,
        "Acide Citrique": 0.0001,
        "Arôme Citron": 0.0003
    }
}

# Stock en kg / L
if "stock" not in st.session_state:
    st.session_state.stock = {
        "Maltodextrine": 100.0,
        "Fructose": 80.0,
        "Eau": 50.0,
        "Sodium": 1.0,
        "Acide Citrique": 0.5,
        "Arôme Citron": 5.0
    }

if "production_log" not in st.session_state:
    st.session_state.production_log = []

# --- Interface : Onglet Ordre de production ---
st.subheader("Ordre de production")

col1, col2, col3 = st.columns(3)
with col1:
    gamme = st.selectbox("Gamme", list(recettes.keys()))
with col2:
    saveur = st.selectbox("Saveur", ["Fraise", "Citron", "Menthe"])
with col3:
    st.markdown("** **")

# Calcul du max possible
def calculer_max_production(gamme):
    recette = recettes[gamme]
    mini = float('inf')
    for ingr, qt_par_gel in recette.items():
        dispo = st.session_state.stock.get(ingr, 0)
        gels_possibles = dispo / qt_par_gel if qt_par_gel > 0 else 0
        mini = min(mini, gels_possibles)
    gels_max = int(mini)
    boites_max = gels_max // 16
    return gels_max, boites_max

gels_max, boites_max = calculer_max_production(gamme)
st.info(f"Max possible : {gels_max:,} gels — {boites_max:,} boîtes")

q = st.number_input("Quantité à produire (gels)", 1, int(gels_max), value=16, step=1)
boites = q // 16

# Bon de commande temporaire
if "bon_commandes" not in st.session_state:
    st.session_state.bon_commandes = []

if st.button("Envoyer commande"):
    ligne = {
        "gamme": gamme,
        "saveur": saveur,
        "quantité": q,
        "boites": boites,
        "date": st.session_state.get("timestamp", "maintenant")
    }
    st.session_state.bon_commandes.append(ligne)

# Affichage du bon de commande
st.markdown("### Bon de commande en attente")
for i, ligne in enumerate(st.session_state.bon_commandes):
    st.markdown(f"- {ligne['quantité']} gels / {ligne['boites']} boîtes – {ligne['gamme']} - {ligne['saveur']}")

# Action PRODUIRE
if st.button("PRODUIRE"):
    recette = recettes[gamme]
    erreur_stock = False
    for ligne in st.session_state.bon_commandes:
        for ingr, qt_par_gel in recette.items():
            total = qt_par_gel * ligne["quantité"]
            if st.session_state.stock[ingr] < total:
                st.error(f"Stock insuffisant pour {ingr} ({ligne['gamme']})")
                erreur_stock = True
                break
        if erreur_stock:
            break
    if not erreur_stock:
        for ligne in st.session_state.bon_commandes:
            for ingr, qt_par_gel in recette.items():
                st.session_state.stock[ingr] -= qt_par_gel * ligne["quantité"]
            st.session_state.production_log.append(ligne)
        st.success("Production enregistrée avec succès.")
        st.session_state.bon_commandes = []

