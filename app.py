
import streamlit as st

# Initialisation des données dans session_state
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

if "gammes" not in st.session_state:
    st.session_state.gammes = {
        "HIGHWATT45": {
            "Maltodextrine": 0.030,
            "Fructose": 0.015,
            "Eau": 0.012,
            "Sodium": 0.001,
            "Acide Citrique": 0.001,
            "Arôme Citron": 0.002
        }
    }

if "produits" not in st.session_state:
    st.session_state.produits = {
        "HIGHWATT45": {
            "Fraise": 0,
            "Citron": 0
        }
    }

st.set_page_config(page_title="IANABOOST MANAGER", layout="wide")

onglet_principal = st.selectbox("Section", ["STOCK", "PRODUCTION"])

if onglet_principal == "STOCK":
    sous_onglet = st.radio("Sous-onglet :", ["Matière première", "Produit fini"], horizontal=True)

    if sous_onglet == "Matière première":
        st.title("IANABOOST MANAGER — STOCK")
        st.header("STOCK MATIÈRES PREMIÈRES")

        # Calcul gels max pour la gamme HW45
        recette = st.session_state.gammes["HIGHWATT45"]
        max_gels_possible = int(min([
            st.session_state.stock[ingr] // qty for ingr, qty in recette.items()
        ]))

        st.markdown(f"**Nombre de gels HW45 possible :** `{max_gels_possible}`")

        col1, col2 = st.columns([1, 2])
        with col1:
            for ingr, val in st.session_state.stock.items():
                previous = st.session_state.stock_prec[ingr]
                unite = "kg" if ingr not in ["Eau", "Arôme Citron"] else "L"
                couleur = "orange"
                st.markdown(
                    f"<b>{ingr}</b> : {val:.3f} {unite} "
                    f"<span style='color:{couleur}'>(dernier : {previous:.3f})</span>",
                    unsafe_allow_html=True
                )

        with col2:
            reappro = {}
            ajust = {}
            for ingr in st.session_state.stock:
                reappro[ingr] = st.text_input(f"Ajouter {ingr}", key=f"ajout_{ingr}")
                ajust[ingr] = st.text_input(f"Ajuster {ingr}", key=f"ajust_{ingr}")

            if st.button("Valider"):
                for ingr in st.session_state.stock:
                    try:
                        r = float(reappro[ingr].replace(",", ".")) if reappro[ingr] else 0.0
                        a = float(ajust[ingr].replace(",", ".")) if ajust[ingr] else None
                        st.session_state.stock_prec[ingr] = st.session_state.stock[ingr]
                        if a is not None:
                            st.session_state.stock[ingr] = a
                        else:
                            st.session_state.stock[ingr] += r
                        st.session_state[f"ajout_{ingr}"] = ""
                        st.session_state[f"ajust_{ingr}"] = ""
                    except:
                        pass
                st.success("Mise à jour effectuée.")

    elif sous_onglet == "Produit fini":
        st.title("STOCK PRODUITS FINIS")
        for gamme, saveurs in st.session_state.produits.items():
            st.subheader(gamme)
            total = sum(saveurs.values())
            boites = total // 16
            poids = total * sum(st.session_state.gammes[gamme].values())
            st.write(f"**Total gels** : {total}")
            st.write(f"**Total boîtes** : {boites}")
            st.write(f"**Total poids** : {poids:.3f} kg")
            if st.button(f"Par saveur - {gamme}"):
                for s, q in saveurs.items():
                    st.markdown(f"- {s} : {q} gels")

elif onglet_principal == "PRODUCTION":
    onglet_prod = st.tabs(["Ordre de production", "LiveProd", "Cadence"])[0]
    with onglet_prod:
        st.subheader("Ordre de production")
        gamme = st.selectbox("Gamme", list(st.session_state.gammes.keys()))
        saveur = st.selectbox("Saveur", list(st.session_state.produits[gamme].keys()))
        recette = st.session_state.gammes[gamme]

        gels_max = int(min([st.session_state.stock[ing] // recette[ing] for ing in recette]))
        boites_max = gels_max // 16
        st.info(f"Max possible : {gels_max:,} gels — {boites_max:,} boîtes")

        q = st.number_input("Quantité à produire (gels)", min_value=1, max_value=gels_max, step=1)
        if st.button("Envoyer"):
            st.session_state.produits[gamme][saveur] += q
            for ing, qty in recette.items():
                st.session_state.stock[ing] -= q * qty
            st.success("Production enregistrée.")
