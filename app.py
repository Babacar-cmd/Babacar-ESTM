
import streamlit as st
from datetime import datetime
import random

st.set_page_config(
    page_title="BabaESTM - L3 GLAR",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATA L3 GLAR ESTM ---
MATIERES = {
    "Algo Avancé": {"emoji": "🧠", "color": "#0F2C59", "prof": "Dr. Diop", "coef": 3, "chapitres": ["Complexité Avancée", "Diviser pour Régner", "Prog Dynamique", "Graphes Avancés", "NP-Complétude"], "resume": "Algorithmes avancés, complexité, paradigmes"},
    "POO Java": {"emoji": "☕", "color": "#D94A4A", "prof": "Mme Fall", "coef": 3, "chapitres": ["Classes & Objets", "Héritage", "Interfaces", "Collections", "Threads"], "resume": "POO en Java"},
    "Réseaux Avancés": {"emoji": "🌐", "color": "#1A8C5E", "prof": "M. Ndiaye", "coef": 3, "chapitres": ["TCP/IP", "Routage", "VLAN & STP", "Sécurité", "QoS"], "resume": "Réseaux avancés"},
    "Systèmes Distribués": {"emoji": "🔗", "color": "#7C3AED", "prof": "Dr. Sow", "coef": 2, "chapitres": ["Middleware", "RMI & RPC", "Tolérance pannes", "Consensus"], "resume": "Systèmes répartis"},
    "BD Avancées": {"emoji": "🗄️", "color": "#EA580C", "prof": "Mme Bâ", "coef": 3, "chapitres": ["Optimisation SQL", "Transactions", "NoSQL", "Indexation"], "resume": "BD avancées"},
    "Génie Logiciel": {"emoji": "⚙️", "color": "#0891B2", "prof": "M. Kane", "coef": 2, "chapitres": ["UML Avancé", "Agile", "Tests", "CI/CD"], "resume": "Génie logiciel"},
    "Sécurité": {"emoji": "🔒", "color": "#DC2626", "prof": "Dr. Sy", "coef": 2, "chapitres": ["Crypto", "Sécurité Web", "Pentest", "Firewall"], "resume": "Sécurité info"},
    "Anglais Tech": {"emoji": "🇬🇧", "color": "#475569", "prof": "Ms Johnson", "coef": 1, "chapitres": ["Technical Writing", "Presentations", "Reading Papers"], "resume": "Anglais tech"}
}

QUIZ = {
    "Algo Avancé": [
        {"q": "Complexité du tri fusion ?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "a": 1, "exp": "Tri fusion divise en 2 → n log n"},
        {"q": "Prog dynamique sert à ?", "options": ["Trier", "Éviter recalculs", "Compresser", "Chiffrer"], "a": 1, "exp": "On mémorise sous-problèmes"},
    ],
    "POO Java": [
        {"q": "Mot-clé héritage Java ?", "options": ["inherits", "extends", "implements", "herit"], "a": 1, "exp": "extends pour classe"},
    ],
    "Réseaux Avancés": [
        {"q": "Port HTTPS ?", "options": ["80", "443", "22", "3306"], "a": 1, "exp": "443 = HTTPS"},
    ],
}

# --- SESSION STATE ---
if "progress" not in st.session_state:
    st.session_state.progress = {m: {"xp": 0, "chapitres": [], "quiz_score": 0} for m in MATIERES}
if "custom_matieres" not in st.session_state:
    st.session_state.custom_matieres = {}

# --- HERO WITH PHOTO ---
with st.container():
    col_photo, col_text = st.columns([1, 3])
    with col_photo:
        try:
            st.image("Babacar_Mbow.jpg", width=180)
        except:
            st.markdown("### 🎓")
    with col_text:
        st.markdown("""
        <div style="padding-top:10px">
        <h1 style="margin-bottom:0">BabaESTM <span style="color:#0F2C59">L3 GLAR</span></h1>
        <h3 style="margin-top:5px; color:#475569; font-weight:400">Plateforme de révision créée par <b>Babacar Mbow</b></h3>
        <p style="color:#64748B">ESTM Dakar - Génie Logiciel & Administration Réseaux<br>
        🎯 Objectif: Valider L3 avec mention • 8 matières • Quiz • Flashcards • Prof IA</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎓 BabaESTM")
    st.caption("Babacar Mbow - L3 GLAR ESTM")
    st.caption(f"Dakar • {datetime.now().strftime('%d %b %Y')}")
    st.divider()
    
    all_matieres = {**MATIERES, **st.session_state.custom_matieres}
    matiere_selected = st.selectbox("📚 Matière", list(all_matieres.keys()))
    page = st.radio("Navigation", ["📖 Réviser", "🧠 Quiz", "🃏 Flashcards", "📊 Progression", "⚙️ Gérer matières"], label_visibility="collapsed")
    
    st.divider()
    total_xp = sum(v["xp"] for v in st.session_state.progress.values())
    st.metric("XP Total", f"{total_xp} XP")
    
    if st.button("🔄 Reset progression"):
        st.session_state.progress = {m: {"xp": 0, "chapitres": [], "quiz_score": 0} for m in MATIERES}
        st.rerun()

# --- MAIN ---
m_data = all_matieres[matiere_selected]
st.session_state.progress.setdefault(matiere_selected, {"xp":0, "chapitres":[], "quiz_score":0})

col1, col2 = st.columns([1, 5])
with col1:
    st.markdown(f"<div style='background:{m_data['color']}; width:80px; height:80px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:40px'>{m_data['emoji']}</div>", unsafe_allow_html=True)
with col2:
    st.title(f"{matiere_selected}")
    st.caption(f"{m_data['resume']} • Prof: {m_data.get('prof','')} • Coef {m_data.get('coef',1)}")

st.divider()

if page == "📖 Réviser":
    tab1, tab2, tab3 = st.tabs(["📚 Chapitres", "📝 Notes", "🤖 Prof BabaESTM"])
    with tab1:
        cols = st.columns(2)
        for i, chap in enumerate(m_data["chapitres"]):
            done = chap in st.session_state.progress[matiere_selected]["chapitres"]
            with cols[i % 2]:
                with st.container(border=True):
                    c1, c2 = st.columns([3,1])
                    c1.markdown(f"**{i+1}. {chap}**")
                    if c2.checkbox("✓", value=done, key=f"chap_{matiere_selected}_{i}"):
                        if chap not in st.session_state.progress[matiere_selected]["chapitres"]:
                            st.session_state.progress[matiere_selected]["chapitres"].append(chap)
                            st.session_state.progress[matiere_selected]["xp"] += 50
                    else:
                        if chap in st.session_state.progress[matiere_selected]["chapitres"]:
                            st.session_state.progress[matiere_selected]["chapitres"].remove(chap)
                    st.info(f"💡 Astuce: Explique {chap} à voix haute")
    with tab2:
        st.text_area("Tes notes", height=200, key=f"note_{matiere_selected}", placeholder="Résumé, formules...")
        st.caption("Notes stockées en session")
    with tab3:
        q = st.text_input("Ta question", placeholder="Ex: Explique programmation dynamique")
        if q:
            st.success(f"**Prof BabaESTM sur {matiere_selected}:**\n\nExcellente question ! {q} → Voici l'essentiel : Définition simple, exemple concret ESTM, piège examen, formule clé à retenir.")

elif page == "🧠 Quiz":
    questions = QUIZ.get(matiere_selected, [])
    if not questions:
        st.warning("Pas encore de quiz. Ajoute-en dans Gérer matières.")
    else:
        if "quiz_idx" not in st.session_state:
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
        if st.session_state.quiz_idx < len(questions):
            qq = questions[st.session_state.quiz_idx]
            st.progress(st.session_state.quiz_idx/len(questions))
            st.markdown(f"### {qq['q']}")
            choice = st.radio("Choisis:", qq["options"], index=None, key=f"q_{st.session_state.quiz_idx}")
            if st.button("Valider"):
                if choice and qq["options"].index(choice) == qq["a"]:
                    st.success(f"✅ Correct ! {qq['exp']}")
                    st.session_state.quiz_score += 1
                    st.session_state.progress[matiere_selected]["xp"] += 20
                else:
                    st.error(f"❌ Faux. Réponse: {qq['options'][qq['a']]} — {qq['exp']}")
                st.session_state.quiz_idx += 1
                st.rerun()
        else:
            st.balloons()
            st.success(f"Score: {st.session_state.quiz_score}/{len(questions)}")
            if st.button("Recommencer"):
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.rerun()

elif page == "🃏 Flashcards":
    st.info("Mode flashcards à venir - ajoute tes cartes dans Gérer matières")

elif page == "📊 Progression":
    cols = st.columns(4)
    for i, (m, d) in enumerate(all_matieres.items()):
        p = st.session_state.progress.get(m, {"xp":0, "chapitres":[]})
        pct = int(len(p["chapitres"])/len(d["chapitres"])*100) if d["chapitres"] else 0
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"{d['emoji']} **{m}**")
                st.progress(pct)
                st.caption(f"{pct}% • {p['xp']} XP")
    st.bar_chart({m: v["xp"] for m, v in st.session_state.progress.items()})

else:
    st.subheader("Gérer tes matières")
    with st.form("add_matiere"):
        nom = st.text_input("Nom matière*")
        emoji = st.text_input("Emoji", value="📘")
        color = st.color_picker("Couleur", value="#0F2C59")
        chapitres_str = st.text_area("Chapitres (un par ligne)")
        if st.form_submit_button("Créer matière"):
            if nom:
                chaps = [c.strip() for c in chapitres_str.split("\n") if c.strip()]
                st.session_state.custom_matieres[nom] = {"emoji": emoji, "color": color, "prof": "", "coef": 2, "chapitres": chaps if chaps else ["Chapitre 1"], "resume": "Perso"}
                st.session_state.progress[nom] = {"xp":0, "chapitres":[], "quiz_score":0}
                st.success(f"{nom} ajoutée !")
                st.rerun()

st.divider()
st.caption("BabaESTM L3 GLAR • ESTM Dakar • Babacar Mbow • Streamlit Cloud Ready")
