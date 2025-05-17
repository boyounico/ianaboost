
import streamlit as st
from datetime import datetime

# === Initialisation ===
if "onglet" not in st.session_state:
    st.session_state.onglet = "STOCK"
if "sous_onglet" not in st.session_state:
    st.session_state.sous_onglet = "Matière première"
if "sous_prod" not in st.session_state:
    st.session_state.sous_prod = "Ordre de production"

if "stock_matieres" not in st.session_state:
    st.session_state.stock_matieres = {
        "Maltodextrine": 100.0,
        "Fructose": 80.0,
        "Eau": 50.0,
        "Sodium": 1.0,
        "Acide Citrique": 0.5,
        "Arôme Citron": 5.0
    }
    st.session_state.stock_prec = st.session_state.stock_matieres.copy()

if "produits_finis" not in st.session_state:
    st.session_state.produits_finis = {
        "HIGHWATT45": {"saveurs": {"Citron Bio": 240, "Fruits Rouges": 80}},
        "HIGHWATT30": {"saveurs": {"Menthe": 100}},
        "HIGHWATT25 BCAA": {"saveurs": {"Cola": 64}}
    }

if "bon_commandes" not in st.session_state:
    st.session_state.bon_commandes = []

recettes = {
    "HIGHWATT45": {
        "Maltodextrine": 0.028,
        "Fructose": 0.017,
        "Eau": 0.010,
        "Sodium": 0.001,
        "Acide Citrique": 0.0005,
        "Arôme Citron": 0.001
    }
}

st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

# === Navigation Principale ===
onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
cols = st.columns(len(onglets))
for i, name in enumerate(onglets):
    if cols[i].button(name):
        st.session_state.onglet = name

# === Onglet STOCK ===
if st.session_state.onglet == "STOCK":
    sous = st.columns(2)
    for i, name in enumerate(["Matière première", "Produit fini"]):
        if sous[i].button(name):
            st.session_state.sous_onglet = name

    if st.session_state.sous_onglet == "Matière première":
        st.subheader("STOCK MATIÈRES PREMIÈRES")
        recette = recettes["HIGHWATT45"]
        gels_possible = min([
            st.session_state.stock_matieres[ing] * 1000 // recette[ing]
            for ing in recette
        ])
        st.success(f"Gels HW45 possibles : {int(gels_possible)}")

        with st.form("form_mp"):
            for ing in st.session_state.stock_matieres:
                col1, col2, col3 = st.columns([2, 1.5, 1.5])
                val = st.session_state.stock_matieres[ing]
                old = st.session_state.stock_prec[ing]
                with col1:
                    st.markdown(f"**{ing}** : {val:.3f} <span style='color:orange'>(dernier : {old:.3f})</span>", unsafe_allow_html=True)
                with col2:
                    st.text_input(f"Ajouter {ing}", key=f"add_{ing}", value="")
                with col3:
                    st.text_input(f"Ajuster {ing}", key=f"ajust_{ing}", value="")
            if st.form_submit_button("Valider"):
                for ing in st.session_state.stock_matieres:
                    try:
                        a = float(st.session_state[f"add_{ing}"].replace(",", "."))
                        st.session_state.stock_prec[ing] = st.session_state.stock_matieres[ing]
                        st.session_state.stock_matieres[ing] += a
                        st.session_state[f"add_{ing}"] = ""
                    except: pass
                    try:
                        j = float(st.session_state[f"ajust_{ing}"].replace(",", "."))
                        st.session_state.stock_prec[ing] = st.session_state.stock_matieres[ing]
                        st.session_state.stock_matieres[ing] = j
                        st.session_state[f"ajust_{ing}"] = ""
                    except: pass
                st.rerun()

    elif st.session_state.sous_onglet == "Produit fini":
        st.subheader("STOCK PRODUITS FINIS")
        total_gels = 0
        total_boites = 0
        total_poids = 0
        couleurs = ["#009688", "#1E88E5", "#43A047", "#FB8C00"]
        for i, (gamme, data) in enumerate(st.session_state.produits_finis.items()):
            saveurs = data.get("saveurs", {})
            total = sum(saveurs.values())
            boites = total // 16
            poids = total * 60
            c1, c2, c3, c4 = st.columns(4)
            bloc = lambda txt: f"<div style='background-color:{couleurs[i % len(couleurs)]}; color:white; padding:10px; border-radius:5px'><b>{txt}</b></div>"
            with c1:
                st.markdown(bloc(gamme), unsafe_allow_html=True)
            with c2:
                st.markdown(bloc(f"{total} gels"), unsafe_allow_html=True)
            with c3:
                st.markdown(bloc(f"{boites} boîtes"), unsafe_allow_html=True)
            with c4:
                if st.button(f"Par saveur - {gamme}"):
                    st.session_state["popup"] = saveurs
            total_gels += total
            total_boites += boites
            total_poids += poids

        st.markdown("---")
        st.success(f"Total gels : {total_gels} — Total boîtes : {total_boites} — Poids total : {total_poids / 1000:.1f} kg")

        if "popup" in st.session_state:
            st.subheader("Détail par saveur")
            for s, q in st.session_state.popup.items():
                st.markdown(f"- {s} : **{q} gels**")
            if st.button("Fermer"):
                del st.session_state["popup"]

# === Onglet PRODUCTION ===
if st.session_state.onglet == "PRODUCTION":
    st.markdown("### PRODUCTION")
    sous_prod = st.columns(3)
    for i, name in enumerate(["Ordre de production", "LiveProd", "Cadence"]):
        if sous_prod[i].button(name, key=f"sous_prod_{name}"):
            st.session_state.sous_prod = name

    if st.session_state.sous_prod == "Ordre de production":
        st.subheader("Ordre de production")
        gamme = st.selectbox("Gamme", list(recettes.keys()))
        saveur = st.selectbox("Saveur", ["Citron", "Fraise", "Tropical"])

        recette = recettes[gamme]
        gels_max = min([
            st.session_state.stock_matieres[ing] * 1000 // recette[ing]
            for ing in recette
        ])
        boites_max = gels_max // 16
        st.info(f"Max possible : {gels_max} gels — {boites_max} boîtes")
        q = st.number_input("Quantité à produire (gels)", 1, gels_max)

        if st.button("Envoyer"):
            st.session_state.bon_commandes.append({
                "gamme": gamme,
                "saveur": saveur,
                "quantite": q,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Ajouté au bon de commande.")

        for cmd in st.session_state.bon_commandes:
            st.markdown(f"- {cmd['gamme']} / {cmd['saveur']} — {cmd['quantite']} gels — {cmd['date']}")

        if st.button("Produire"):
            for cmd in st.session_state.bon_commandes:
                for ing, qt in recettes[cmd["gamme"]].items():
                    st.session_state.stock_matieres[ing] -= qt * cmd["quantite"]
                st.session_state.produits_finis.setdefault(cmd["gamme"], {"saveurs": {}})
                st.session_state.produits_finis[cmd["gamme"]]["saveurs"][cmd["saveur"]] =                     st.session_state.produits_finis[cmd["gamme"]]["saveurs"].get(cmd["saveur"], 0) + cmd["quantite"]
            st.session_state.bon_commandes.clear()
            st.success("Production terminée.")

    elif st.session_state.sous_prod == "LiveProd":
        st.subheader("LiveProd (à venir)")
    elif st.session_state.sous_prod == "Cadence":
        st.subheader("Cadence (à venir)")
