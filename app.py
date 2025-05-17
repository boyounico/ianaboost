
import streamlit as st

# Initialisation du stock
if "stock" not in st.session_state:
    st.session_state.stock = {
        "Maltodextrine": 100.0,
        "Fructose": 80.0,
        "Eau": 50.0,
        "Sodium": 1.0,
        "Acide Citrique": 0.5,
        "Arôme Citron": 5.0
    }
    st.session_state.stock_prec = st.session_state.stock.copy()
    st.session_state.unites = {
        "Maltodextrine": "kg",
        "Fructose": "kg",
        "Eau": "L",
        "Sodium": "kg",
        "Acide Citrique": "kg",
        "Arôme Citron": "L"
    }

# Initialisation des produits
if "produits" not in st.session_state:
    st.session_state.produits = {
        "HIGHWATT45": {"saveur": {"Citron Bio": 240, "Fruits Rouges": 80}},
        "HIGHWATT30": {"saveurs": {"Mangue": 120}},
        "HIGHWATT25 BCAA": {"saveur": {"Cola": 60}}
    }

# Recette HW45
recette_hw45 = {
    "Maltodextrine": 28,
    "Fructose": 17,
    "Eau": 10,
    "Sodium": 0.1,
    "Acide Citrique": 0.1,
    "Arôme Citron": 0.3
}

# Sélecteur d'onglet
onglet = st.selectbox("Onglet", ["Matière première", "Produit fini"])

# === Onglet : Matière première ===
if onglet == "Matière première":
    st.header("STOCK MATIÈRES PREMIÈRES")
    gels_possibles = min(
        (st.session_state.stock[ing] * 1000) // recette_hw45[ing]
        for ing in recette_hw45
    )
    st.success(f"Nombre de gels HW45 possibles : {int(gels_possibles)}")

    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    modifications = {}

    for ingr in st.session_state.stock:
        prec = st.session_state.stock_prec[ingr]
        unit = st.session_state.unites[ingr]
        stock = st.session_state.stock[ingr]

        with col1:
            st.markdown(
                f"**{ingr}** : {stock:.3f} {unit} "
                f"<span style='color:orange'>(dernier : {prec:.3f})</span>",
                unsafe_allow_html=True
            )
        with col2:
            modifications[f"ajout_{ingr}"] = st.text_input(f"Ajouter {ingr}", key=f"ajout_{ingr}")
        with col3:
            modifications[f"ajust_{ingr}"] = st.text_input(f"Ajuster {ingr}", key=f"ajust_{ingr}")

    if st.button("Valider"):
        for ingr in st.session_state.stock:
            try:
                ajout = float(modifications[f"ajout_{ingr}"].replace(",", "."))
                if ajout > 0:
                    st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                    st.session_state.stock[ingr] += ajout
                    st.session_state[f"ajout_{ingr}"] = ""
            except:
                pass
            try:
                val = float(modifications[f"ajust_{ingr}"].replace(",", "."))
                st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                st.session_state.stock[ingr] = val
                st.session_state[f"ajust_{ingr}"] = ""
            except:
                pass
        st.success("Mise à jour effectuée.")

# === Onglet : Produit fini ===
elif onglet == "Produit fini":
    st.header("STOCK PRODUITS FINIS")
    total_gels = 0
    total_boites = 0
    total_poids = 0

    for gamme, infos in st.session_state.produits.items():
        saveurs = infos.get("saveurs") or infos.get("saveur") or {}
        sous_total = sum(saveurs.values())
        boites = sous_total // 16
        poids = sous_total * 60

        st.markdown(f"### {gamme}")
        st.markdown(f"- Gels : **{sous_total}**")
        st.markdown(f"- Boîtes : **{boites}**")
        st.markdown(f"- Poids total : **{poids / 1000:.2f} kg**")

        with st.expander("Détail par saveur"):
            for nom, val in saveurs.items():
                st.markdown(f"- {nom} : {val} gels")

        total_gels += sous_total
        total_boites += boites
        total_poids += poids

    st.divider()
    st.success(f"**TOTAL GELS : {total_gels}** — **TOTAL BOÎTES : {total_boites}** — **POIDS : {total_poids / 1000:.2f} kg**")
