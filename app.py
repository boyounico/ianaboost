import streamlit as st

# === Initialisation des données ===
if "stock" not in st.session_state:
    st.session_state.stock = {
        "Maltodextrine": 100.000,
        "Fructose": 80.000,
        "Eau": 50.000,
        "Sodium": 1.000,
        "Acide Citrique": 0.500,
        "Arôme Citron": 5.000
    }
    st.session_state.unites = {
        "Maltodextrine": "kg",
        "Fructose": "kg",
        "Eau": "L",
        "Sodium": "kg",
        "Acide Citrique": "kg",
        "Arôme Citron": "L"
    }
    st.session_state.prec = st.session_state.stock.copy()
    st.session_state.historique = []

# === Barre d’onglets horizontale ===
onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
colong = st.columns(len(onglets))
onglet_actif = None
for i, ong in enumerate(onglets):
    if colong[i].button(ong):
        st.session_state.onglet_actif = ong
if "onglet_actif" not in st.session_state:
    st.session_state.onglet_actif = "STOCK"
onglet_actif = st.session_state.onglet_actif

st.markdown(f"## IANABOOST MANAGER — {onglet_actif}")

# === GESTION STOCK ===
if onglet_actif == "STOCK":
    sous_onglet = st.radio("Sous-onglet :", ["Matière première", "Produit fini"], horizontal=True)

    if sous_onglet == "Matière première":
        st.header("STOCK MATIÈRES PREMIÈRES")

        for ingr, val in st.session_state.stock.items():
            col1, col2 = st.columns([3, 2])
            unite = st.session_state.unites[ingr]
            prec = st.session_state.prec[ingr]

            with col1:
                st.markdown(f"**{ingr}**")
                st.markdown(
                    f"{val:,.3f} {unite} "
                    f"<span style='color:orange'>(ancien : {prec:,.3f} {unite})</span>",
                    unsafe_allow_html=True
                )

            with col2:
                ajout = st.text_input(f"Ajout {ingr}", "", key=f"add_{ingr}")
                ajust = st.text_input(f"Ajustement {ingr}", "", key=f"ajust_{ingr}")

                if st.button(f"Valider {ingr}", key=f"valider_{ingr}"):
                    try:
                        if ajout:
                            add = float(ajout.replace(",", "."))
                            st.session_state.prec[ingr] = st.session_state.stock[ingr]
                            st.session_state.stock[ingr] += add
                            st.success(f"Ajouté {add} {unite} à {ingr}")
                        elif ajust:
                            new = float(ajust.replace(",", "."))
                            st.session_state.prec[ingr] = st.session_state.stock[ingr]
                            st.session_state.stock[ingr] = new
                            st.success(f"Nouveau stock de {ingr} : {new} {unite}")
                        st.rerun()
                    except:
                        st.warning("Entrée invalide.")

    elif sous_onglet == "Produit fini":
        st.header("STOCK PRODUITS FINIS")
        st.info("Module à venir...")
else:
    st.info(f"Onglet {onglet_actif} en développement.")
