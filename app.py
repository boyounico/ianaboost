
import streamlit as st
import datetime

st.set_page_config(page_title="IANABOOST MANAGER", layout="wide")

# === Données ===
if "stock" not in st.session_state:
    st.session_state.stock = {
        "Maltodextrine": 100.000,
        "Fructose": 80.000,
        "Eau": 50.000,
        "Sodium": 1.000,
        "Acide Citrique": 0.500,
        "Arôme Citron": 5.000
    }
    st.session_state.stock_prec = st.session_state.stock.copy()
    st.session_state.historique = []
    st.session_state.produits = {
        "HIGHWATT45": {
            "Citron": 320,
            "Fruits Rouges": 120,
            "Menthe Glacée": 64
        }
    }

unités = {
    "Maltodextrine": "kg",
    "Fructose": "kg",
    "Eau": "L",
    "Sodium": "kg",
    "Acide Citrique": "kg",
    "Arôme Citron": "L"
}

seuils = {
    "Maltodextrine": 45.0,
    "Fructose": 30.0,
    "Eau": 20.0,
    "Sodium": 0.1,
    "Acide Citrique": 0.1,
    "Arôme Citron": 0.2
}

recette_hw45 = {
    "Maltodextrine": 27,
    "Fructose": 18,
    "Arôme Citron": 1,
    "Sodium": 0.5,
    "Eau": 12,
    "Acide Citrique": 0.2
}

# === Fonctions ===
def now():
    return datetime.datetime.now().strftime("[%d/%m %H:%M]")

def calcul_gels_possibles():
    mini = float("inf")
    for ingr, qt in recette_hw45.items():
        dispo = st.session_state.stock.get(ingr, 0)
        gels = dispo * 1000 / qt
        mini = min(mini, gels)
    return int(mini)

def total_produits_finaux():
    total_gels = 0
    total_grammes = 0
    for gamme, saveurs in st.session_state.produits.items():
        for saveur, qte in saveurs.items():
            total_gels += qte
            total_grammes += qte * 45  # 45g/gel
    total_boites = total_gels // 16
    return total_gels, total_boites, total_grammes

# === Interface ===
tabs = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
selected_tab = st.selectbox("Menu", tabs, key="main_tab", label_visibility="collapsed")

sous_onglets = {
    "STOCK": ["Matière première", "Produit fini"],
    "PRODUCTION": [],
    "GAMMES": [],
    "HISTORIQUE": [],
    "B2B": []
}

col1, col2 = st.columns([6, 1])

with col1:
    st.title(f"IANABOOST MANAGER — {selected_tab}")

    sous = st.radio("Sous-onglet :", sous_onglets[selected_tab], horizontal=True) if sous_onglets[selected_tab] else None

    if selected_tab == "STOCK" and sous == "Matière première":
        st.subheader("STOCK MATIÈRES PREMIÈRES")
        colg1, colg2 = st.columns([3, 3])
        reappro = {}
        for ingr in st.session_state.stock:
            val = st.session_state.stock[ingr]
            prec = st.session_state.stock_prec[ingr]
            unit = unités[ingr]
            alert = "🔴" if val < seuils[ingr] else ""
            with colg1:
                st.markdown(f"**{ingr}** : {val:.3f} {unit} *(dernier : {prec:.3f} {unit})* {alert}")
            with colg2:
                reappro[ingr] = st.text_input(f"{ingr} (ajout)", key=f"aj_{ingr}")

        if st.button("Valider le réapprovisionnement"):
            for ingr, val in reappro.items():
                try:
                    ajout = float(val.replace(",", "."))
                    if ajout > 0:
                        st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                        st.session_state.stock[ingr] += ajout
                        st.session_state.historique.append(f"{now()} APPRO +{ajout:.3f} sur {ingr}")
                except:
                    st.warning(f"Erreur saisie : {ingr}")
            st.experimental_rerun()

        st.divider()
        gels = calcul_gels_possibles()
        st.success(f"Stock actuel permet de produire **{gels} gels HW45**")
        if any(st.session_state.stock[i] < seuils[i] for i in seuils):
            st.error("ALERTE : au moins un ingrédient est sous le seuil critique.")
        if st.button("Voir historique stock"):
            st.info("Historique :")
            for ligne in reversed(st.session_state.historique[-30:]):
                st.write(ligne)

    elif selected_tab == "STOCK" and sous == "Produit fini":
        st.subheader("STOCK PRODUITS FINIS")
        for gamme, saveurs in st.session_state.produits.items():
            with st.expander(f"Gamme : {gamme}"):
                for saveur, qte in saveurs.items():
                    boites = qte // 16
                    poids = qte * 45
                    st.markdown(f"**{saveur}** : {qte} gels – {boites} boîtes – {poids} g")

        st.divider()
        gels, boites, poids = total_produits_finaux()
        colx1, colx2, colx3 = st.columns(3)
        colx1.metric("Total gels", gels)
        colx2.metric("Total boîtes", boites)
        colx3.metric("Total poids (g)", poids)

    elif selected_tab == "HISTORIQUE":
        st.subheader("Historique complet")
        for ligne in reversed(st.session_state.historique[-100:]):
            st.write(ligne)
    else:
        st.info("Contenu à venir.")

with col2:
    st.markdown("### TESTS")
    st.button("TEST1")
    st.button("TEST2")
    st.button("TEST3")
