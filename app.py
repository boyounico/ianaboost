
import streamlit as st

# Gestion de la mémoire temporaire pour effacer les champs après validation
if "_to_clear" not in st.session_state:
    st.session_state._to_clear = []

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
            "couleur": "#2f7d32",
            "saveurs": {
                "Citron Bio": 240,
                "Fruits Rouges": 80,
                "Mangue": 30
            }
        },
        "HIGHWATT30": {
            "couleur": "#1a4f8b",
            "saveurs": {
                "Menthe": 160,
                "Fraise": 40
            }
        },
        "HIGHWATT25 BCAA": {
            "couleur": "#8a3c00",
            "saveurs": {
                "Cola": 64
            }
        }
    }

recette_hw45 = {
    "Maltodextrine": 27,
    "Fructose": 18,
    "Eau": 12,
    "Sodium": 0.5,
    "Acide Citrique": 0.2,
    "Arôme Citron": 1
}

def gels_possibles(stock, recette):
    mini = float("inf")
    for ingr, qt in recette.items():
        dispo = stock.get(ingr, 0) * 1000
        nb = dispo // qt
        if nb < mini:
            mini = nb
    return int(mini)

# Réinitialisation des champs marqués
for key in st.session_state._to_clear:
    if key in st.session_state:
        st.session_state[key] = ""
st.session_state._to_clear.clear()

# === Interface ===
st.set_page_config(layout="wide")
st.title("IANABOOST MANAGER")

onglets = ["STOCK", "PRODUCTION", "GAMMES", "HISTORIQUE", "B2B"]
cols = st.columns(len(onglets))
for i, ong in enumerate(onglets):
    if cols[i].button(ong):
        st.session_state.onglet = ong
if "onglet" not in st.session_state:
    st.session_state.onglet = "STOCK"
onglet_actif = st.session_state.onglet

if onglet_actif == "STOCK":
    sous = st.radio("Sous-onglet STOCK", ["Matière première", "Produit fini"], horizontal=True)

    if sous == "Matière première":
        st.subheader("STOCK MATIÈRES PREMIÈRES")

        gels = gels_possibles(st.session_state.stock_matieres, recette_hw45)
        st.success(f"Le stock actuel permet de produire environ **{gels} gels HIGHWATT45**.")

        with st.form("réappro"):
            champs_add = {}
            champs_ajust = {}
            for ingr, val in st.session_state.stock_matieres.items():
                prec = st.session_state.stock_prec[ingr]
                col1, col2, col3 = st.columns([2, 1.5, 1.5])
                with col1:
                    st.markdown(f"**{ingr}** : {val:.3f} ("
                                f"<span style='color:orange'>dernier : {prec:.3f}</span>)",
                                unsafe_allow_html=True)
                with col2:
                    champs_add[ingr] = st.text_input(f"Ajouter {ingr}", key=f"add_{ingr}")
                with col3:
                    champs_ajust[ingr] = st.text_input(f"Ajuster {ingr}", key=f"ajust_{ingr}")

            if st.form_submit_button("Valider"):
                for ingr in st.session_state.stock_matieres:
                    ajout = champs_add[ingr]
                    ajust = champs_ajust[ingr]
                    try:
                        if ajout:
                            v = float(ajout.replace(",", "."))
                            if v > 0:
                                st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                                st.session_state.stock_matieres[ingr] += v
                                st.session_state.historique.append(f"APPRO {ingr} +{v:.3f}")
                        st.session_state._to_clear.append(f"add_{ingr}")
                    except:
                        pass
                    try:
                        if ajust:
                            v = float(ajust.replace(",", "."))
                            if v > 0:
                                st.session_state.stock_prec[ingr] = st.session_state.stock_matieres[ingr]
                                st.session_state.stock_matieres[ingr] = v
                                st.session_state.historique.append(f"AJUST {ingr} -> {v:.3f}")
                        st.session_state._to_clear.append(f"ajust_{ingr}")
                    except:
                        pass
                st.success("Mise à jour effectuée.")
                st.experimental_rerun()

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
            bloc_html = lambda txt: f"<div style='background-color:{infos['couleur']}; color:white; padding:10px; border-radius:5px'><b>{txt}</b></div>"
            with c1:
                st.markdown(bloc_html(gamme), unsafe_allow_html=True)
            with c2:
                st.markdown(bloc_html(f"Unités : {total}"), unsafe_allow_html=True)
            with c3:
                st.markdown(bloc_html(f"Boîtes : {boites}"), unsafe_allow_html=True)
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
