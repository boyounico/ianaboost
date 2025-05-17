
import streamlit as st
from datetime import datetime

# === Initialisation de session ===
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

# Recettes
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

# Layout
st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

# Onglets principaux
onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
cols = st.columns(len(onglets))
for i, name in enumerate(onglets):
    if cols[i].button(name):
        st.session_state.onglet = name

# --- STOCK ---
if st.session_state.onglet == "STOCK":
    st.markdown("### Sous-onglets STOCK")
    for i, name in enumerate(["Matière première", "Produit fini"]):
        if st.columns(2)[i].button(name, key=f"sous_{name}"):
            st.session_state.sous_onglet = name

    if st.session_state.sous_onglet == "Matière première":
        st.subheader("STOCK MATIÈRES PREMIÈRES")

        recette = recettes["HIGHWATT45"]
        gels_possible = min([
            st.session_state.stock_matieres[ing] * 1000 // recette[ing]
            for ing in recette
        ])
        st.success(f"Nombre de gels HW45 possibles : {int(gels_possible)}")

        with st.form("form_matiere"):
            for ing in st.session_state.stock_matieres:
                col1, col2, col3 = st.columns([2, 1.5, 1.5])
                stock = st.session_state.stock_matieres[ing]
                prec = st.session_state.stock_prec[ing]
                with col1:
                    st.markdown(f"**{ing}** : {stock:.3f} "
                                f"<span style='color:orange'>(dernier : {prec:.3f})</span>",
                                unsafe_allow_html=True)
                with col2:
                    st.text_input(f"Ajouter {ing}", key=f"add_{ing}", value="")
                with col3:
                    st.text_input(f"Ajuster {ing}", key=f"ajust_{ing}", value="")
            if st.form_submit_button("Valider"):
                for ing in st.session_state.stock_matieres:
                    a = st.session_state[f"add_{ing}"]
                    j = st.session_state[f"ajust_{ing}"]
                    try:
                        if a:
                            a = float(a.replace(",", "."))
                            st.session_state.stock_prec[ing] = st.session_state.stock_matieres[ing]
                            st.session_state.stock_matieres[ing] += a
                            st.session_state[f"add_{ing}"] = ""
                    except: pass
                    try:
                        if j:
                            j = float(j.replace(",", "."))
                            st.session_state.stock_prec[ing] = st.session_state.stock_matieres[ing]
                            st.session_state.stock_matieres[ing] = j
                            st.session_state[f"ajust_{ing}"] = ""
                    except: pass
                st.rerun()

    elif st.session_state.sous_onglet == "Produit fini":
        st.subheader("STOCK PRODUITS FINIS")
        for gamme, infos in st.session_state.produits_finis.items():
            saveurs = infos.get("saveurs") or infos.get("saveur") or {}
            total = sum(saveurs.values())
            boites = total // 16
            st.markdown(f"### {gamme} : {total} gels / {boites} boîtes")

# --- PRODUCTION ---
if st.session_state.onglet == "PRODUCTION":
    st.markdown("### Sous-onglets PRODUCTION")
    for i, name in enumerate(["Ordre de production", "LiveProd", "Cadence"]):
        if st.columns(3)[i].button(name, key=f"sous_prod_{name}"):
            st.session_state.sous_prod = name

    if st.session_state.sous_prod == "Ordre de production":
        st.subheader("ORDRE DE PRODUCTION")

        gamme = st.selectbox("Gamme à produire", list(recettes.keys()))
        saveur = st.selectbox("Saveur", ["Citron", "Fraise", "Tropical"])

        recette = recettes[gamme]
        gels_max = min([
            st.session_state.stock_matieres[ing] * 1000 // recette[ing]
            for ing in recette
        ])
        boites_max = gels_max // 16

        st.info(f"Maximum possible : {gels_max} gels — {boites_max} boîtes")
        q = st.number_input("Quantité à produire (gels)", 1, gels_max)

        if st.button("Envoyer"):
            st.session_state.bon_commandes.append({
                "gamme": gamme,
                "saveur": saveur,
                "quantite": q,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Ajouté au bon de commande.")

        st.markdown("#### Bon de commande")
        for cmd in st.session_state.bon_commandes:
            st.markdown(f"- {cmd['gamme']} / {cmd['saveur']} — {cmd['quantite']} gels — {cmd['date']}")

        if st.button("Produire"):
            for cmd in st.session_state.bon_commandes:
                r = recettes[cmd["gamme"]]
                for ing, qt in r.items():
                    st.session_state.stock_matieres[ing] -= qt * cmd["quantite"]
                key = cmd["gamme"]
                st.session_state.produits_finis.setdefault(key, {"saveurs": {}})
                st.session_state.produits_finis[key]["saveurs"][cmd["saveur"]] = (
                    st.session_state.produits_finis[key]["saveurs"].get(cmd["saveur"], 0)
                    + cmd["quantite"]
                )
            st.session_state.bon_commandes.clear()
            st.success("Production lancée.")

    elif st.session_state.sous_prod == "LiveProd":
        st.subheader("LiveProd — à venir")

    elif st.session_state.sous_prod == "Cadence":
        st.subheader("Cadence — à venir")
