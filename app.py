
import streamlit as st

# Initialisation de l'état de session
if "stock" not in st.session_state:
    st.session_state.stock = {
        "Maltodextrine": 100.000,
        "Fructose": 80.000,
        "Eau": 50.000,
        "Sodium": 1.000,
        "Acide Citrique": 0.500,
        "Arôme Citron": 5.000
    }
if "dernier_stock" not in st.session_state:
    st.session_state.dernier_stock = st.session_state.stock.copy()

# Fonction utilitaire
def format_val(v):
    return f"{v:.3f}".replace(".", ",")

# Interface
st.set_page_config(page_title="IANABOOST MANAGER", layout="wide")
st.title("IANABOOST MANAGER — STOCK")

# Sélecteur d’onglet principal
onglet = st.selectbox("STOCK", ["Matière première", "Produit fini"])

# Onglet : Matière première
if onglet == "Matière première":
    st.header("STOCK MATIÈRES PREMIÈRES")

    # Calcul du nombre de gels HW45 possibles
    recette_hw45 = {
        "Maltodextrine": 0.030,
        "Fructose": 0.015,
        "Eau": 0.010,
        "Sodium": 0.001,
        "Acide Citrique": 0.001,
        "Arôme Citron": 0.003
    }
    gels_possibles = min(st.session_state.stock[ing] // recette_hw45[ing] for ing in recette_hw45)
    st.success(f"Nombre de gels HW45 possibles : {int(gels_possibles)}")

    # Colonnes pour interface
    col1, col2, col3 = st.columns([2, 1.5, 1.5])

    approvisionnement = {}
    ajustement = {}

    for ingr in st.session_state.stock:
        unite = "kg" if ingr not in ["Eau", "Arôme Citron"] else "L"
        stock_actuel = st.session_state.stock[ingr]
        stock_prec = st.session_state.dernier_stock[ingr]

        # Affichage gauche
        with col1:
            st.markdown(f"**{ingr}** : {format_val(stock_actuel)} {unite}  "
                        f"<span style='color:orange'>(dernier : {format_val(stock_prec)})</span>",
                        unsafe_allow_html=True)

        # Champs de réapprovisionnement
        with col2:
            val = st.text_input(f"Ajouter {ingr}", key=f"ajout_{ingr}")
            approvisionnement[ingr] = val

        # Champs d’ajustement
        with col3:
            val2 = st.text_input(f"Ajuster {ingr}", key=f"ajust_{ingr}")
            ajustement[ingr] = val2

    if st.button("Valider"):
        for ingr in st.session_state.stock:
            try:
                ajout = float(approvisionnement[ingr].replace(",", "."))
                if ajout > 0:
                    st.session_state.dernier_stock[ingr] = st.session_state.stock[ingr]
                    st.session_state.stock[ingr] += ajout
                    st.session_state[f"ajout_{ingr}"] = ""
            except:
                pass
            try:
                val = float(ajustement[ingr].replace(",", "."))
                st.session_state.dernier_stock[ingr] = st.session_state.stock[ingr]
                st.session_state.stock[ingr] = val
                st.session_state[f"ajust_{ingr}"] = ""
            except:
                pass
        st.success("Mise à jour effectuée.")

# Onglet : Produit fini
elif onglet == "Produit fini":
    st.header("STOCK PRODUITS FINIS")

    # Simuler une structure valide pour éviter l'erreur précédente
    if "produits" not in st.session_state:
        st.session_state.produits = {
            "HIGHWATT45": {
                "saveurs": {
                    "Citron Bio": 240,
                    "Fruits Rouges": 80
                }
            },
            "HIGHWATT30": {
                "saveurs": {
                    "Mangue": 120
                }
            }
        }

    for gamme, infos in st.session_state.produits.items():
        saveurs = infos.get("saveurs", {})
        total = sum(saveurs.values())
        st.markdown(f"### {gamme} — Total gels : **{total}**")
        with st.expander("Voir par saveur"):
            for nom, val in saveurs.items():
                st.markdown(f"- {nom} : **{val}** gels")
