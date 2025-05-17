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

def stock_suffisant(n_gels):
    for ingr, qt in recette_hw45.items():
        dispo = st.session_state.stock.get(ingr, 0) * 1000
        if dispo < qt * n_gels:
            return False
    return True

# === Interface ===
st.sidebar.title("IANABOOST MANAGER")
onglet = st.sidebar.radio("Menu", ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"])

# --- STOCK ---
if onglet == "STOCK":
    st.title("STOCK : Matières Premières")
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        st.markdown("### Stock actuel")
        for ingr in st.session_state.stock:
            val = st.session_state.stock[ingr]
            prec = st.session_state.stock_prec[ingr]
            unit = unités[ingr]
            st.markdown(f"**{ingr}** : {val:.3f} {unit} *(ancien : {prec:.3f} {unit})*")

    ajout = {}
    with col2:
        st.markdown("### Réapprovisionnement")
        for ingr in st.session_state.stock:
            unit = unités[ingr]
            ajout[ingr] = st.text_input(f"{ingr} (+ {unit})", key=f"ajout_{ingr}")

    if st.button("Valider le réapprovisionnement"):
        for ingr in ajout:
            try:
                qt = float(ajout[ingr].replace(",", "."))
                if qt > 0:
                    st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                    st.session_state.stock[ingr] += qt
                    st.session_state.historique.append(f"{now()} APPRO +{qt:.3f} sur {ingr}")
                    st.success(f"{qt:.3f} ajouté à {ingr}")
            except:
                pass
        st.experimental_rerun()

    with col3:
        st.markdown("### Synthèse")
        gels = calcul_gels_possibles()
        st.metric("Gels HW45 possibles", gels)
        alerts = []
        for ingr in st.session_state.stock:
            if st.session_state.stock[ingr] < seuils[ingr]:
                alerts.append(f"- {ingr} : {st.session_state.stock[ingr]:.3f} (seuil = {seuils[ingr]:.3f})")
        if alerts:
            st.error("#### ALERTES STOCK BAS\n" + "\n".join(alerts))
        else:
            st.success("Tous les stocks sont suffisants.")

# --- PRODUCTION ---
elif onglet == "PRODUCTION":
    st.title("PRODUCTION")
    st.markdown("### Gamme : HIGHWATT45")
    saveur = st.selectbox("Choisir la saveur", ["Citron Bio", "Fruits Rouges", "Menthe Glacée"])
    mode = st.radio("Entrer la quantité en :", ["Nombre de gels", "Nombre de boîtes"])
    if mode == "Nombre de gels":
        nb = st.number_input("Nombre de gels à produire", min_value=1, step=1)
        gels = nb
    else:
        nb = st.number_input("Nombre de boîtes (16 gels/boîte)", min_value=1, step=1)
        gels = nb * 16

    if st.button("Valider la production"):
        if stock_suffisant(gels):
            for ingr, qt in recette_hw45.items():
                consommation = gels * qt / 1000
                st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                st.session_state.stock[ingr] -= consommation
            st.session_state.historique.append(f"{now()} PRODUCTION {gels} gels HW45 ({saveur})")
            st.success(f"{gels} gels HW45 ({saveur}) produits.")
            st.experimental_rerun()
        else:
            st.error("Stock insuffisant pour cette production.")

# --- HISTORIQUE ---
elif onglet == "HISTORIQUE":
    st.title("Historique des Mouvements")
    for ligne in reversed(st.session_state.historique[-100:]):
        st.write(ligne)

# --- AUTRES ONGLET (placeholders) ---
else:
    st.title(f"{onglet} (en cours de développement)")
