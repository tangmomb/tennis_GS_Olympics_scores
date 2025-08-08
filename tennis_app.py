import streamlit as st
import pandas as pd

st.title("🎾 Grand Slams / Olympics")

@st.cache_data
def load_data():
    return pd.read_csv(r"recup\atp_grand_slam_2000_2024Filtre.csv")

df = load_data()

# --- Affichage des radios en ligne ---
cols = st.columns(2)

# Année en radio horizontale
with cols[0]:
    annees = sorted(df["year"].unique())
    annee_choisie = st.radio(
        "Année",
        options=annees,
        index=0,
        horizontal=True,
        key="annee"
    )

# Tournoi en radio horizontal, filtré par année
with cols[1]:
    df_annee = df[df["year"] == annee_choisie]
    tournois = sorted(df_annee["tourney_name"].unique())
    tournoi_choisi = st.radio(
        "Tournoi",
        options=tournois,
        index=0,
        horizontal=True,
        key="tournoi"
    )

# Liste joueurs pour le filtre actuel
df_tournoi = df_annee[df_annee["tourney_name"] == tournoi_choisi]
joueurs = pd.concat([df_tournoi["winner_name"], df_tournoi["loser_name"]]).dropna().unique()
joueurs = sorted(joueurs)

# Variable session_state pour stocker le joueur sélectionné
if "joueur_choisi" not in st.session_state:
    st.session_state.joueur_choisi = None

# Sélecteur joueur avec possibilité d'effacer la sélection
joueur_choisi = st.selectbox(
    "Joueur",
    options=[""] + joueurs,
    index=0,
    key="joueur_select"
    )

if joueur_choisi == "":
    st.session_state.joueur_choisi = None
else:
    st.session_state.joueur_choisi = joueur_choisi


# Affichage des résultats seulement si joueur sélectionné
if st.session_state.joueur_choisi:
    matchs_joueur = df_tournoi[
        (df_tournoi["winner_name"] == st.session_state.joueur_choisi) |
        (df_tournoi["loser_name"] == st.session_state.joueur_choisi)
    ]

    st.subheader(f"📊 Matchs de {st.session_state.joueur_choisi} :")
    st.dataframe(matchs_joueur[[
        "year", "tourney_name", "round", "winner_name", "loser_name", "score", "surface"
    ]])

    victoires = sum(matchs_joueur["winner_name"] == st.session_state.joueur_choisi)
    defaites = sum(matchs_joueur["loser_name"] == st.session_state.joueur_choisi)

    st.write(f"✅ Victoires : {victoires}")
    st.write(f"❌ Défaites : {defaites}")
else:
    st.info("Veuillez sélectionner un joueur pour afficher les matchs.")

# Identifier le vainqueur de la finale (round == "F") du tournoi et année sélectionnés
finale = df_tournoi[df_tournoi["round"] == "F"]

if not finale.empty:
    vainqueur = finale.iloc[0]["winner_name"]
    st.write(f" 🏆 Vainqueur du tournoi : **{vainqueur}**")
else:
    st.write(" 🏆 Vainqueur du tournoi : Non déterminé")


# thanks to Jeff Sackmann
st.markdown('<span style="text-decoration:none;color:#596377">thanks to github.com/JeffSackmann</span>', unsafe_allow_html=True)
