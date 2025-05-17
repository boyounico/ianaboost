
import streamlit as st

# === Données initiales ===
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
    st.session_state.historique = []

if "produits_finis" not in st.session_state:
    st.session_state.produits_finis = {
        "HIGHWATT45": {
            "couleur": "#d0f0c0",
            "saveurs": {
                "Citron Bio": 240,
                "Fruits Rouges": 80,
                "Mangue": 30
            }
        },
        "HIGHWATT30": {
            "couleur": "#c0e0ff",
            "saveurs": {
                "Menthe": 160,
                "Fraise": 40
            }
        },
        "HIGHWATT25 BCAA": {
            "couleur": "#ffe0c0",
            "saveurs": {
                "Cola": 64
            }
        }
    }

# === Interface ===
st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

# Onglets horizontaux (boutons)
onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
cols = st.columns(len(onglets))
for i, ong in enumerate(onglets):
    if cols[i].button(ong):
        st.session_state.onglet = ong
if "onglet" not in st.session_state:
    st.session_state.onglet = "STOCK"
onglet_actif = st.session_state.onglet

# === SOUS-ONGLETS STOCK ===
if onglet_actif == "STOCK":
    sous = st.radio("Sous-onglet STOCK", ["Matière première", "Produit fini"], horizontal=True)

    if sous == "Matière première":
        st.subheader("STOCK MATIÈRES PREMIÈRES")
        with st.form("réappro"):
            for ingr, val in st.session_state.stock_matieres.items():
                prec = st.session_state.stock_prec[ingr]
                col1, col2, col3 = st.columns([2, 1.5, 1.5])
                with col1:
                    st.markdown(f"**{ingr}** : {val:.3f} ("
                                f"<span style='color:orange'>dernier : {prec:.3f}</span>)",
                                unsafe_allow_html=True)
                with col2:
                    st.number_input(f"Ajouter {ingr}", key=f"add_{ingr}", format="%.3f")
                with col3:
                    st.number_input(f"Ajuster {ingr}", key=f"ajust_{ingr}", format="%.3f")
            if st.form_submit_button("Valider"):
                for ingr in st.session_state.stock_matieres:
                    ajout = st.session_state.get(f"add_{ingr}", 0.0)
                    ajust = st.session_state.get(f"ajust_{ingr}", 0.0)
                    if ajout > 0:
                        st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                        st.session_state.stock_matieres[ingr] += ajout
                        st.session_state.historique.append(f"APPRO {ingr} +{ajout:.3f}")
                    if ajust > 0:
                        st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                        st.session_state.stock_matieres[ingr] = ajust
                        st.session_state.historique.append(f"AJUST {ingr} -> {ajust:.3f}")
                st.success("Mise à jour effectuée.")
                st.rerun()

    elif sous == "Produit fini":
        st.subheader("STOCK PRODUITS FINIS")
        total_gels = 0
        total_boites = 0
        total_poids = 0
        for gamme, infos in st.session_state.produits_finis.items():
            saveurs = infos["saveurs"]
            total = sum(saveurs.values())
            boites = total // 16
            poids = total * 45
            total_gels += total
            total_boites += boites
            total_poids += poids

            c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
            with c1:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'><b>{gamme}</b></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'>Unités : <b>{total}</b></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'>Boîtes : <b>{boites}</b></div>", unsafe_allow_html=True)
            with c4:
                if st.button(f"Par saveur - {gamme}"):
                    st.session_state["popup"] = saveurs

        st.divider()
        colt1, colt2, colt3 = st.columns(3)
        colt1.success(f"**Total gels :** {total_gels}")
        colt2.success(f"**Total boîtes :** {total_boites}")
        colt3.success(f"**Poids total :** {total_poids} g")

        if "popup" in st.session_state:
            st.subheader("Détail par saveur")
            for s, q in st.session_state.popup.items():
                st.markdown(f"- {s} : **{q} gels**")
