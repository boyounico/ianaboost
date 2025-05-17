
import streamlit as st

# === Données de base ===
if "stock_matieres" not in st.session_state:
    st.session_state.stock_matieres = {
        "Maltodextrine": 100.000,
        "Fructose": 80.000,
        "Eau": 50.000,
        "Sodium": 1.000,
        "Acide Citrique": 0.500,
        "Arôme Citron": 5.000
    }
    st.session_state.stock_prec = st.session_state.stock_matieres.copy()

if "produits" not in st.session_state:
    st.session_state.produits = {
        "HIGHWATT45": {
            "saveurs": {
                "Citron Bio": 240,
                "Fruits Rouges": 80,
                "Mangue": 30
            },
            "recette": {
                "Maltodextrine": 30,
                "Fructose": 15,
                "Eau": 10,
                "Sodium": 0.1,
                "Acide Citrique": 0.05,
                "Arôme Citron": 0.2
            }
        },
        "HIGHWATT30": {
            "saveurs": {
                "Menthe": 160,
                "Fraise": 40
            },
            "recette": {
                "Maltodextrine": 20,
                "Fructose": 10,
                "Eau": 8,
                "Sodium": 0.08,
                "Acide Citrique": 0.04,
                "Arôme Citron": 0.1
            }
        }
    }

# === Interface ===
st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

onglet = st.selectbox("STOCK", ["Matière première", "Produit fini"])

# === Matière première ===
if onglet == "Matière première":
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.subheader("Liste des ingrédients")
        for ingr, qty in st.session_state.stock_matieres.items():
            prec = st.session_state.stock_prec[ingr]
            st.markdown(
                f"**{ingr}** : {qty:.3f} ("
                f":orange[{prec:.3f}] ← dernier stock)"
            )

    with col2:
        st.subheader("Réapprovisionnement")
        with st.form("form_reappro"):
            champs = {}
            for ingr in st.session_state.stock_matieres:
                champs[ingr] = st.text_input(f"{ingr}", placeholder="en kg ou L", key=f"r_{ingr}")
            if st.form_submit_button("Valider réapprovisionnement"):
                for ingr, val in champs.items():
                    try:
                        val_f = float(val.replace(",", "."))
                        if val_f > 0:
                            st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                            st.session_state.stock_matieres[ingr] += val_f
                    except:
                        pass

        st.subheader("Ajuster le stock")
        with st.form("form_ajust"):
            champs_ajust = {}
            for ingr in st.session_state.stock_matieres:
                champs_ajust[ingr] = st.text_input(f"{ingr} (ajuster)", placeholder="valeur exacte", key=f"a_{ingr}")
            if st.form_submit_button("Valider ajustement"):
                for ingr, val in champs_ajust.items():
                    try:
                        val_f = float(val.replace(",", "."))
                        st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                        st.session_state.stock_matieres[ingr] = val_f
                    except:
                        pass

    with col3:
        st.subheader("À venir")
        st.success("Estimation de production possible")
        st.warning("Alertes seuils critiques")
        st.info("Accès à l’historique")

# === Produit fini ===
if onglet == "Produit fini":
    st.subheader("STOCK PRODUITS FINIS")
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
    total_gels = 0
    total_boites = 0
    total_poids = 0
    for gamme, data in st.session_state.produits.items():
        saveurs = data["saveurs"]
        recette = data["recette"]
        gels = sum(saveurs.values())
        boites = gels // 16
        poids_par_gel = sum(recette.values())
        poids_total = round(poids_par_gel * gels, 1)
        total_gels += gels
        total_boites += boites
        total_poids += poids_total

        col1.markdown(f"### {gamme}")
        col2.markdown(f"**{gels}** gels ({boites} boîtes)")
        if col3.button(f"Par saveur ({gamme})"):
            st.session_state["popup"] = saveurs

    st.divider()
    st.subheader("Totaux")
    colA, colB = st.columns(2)
    colA.success(f"Total gels : {total_gels}  
Total boîtes : {total_boites}")
    colB.info(f"Poids total (sans emballage) : {total_poids} g")

    if "popup" in st.session_state:
        st.subheader("Détail par saveur")
        st.json(st.session_state["popup"])
