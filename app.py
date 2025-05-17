
import streamlit as st

# Initialisation session
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
    st.session_state.unites = {
        "Maltodextrine": "kg", "Fructose": "kg", "Eau": "L",
        "Sodium": "kg", "Acide Citrique": "kg", "Arôme Citron": "L"
    }

if "produits" not in st.session_state:
    st.session_state.produits = {
        "HIGHWATT45": {"Fruits Rouges": 80, "Menthe": 50},
        "HIGHWATT30": {"Cola": 48},
        "HIGHWATT25 BCAA": {"Citron Bio": 240},
        "HIGHWATT CAF100": {"Menthe Glacée": 144}
    }

# Recette HW45 pour estimation
recette_hw45 = {
    "Maltodextrine": 30, "Fructose": 15, "Eau": 10,
    "Sodium": 0.1, "Acide Citrique": 0.2, "Arôme Citron": 0.3
}

def format_val(v):
    return f"{v:.3f}".replace(".", ",")

def nombre_gels_possibles(stock, recette):
    possibles = []
    for ingr, qty in recette.items():
        stock_qty = stock.get(ingr, 0)
        possibles.append(stock_qty * 1000 // qty)
    return int(min(possibles)) if possibles else 0

# Barre d’onglets principaux
onglet = st.selectbox("STOCK", options=["Matière première", "Produit fini"])

st.markdown("## IANABOOST MANAGER — STOCK")

# === MATIÈRE PREMIÈRE ===
if onglet == "Matière première":
    st.markdown("### STOCK MATIÈRES PREMIÈRES")

    gels_possibles = nombre_gels_possibles(st.session_state.stock, recette_hw45)
    st.success(f"**Nombre de gels HW45 possibles :** {gels_possibles} unités")

    cols = st.columns(3)
    with cols[0]:
        st.markdown("**Ingrédient**")
    with cols[1]:
        st.markdown("**Réapprovisionnement (+)**")
    with cols[2]:
        st.markdown("**Ajustement (=)**")

    ajout_fields = {}
    ajust_fields = {}

    for ingr in st.session_state.stock:
        unit = st.session_state.unites[ingr]
        val = st.session_state.stock[ingr]
        old = st.session_state.stock_prec[ingr]

        cols = st.columns(3)

        with cols[0]:
            st.markdown(
                f"**{ingr}** : {format_val(val)} {unit} "
                f"<span style='color:orange'>(dernier : {format_val(old)})</span>",
                unsafe_allow_html=True
            )

        with cols[1]:
            ajout_fields[ingr] = st.text_input(f"Ajouter {ingr}", key=f"ajout_{ingr}_field")

        with cols[2]:
            ajust_fields[ingr] = st.text_input(f"Ajuster {ingr}", key=f"ajust_{ingr}_field")

    if st.button("Valider"):
        updated = False
        for ingr in st.session_state.stock:
            unit = st.session_state.unites[ingr]
            # Réapprovisionnement
            val = st.session_state.get(f"ajout_{ingr}_field", "")
            if val:
                try:
                    ajout = float(val.replace(",", "."))
                    st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                    st.session_state.stock[ingr] += ajout
                    st.session_state[f"ajout_{ingr}_field"] = ""
                    updated = True
                except:
                    pass
            # Ajustement
            val = st.session_state.get(f"ajust_{ingr}_field", "")
            if val:
                try:
                    new_val = float(val.replace(",", "."))
                    st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                    st.session_state.stock[ingr] = new_val
                    st.session_state[f"ajust_{ingr}_field"] = ""
                    updated = True
                except:
                    pass
        if updated:
            st.success("Mise à jour effectuée.")

# === PRODUIT FINI (placeholder seulement ici) ===
elif onglet == "Produit fini":
    st.markdown("### STOCK PRODUITS FINIS — à finaliser.")
