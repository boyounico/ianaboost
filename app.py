
import streamlit as st

# === Données simulées ===
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

# === Structure globale ===
st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

# Onglets horizontaux (fixes)
onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
colong = st.columns(len(onglets))
onglet_actif = st.session_state.get("onglet", "STOCK")
for i, ong in enumerate(onglets):
    if colong[i].button(ong):
        st.session_state.onglet = ong
onglet_actif = st.session_state.get("onglet", "STOCK")

# Sous-onglets
if onglet_actif == "STOCK":
    sous = st.radio("Sous-onglet STOCK", ["Matière première", "Produit fini"], horizontal=True)
    if sous == "Produit fini":
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

            # Affichage ligne par gamme
            c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
            with c1:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'><b>{gamme}</b></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'>Unités : <b>{total}</b></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div style='background-color:{infos['couleur']}; padding:10px; border-radius:5px'>Boîtes : <b>{boites}</b></div>", unsafe_allow_html=True)
            with c4:
                if st.button(f"Par saveur - {gamme}"):
                    st.session_state.popup = saveurs

        st.divider()
        colt1, colt2, colt3 = st.columns(3)
        colt1.success(f"**Total gels :** {total_gels}")
        colt2.success(f"**Total boîtes :** {total_boites}")
        colt3.success(f"**Poids total :** {total_poids} g")

        if "popup" in st.session_state:
            st.subheader("Détail par saveur")
            for s, q in st.session_state.popup.items():
                st.markdown(f"- {s} : **{q} gels**")

