import streamlit as st
from datetime import datetime
import json
import random

st.set_page_config(
    page_title="BabaESTM - L3 GLAR",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DATA L3 GLAR ESTM ---
MATIERES = {
    "Algo Avancé": {
        "emoji": "🧠", "color": "#0F2C59", "prof": "Dr. Diop", "coef": 3,
        "chapitres": ["Complexité Avancée", "Diviser pour Régner", "Programmation Dynamique", "Graphes Avancés", "NP-Complétude"],
        "resume": "Algorithmes avancés, analyse de complexité, paradigmes de résolution"
    },
    "POO Java": {
        "emoji": "☕", "color": "#D94A4A", "prof": "Mme Fall", "coef": 3,
        "chapitres": ["Classes & Objets", "Héritage & Polymorphisme", "Interfaces", "Collections", "Threads"],
        "resume": "Programmation orientée objet en Java, design patterns de base"
    },
    "Réseaux Avancés": {
        "emoji": "🌐", "color": "#1A8C5E", "prof": "M. Ndiaye", "coef": 3,
        "chapitres": ["TCP/IP Approfondi", "Routage Dynamique", "VLAN & STP", "Sécurité Réseau", "QoS"],
        "resume": "Architecture et protocoles réseaux avancés"
    },
    "Systèmes Distribués": {
        "emoji": "🔗", "color": "#7C3AED", "prof": "Dr. Sow", "coef": 2,
        "chapitres": ["Middleware", "RMI & RPC", "Tolérance aux pannes", "Consensus", "Microservices"],
        "resume": "Conception de systèmes répartis"
    },
    "BD Avancées": {
        "emoji": "🗄️", "color": "#EA580C", "prof": "Mme Bâ", "coef": 3,
        "chapitres": ["Optimisation SQL", "Transactions", "NoSQL", "Indexation", "Data Warehouse"],
        "resume": "Bases de données avancées et optimisation"
    },
    "Génie Logiciel": {
        "emoji": "⚙️", "color": "#0891B2", "prof": "M. Kane", "coef": 2,
        "chapitres": ["UML Avancé", "Agile & Scrum", "Tests", "CI/CD", "Design Patterns"],
        "resume": "Méthodes et outils du génie logiciel"
    },
    "Sécurité": {
        "emoji": "🔒", "color": "#DC2626", "prof": "Dr. Sy", "coef": 2,
        "chapitres": ["Cryptographie", "Sécurité Web", "Pentest", "Firewall", "RGPD"],
        "resume": "Sécurité informatique et cryptographie"
    },
    "Anglais Tech": {
        "emoji": "🇬🇧", "color": "#475569", "prof": "Ms Johnson", "coef": 1,
        "chapitres": ["Technical Writing", "Presentations", "Reading Papers", "Vocab IT"],
        "resume": "Anglais technique pour l'informatique"
    }
}

# Quiz base
QUIZ = {
    "Algo Avancé": [
        {"q": "Complexité du tri fusion ?", "options": ["O(n)", "O(n log n)", "O(n²)", "O(log n)"], "a": 1, "exp": "Tri fusion divise en 2 à chaque fois → n log n"},
        {"q": "Programmation dynamique sert à ?", "options": ["Trier", "Éviter recalculs", "Compresser", "Chiffrer"], "a": 1, "exp": "On mémorise les sous-problèmes"},
        {"q": "Problème NP-Complet = ?", "options": ["P=NP", "Vérifiable en poly", "Impossible", "Toujours O(n)"], "a": 1, "exp": "Solution vérifiable en temps polynomial"},
    ],
    "POO Java": [
        {"q": "Mot-clé héritage Java ?", "options": ["inherits", "extends", "implements", "herit"], "a": 1, "exp": "extends pour classe, implements pour interface"},
        {"q": "Polymorphisme = ?", "options": ["Même nom, comportement différent", "Même classe", "Pas d'héritage", "Classe finale"], "a": 0, "exp": "Override de méthodes"},
    ],
    "Réseaux Avancés": [
        {"q": "Port HTTPS ?", "options": ["80", "443", "22", "3306"], "a": 1, "exp": "443 = HTTPS, 80 = HTTP"},
    ],
    "BD Avancées": [
        {"q": "ACID = ?", "options": ["Type NoSQL", "Propriétés transaction", "Index", "Vue"], "a": 1, "exp": "Atomicity Consistency Isolation Durability"},
    ]
}

FLASHCARDS = {
    "Algo Avancé": [
        {"front": "Diviser pour régner - 3 étapes", "back": "1. Diviser problème 2. Régner (résoudre) 3. Combiner résultats. Ex: MergeSort"},
        {"front": "Différence glouton vs DP", "back": "Glouton: choix local optimal. DP: optimal global avec mémorisation"},
    ],
    "POO Java": [
        {"front": "4 piliers POO", "back": "Abstraction, Encapsulation, Héritage, Polymorphisme"},
        {"front": "Interface vs Classe abstraite", "back": "Interface: 100% abstrait. Classe abstraite: peut avoir code + état"},
    ]
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
        st.image("Babacar_Mbow.jpg", width=180)
    with col_text:
        st.markdown("""
        <div style="padding-top:10px">
        <h1 style="margin-bottom:0">BabaESTM <span style="color:#0F2C59">L3 GLAR</span></h1>
        <h3 style="margin-top:5px; color:#475569; font-weight:400">Plateforme de révision créée par <b>Babacar Mbow</b></h3>
        <p style="color:#64748B">ESTM Dakar - Génie Logiciel & Administration Réseaux<br>
        🎯 Objectif: Valider L3 avec mention • 8 matières • Quiz • Flashcards • Prof IA</p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Matières", "8", "L3 GLAR")
        c2.metric("XP Total", f"{sum(v['xp'] for v in st.session_state.progress.values())} XP")
        c3.metric("Progression", f"{sum(len(v['chapitres']) for v in st.session_state.progress.values())} chapitres")

st.divider()

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn.fbsbx.com/v/t65.102178-21/844757195_1044402238696383_2591989364697809072_n.jpg/babaestm_logo_visible.png?_nc_ht=cdn.fbsbx.com&oh=00_AQNsPSYPDCN3e5tf6l3PzUNrs3NzEdmWyE2qG1ZlE_tvdQ&oe=6AF61450&_nc_sid=4ee932", width=200) if False else st.markdown("## 🎓 BabaESTM")
    st.markdown("### Babacar Mbow - L3 GLAR ESTM")
    st.caption(f"Dakar • {datetime.now().strftime('%d %b %Y')}")
    st.divider()
    
    all_matieres = {**MATIERES, **st.session_state.custom_matieres}
    
    matiere_selected = st.selectbox("📚 Matière", list(all_matieres.keys()))
    
    page = st.radio("Mode", ["📖 Réviser", "🧠 Quiz", "🃏 Flashcards", "📊 Progression", "⚙️ Gérer matières"], label_visibility="collapsed")
    
    st.divider()
    total_xp = sum(v["xp"] for v in st.session_state.progress.values())
    st.metric("XP Total", f"{total_xp} XP")
    
    if st.button("🔄 Reset progression"):
        st.session_state.progress = {m: {"xp": 0, "chapitres": [], "quiz_score": 0} for m in MATIERES}
        st.rerun()

# --- MAIN ---
m_data = all_matieres[matiere_selected]
st.session_state.progress.setdefault(matiere_selected, {"xp":0, "chapitres":[], "quiz_score":0})

# Header matière
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown(f"<div style='background:{m_data['color']}; width:80px; height:80px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:40px'>{m_data['emoji']}</div>", unsafe_allow_html=True)
with col2:
    st.title(f"{matiere_selected}")
    st.caption(f"{m_data['resume']} • Prof: {m_data.get('prof','')} • Coef {m_data.get('coef',1)}")

st.divider()

if page == "📖 Réviser":
    tab1, tab2, tab3 = st.tabs(["📚 Chapitres", "📝 Notes & Résumé", "🤖 Prof BabaESTM"])
    
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
                    
                    # Contenu pédagogique généré
                    st.markdown(f"**Objectif:** Maîtriser {chap.lower()}")
                    st.info(f"💡 **Astuce révision:** Explique {chap} à voix haute comme si tu enseignais. Si tu bloques, c'est le point à revoir.")
                    if st.button(f"Générer fiche {chap}", key=f"fiche_{i}"):
                        st.success(f"Fiche {chap} : Points clés à mémoriser → Définitions, exemples, pièges examen")
    
    with tab2:
        st.subheader("Tes notes personnelles")
        note_key = f"note_{matiere_selected}"
        notes = st.text_area("Ajoute ton résumé, formules, schémas (en texte)", height=200, key=note_key, placeholder="Ex: En POO Java, extends = ...")
        if st.button("💾 Sauvegarder notes"):
            st.toast("Notes sauvegardées localement (session)")
        
        st.divider()
        st.subheader("Méthode d'apprentissage active")
        st.markdown("""
        1. **Lecture** 15 min → 2. **Fiche** de mémoire → 3. **Quiz** → 4. **Enseigne** à un ami
        """)
    
    with tab3:
        st.subheader("🤖 Prof BabaESTM - Pose ta question")
        st.caption("IA connectée à tes chapitres")
        q = st.text_input("Ta question sur " + matiere_selected, placeholder="Ex: Explique-moi la programmation dynamique avec exemple")
        if q:
            # Simulation RAG pédagogique
            st.markdown(f"""
            **Réponse Prof BabaESTM sur {matiere_selected}:**

            Très bonne question Babacar !

            **{matiere_selected} - {m_data['chapitres'][0]}:**

            > {q} → Voici l'explication clé :

            - **Définition simple:** C'est comme [analogie Dakar/ESTM]
            - **Exemple concret:** Imagine tu dois...
            - **Piège examen:** 70% se trompent sur...
            - **À retenir:** Formule / mot-clé = ...

            Veux-tu que je te fasse un quiz de 3 questions là-dessus ?
            """)
            if st.button("Oui, lance le quiz"):
                st.session_state.current_quiz = matiere_selected
                st.rerun()

elif page == "🧠 Quiz":
    st.subheader(f"Quiz - {matiere_selected}")
    
    questions = QUIZ.get(matiere_selected, [])
    if not questions:
        st.warning("Pas encore de quiz pour cette matière. Ajoute tes questions dans Gérer matières.")
        # Générateur rapide
        with st.expander("Créer question rapide"):
            nq = st.text_input("Question")
            o1,o2,o3,o4 = st.columns(4)
            opts = [o1.text_input("A"), o2.text_input("B"), o3.text_input("C"), o4.text_input("D")]
            correct = st.selectbox("Bonne réponse", [0,1,2,3])
            exp = st.text_input("Explication")
            if st.button("Ajouter"):
                QUIZ.setdefault(matiere_selected, []).append({"q": nq, "options": opts, "a": correct, "exp": exp})
                st.success("Ajoutée !")
    else:
        if "quiz_idx" not in st.session_state:
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
        
        if st.session_state.quiz_idx < len(questions):
            qq = questions[st.session_state.quiz_idx]
            st.progress((st.session_state.quiz_idx)/len(questions))
            st.markdown(f"**Question {st.session_state.quiz_idx+1}/{len(questions)}**")
            st.markdown(f"### {qq['q']}")
            
            choice = st.radio("Choisis:", qq["options"], index=None, key=f"q_{st.session_state.quiz_idx}")
            if st.button("Valider"):
                if qq["options"].index(choice) == qq["a"] if choice else False:
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
            st.session_state.progress[matiere_selected]["quiz_score"] = st.session_state.quiz_score
            if st.button("Recommencer"):
                st.session_state.quiz_idx = 0
                st.session_state.quiz_score = 0
                st.rerun()

elif page == "🃏 Flashcards":
    st.subheader(f"Flashcards - {matiere_selected}")
    cards = FLASHCARDS.get(matiere_selected, [])
    if not cards:
        st.info("Pas de flashcards. Crée-en dans Gérer matières.")
    else:
        if "card_idx" not in st.session_state:
            st.session_state.card_idx = 0
            st.session_state.show_back = False
        
        card = cards[st.session_state.card_idx % len(cards)]
        
        with st.container(border=True):
            if not st.session_state.show_back:
                st.markdown(f"### ❓ {card['front']}")
                if st.button("Voir réponse"):
                    st.session_state.show_back = True
                    st.rerun()
            else:
                st.markdown(f"### ✅ {card['back']}")
                col1, col2 = st.columns(2)
                if col1.button("😵 Pas su"):
                    st.session_state.card_idx += 1
                    st.session_state.show_back = False
                    st.rerun()
                if col2.button("😎 Su"):
                    st.session_state.progress[matiere_selected]["xp"] += 10
                    st.session_state.card_idx += 1
                    st.session_state.show_back = False
                    st.rerun()

elif page == "📊 Progression":
    st.subheader("Ta progression L3 GLAR")
    
    cols = st.columns(4)
    for i, (m, d) in enumerate(all_matieres.items()):
        p = st.session_state.progress.get(m, {"xp":0, "chapitres":[], "quiz_score":0})
        pct = int(len(p["chapitres"])/len(d["chapitres"])*100) if d["chapitres"] else 0
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"{d['emoji']} **{m}**")
                st.progress(pct)
                st.caption(f"{pct}% • {p['xp']} XP")
    
    st.divider()
    st.bar_chart({m: v["xp"] for m, v in st.session_state.progress.items()})

else: # Gérer matières
    st.subheader("Gérer tes matières L3")
    
    tab_a, tab_b = st.tabs(["➕ Ajouter", "🗑️ Supprimer"])
    with tab_a:
        with st.form("add_matiere"):
            nom = st.text_input("Nom matière*")
            emoji = st.text_input("Emoji", value="📘")
            color = st.color_picker("Couleur", value="#0F2C59")
            prof = st.text_input("Prof")
            coef = st.number_input("Coef", 1, 6, 2)
            chapitres_str = st.text_area("Chapitres (un par ligne)", placeholder="Chapitre 1\nChapitre 2")
            if st.form_submit_button("Créer matière"):
                if nom:
                    chaps = [c.strip() for c in chapitres_str.split("\n") if c.strip()]
                    st.session_state.custom_matieres[nom] = {
                        "emoji": emoji, "color": color, "prof": prof, "coef": coef,
                        "chapitres": chaps if chaps else ["Chapitre 1"],
                        "resume": "Matière personnalisée"
                    }
                    st.session_state.progress[nom] = {"xp":0, "chapitres":[], "quiz_score":0}
                    st.success(f"{nom} ajoutée !")
                    st.rerun()
                else:
                    st.error("Nom requis")
    
    with tab_b:
        to_del = st.selectbox("Matière à supprimer", list(st.session_state.custom_matieres.keys()) if st.session_state.custom_matieres else ["Aucune matière perso"])
        if st.button("Supprimer définitivement"):
            if to_del in st.session_state.custom_matieres:
                del st.session_state.custom_matieres[to_del]
                del st.session_state.progress[to_del]
                st.success("Supprimée")
                st.rerun()

# Footer
st.divider()
st.caption("BabaESTM L3 GLAR • ESTM Dakar • Propulsé par Babacar Mbow • Prêt pour Streamlit Cloud")
