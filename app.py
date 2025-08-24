# app.py
# -------------------------------------------------------
# A premium, animated Streamlit portfolio for a final-year
# Data Scientist. Modern UI, glassmorphism, typing effect,
# project tags & charts, resume timeline, and polished contact.
# -------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import io
import base64
from datetime import datetime
import os


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Ansh Kedia — Data Scientist Portfolio",
    page_icon="👨‍🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# Custom CSS (theme + components)
# =========================
CUSTOM_CSS = """
<style>
:root{
  --bg: #0b1020;
  --card: rgba(255,255,255,0.06);
  --card-border: rgba(255,255,255,0.12);
  --text: #E5E7EB;
  --muted: #9CA3AF;
  --brand: #34D399; /* teal-400/emerald */
  --brand-2: #60A5FA; /* blue-400 */
  --shadow: 0 20px 60px rgba(0,0,0,0.35);
}

/* Make page edge-to-edge and set gradient background */
.stApp {
  background: radial-gradient(1200px 600px at 10% -10%, rgba(52,211,153,0.2), transparent 40%),
              radial-gradient(1200px 600px at 110% 10%, rgba(96,165,250,0.14), transparent 40%),
              linear-gradient(180deg, #0b1020 0%, #0a0f1b 100%);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans";
}

.block-container {padding-top: 2rem;}

/* Headings */
h1, h2, h3 { letter-spacing: -0.02em; }
.big-title {
  font-weight: 900;
  font-size: clamp(2rem, 6vw, 3.5rem);
  line-height: 1.05;
}
.subhead { color: var(--muted); font-size: clamp(1rem, 2.2vw, 1.25rem); }

/* Glass Card */
.card {
  background: var(--card);
  border: 1px solid var(--card-border);
  border-radius: 20px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 1.2rem 1.3rem;
}

.card-hover { transition: transform .25s ease, border-color .25s ease, background .25s ease; }
.card-hover:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.22); background: rgba(255,255,255,0.08); }

/* Hero badge */
.badge {
  display: inline-flex; align-items: center; gap:.5rem;
  padding: .4rem .8rem; border-radius: 999px;
  background: rgba(52,211,153,0.15); color: #86efac; border: 1px solid rgba(52,211,153,0.35);
  font-weight: 600; font-size: .9rem;
}

/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: .6rem;
  padding: .75rem 1.05rem; border-radius: 14px;
  font-weight: 600; text-decoration: none !important;
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease, border-color .15s ease;
  border: 1px solid var(--card-border);
  box-shadow: var(--shadow);
}
.btn:active { transform: translateY(1px) scale(0.98); }
.btn-primary { background: linear-gradient(90deg, var(--brand), var(--brand-2)); color: #0a0f1b; border: none; }
.btn-ghost { background: var(--card); color: var(--text); }
.btn-ghost:hover { background: rgba(255,255,255,0.09); }

/* Divider */
.hr { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent); margin: 1.5rem 0; border: 0; }

/* Skill bar */
.skill-wrap { display:flex; align-items:center; justify-content:space-between; margin-bottom:.4rem; }
.skill-name { font-weight: 600; }
.skill-bar { width:100%; height:10px; background:rgba(255,255,255,0.08); border-radius:999px; overflow:hidden; }
.skill-bar > span { display:block; height:100%; background: linear-gradient(90deg, var(--brand), var(--brand-2)); }

/* Tags */
.tags { display:flex; gap:.5rem; flex-wrap:wrap; }
.tag {
  font-size:.8rem; padding:.35rem .6rem; border-radius:999px;
  background: rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.18);
}

/* Project grid images */
.project-cover {
  width:100%; height:220px; object-fit:cover; border-radius:14px; border:1px solid var(--card-border);
}

/* Timeline */
.timeline { position: relative; margin-left: .75rem; padding-left: 1.25rem; }
.timeline::before {
  content: ""; position:absolute; left:0; top:.25rem; bottom:0; width:2px; background: rgba(255,255,255,0.18); border-radius:2px;
}
.timeline-item { position: relative; margin-bottom:1rem; }
.timeline-item::before {
  content:""; position:absolute; left:-9px; top:6px; width:12px; height:12px; border-radius:50%;
  background: linear-gradient(90deg, var(--brand), var(--brand-2)); box-shadow: 0 0 0 4px rgba(255,255,255,0.06);
}

/* Footer */
.footer { color: var(--muted); }

/* Typing cursor */
.cursor {
  display:inline-block; width:1ch; animation: blink 1s steps(1,end) infinite;
}
@keyframes blink { 50% { opacity: 0; } }

/* Hide default Streamlit artifacts */
[data-testid="stDecoration"], footer, header { display: none !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# Typing Effect (JS injected)
# =========================
TYPING_HTML = """
<div id="typing" class="subhead"></div>
<script>
const roles = ["Data Scientist", "ML Engineer", "Computer Vision", "NLP & RAG", "Analytics & Dashboards"];
const el = window.parent.document.querySelector('#typing') || document.querySelector('#typing');
let i = 0, j = 0, deleting = false, delay = 70, pause = 900;

function loop(){
  const word = roles[i % roles.length];
  if(!deleting){
    el.innerHTML = word.substring(0,j+1) + '<span class="cursor">▮</span>';
    j++;
    if(j === word.length){ deleting = true; setTimeout(loop, pause); return; }
  } else {
    el.innerHTML = word.substring(0,j-1) + '<span class="cursor">▮</span>';
    j--;
    if(j === 0){ deleting = false; i++; }
  }
  setTimeout(loop, deleting ? delay/2 : delay);
}
setTimeout(loop, 400);
</script>
"""

# =========================
# Header / Hero
# =========================
import base64

def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64_image("2.jpg")

colH1, colH2 = st.columns([1.2, 1], gap="large")
with colH1:
    st.markdown('<span class="badge">👨‍🔬 Final-Year • Data Science</span>', unsafe_allow_html=True)
    st.markdown('<div class="big-title">Hi, I\'m <span style="background:linear-gradient(90deg,var(--brand),var(--brand-2)); -webkit-background-clip:text; background-clip:text; color:transparent;">Ansh Kedia</span></div>', unsafe_allow_html=True)
    st.markdown("Passionate and results-driven 4th Year B.Tech CSE student (Graduating 2026) with a strong foundation in Data Structures and Algorithms, Object Oriented Programming, Java and Python. Actively building projects in Machine Learning, Computer Vision, Deep Learning, GenAI and Full-Stack Development. Quick learner with hands-on coding practice on platforms like LeetCode.", unsafe_allow_html=True)
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
    st.markdown(
        """<div class="subhead">
        I turn data into products and decisions—across ML, CV, and NLP. I love rapid prototyping,
        thoughtful UX, and measurable impact.
        </div>""",
        unsafe_allow_html=True,
    )
    # cta1, cta2, cta3 = st.columns([.18,.18,.64])
    # with cta1: st.markdown('<a class="btn btn-primary" href="#projects">View Projects</a>', unsafe_allow_html=True)
    # with cta2: st.markdown('<a class="btn btn-ghost" href="#contact">Contact</a>', unsafe_allow_html=True)
with colH2:
    st.markdown(
    f"""
    <div class="card card-hover" style="text-align:center;">
      <img src="data:image/png;base64,{img_base64}" 
           style="width:50%; border-radius:16px; border:1px solid #ccc;" />
      <div style="margin-top:.6rem; color: gray;">Based in India🌍 • Open to internships and full-time roles</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# =========================
# About + Quick facts
# =========================
a1, a2, a3, a4 = st.columns(4)
a1.metric("ML Projects", "12")
a2.metric("Dashboards", "4")
a3.metric("CV/NLP Models", "6")
a4.metric("Hackathons", "5")

st.write("")
ab_col1, ab_col2 = st.columns([1.4, 1])
with ab_col1:
    st.markdown(
        """
        <div class="card card-hover">
          <h3>Quick Peek</h3>
          <p style="color:var(--muted)">
          Final-year Data Science student with a strong foundation in machine learning, deep learning, and data visualization. 
          I enjoy building end-to-end ML pipelines — from clean data to elegant, explainable products.
          </p>
          <div class="tags">
            <span class="tag">Python</span>
            <span class="tag">TensorFlow</span>
            <span class="tag">scikit-learn</span>
            <span class="tag">OpenCV</span>
            <span class="tag">Transformers</span>
            <span class="tag">SQL</span>
            <span class="tag">Plotly</span>
            <span class="tag">Streamlit</span>
          </div>
        </div>
        """, unsafe_allow_html=True
    )
with ab_col2:
    st.markdown(
        """
        <div class="card card-hover">
          <h3>Contact</h3>
          <div style="line-height:1.9;">
            <strong>Email:</strong> anshkedia.04@gmail.com<br>
            <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/ansh-kedia-249843266/" target="_blank">linkedin.com/in/anshkedia</a><br>
            <strong>GitHub:</strong> <a href="https://github.com/anshkedia-04" target="_blank">github.com/anshkedia</a><br>
          </div>
          <div style="margin-top: .8rem;">
            <a class="btn btn-ghost" href="mailto:anshkedia.04@gmail.com">Email Me</a>
            <a class="btn btn-primary" href="https://github.com/anshkedia-04" target="_blank">GitHub</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================
# Skills Section
# =========================
# =========================
# Skills Section
# =========================
st.markdown("## Skills & Expertise")
st.caption("Categorized skills with icons instead of charts")

# Define skill categories
skill_categories = {
    "Programming": [
        (" Python", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"),
        (" Java", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg"),
        (" SQL", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg"),
        (" Git", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg"),
    ],
    "Data Science": [
        ("Pandas", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg"),
        ("NumPy", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg"),
        ("Scikit-learn", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/scikitlearn/scikitlearn-original.svg"),
    ],
    "Deep Learning": [
        ("TensorFlow", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tensorflow/tensorflow-original.svg"),
        ("PyTorch", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg"),
        ("CNN", "https://cdn-icons-png.flaticon.com/512/3522/3522092.png"),
    ],
    "Visualization": [
        ("Streamlit", "https://streamlit.io/images/brand/streamlit-mark-color.png"),
        ("Tableau", "https://cdn.worldvectorlogo.com/logos/tableau-software.svg"),
        ("PowerBI", "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/powerbi/powerbi-original.svg"),
    ]
}

# Layout: 2 columns
col1, col2 = st.columns(2)

for i, (category, skills) in enumerate(skill_categories.items()):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"### {category}")
        for name, icon_url in skills:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; margin-bottom:10px;" class="card card-hover">
                    <img src="{icon_url}" alt="{name}" width="28" style="margin-right:10px;">
                    <span style="font-size:16px;">{name}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# =========================
# Projects Section
# =========================
st.markdown('<a id="projects"></a>', unsafe_allow_html=True)
st.markdown("## Projects")
st.caption("Filter by tag and explore interactive demos")


PROJECTS = [
    {
        "title": "🧑🏻‍💻 Facemask 360",
        "desc": "A comprehensive solution for marking attendance using facial recognition.",
        "tags": ["Classification", "Facenet", "Scikit-learn", "OpenCV", "Streamlit"],
        "img": "https://i.pinimg.com/1200x/d9/0d/06/d90d064ba19dfb99b8f49a33bf52b443.jpg",
        "repo": "https://github.com/anshkedia-04/Smart_Attend",
        "demo": None
    },
    {
        "title": "🏡 House Price Prediction",
        "desc": "Regression pipeline with cross-validation, feature selection, and hyperparameter tuning.",
        "tags": ["ML", "Regression", "EDA","Streamlit"],
        "img": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=1600&auto=format&fit=crop",
        "repo": "https://github.com/anshkedia-04/House-Price-Prediction-",
        "demo": "https://csiassignment7-3mwhmzgnnqyr55wv8caelj.streamlit.app/"
    },
    {
        "title": "🤖 BrewBot",
        "desc": "Cafe FAQ Chatbot is an intelligent, open-source chatbot designed specifically for newly launched or small cafés that want a cost-effective customer support solution.",
        "tags": ["Langchain","HuggingFace","Streamlit"],
        "img": "https://i.pinimg.com/736x/a4/40/c1/a440c171389639c89535247065f16809.jpg",
        "repo": "https://github.com/anshkedia-04/BrewBot",
        "demo": None
    },
    {
        "title": "🖱️ Mouse Controller",
        "desc": "A deep learning project that uses computer vision to control the mouse cursor with hand movements.",
        "tags": ["MediaPipe", "OpenCV", "Streamlit"],
        "img": "https://i.pinimg.com/736x/89/54/66/8954661b52c02049504910323fa29989.jpg",
        "repo": "https://github.com/anshkedia-04/Gesture_Mouse_Control",
        "demo": None
    },
    {
        "title": "🔊 Volume Controller",
        "desc": "A deep learning project that uses computer vision to control the volume of the system with simple hand gestures.",
        "tags": ["MediaPipe", "OpenCV", "Streamlit"],
        "img": "https://i.pinimg.com/736x/8a/31/39/8a3139faa5cc210fa7a749a812c31798.jpg",
        "repo": "https://github.com/anshkedia-04/computer_vision_projects/tree/main/VolumeControler",
        "demo": None
    }
    
]

# Tag filter
all_tags = ["All"] + sorted({t for p in PROJECTS for t in p["tags"]})
ft_col1, ft_col2 = st.columns([.7, .3])
with ft_col1:
    active_tag = st.segmented_control("Filter by Tag", options=all_tags, default="All", key="tag_filter")
with ft_col2:
    search = st.text_input("Search", placeholder="Search by title or description")

def show_demo(kind: str):
    if kind == "fraud":
        fraud_data = pd.DataFrame({"Class": ["Normal", "Fraudulent"], "Count": [284315, 492]})
        fig = px.pie(fraud_data, names="Class", values="Count", title="Distribution of Transactions")
        st.plotly_chart(fig, use_container_width=True)
    elif kind == "housing":
        import numpy as np
        df = pd.DataFrame({"price": np.random.lognormal(mean=11.5, sigma=0.4, size=5000)})
        fig = px.histogram(df, x="price", nbins=50, title="Sample Price Distribution")
        fig.update_xaxes(title="Price")
        fig.update_yaxes(title="Count")
        st.plotly_chart(fig, use_container_width=True)
    elif kind == "recsys":
        sim = pd.DataFrame({
            "Movie": ["Inception","Interstellar","Tenet","The Prestige","Memento"],
            "Similarity": [0.95, 0.92, 0.88, 0.85, 0.83]
        })
        fig = px.bar(sim, x="Movie", y="Similarity", title="Top Similar Movies")
        fig.update_yaxes(range=[0,1])
        st.plotly_chart(fig, use_container_width=True)

# Grid of projects
rows = []
for p in PROJECTS:
    if active_tag != "All" and active_tag not in p["tags"]:
        continue
    if search and (search.lower() not in p["title"].lower() and search.lower() not in p["desc"].lower()):
        continue
    rows.append(p)

if not rows:
    st.info("No projects match your filter. Try clearing search/tags.")
else:
    # show in responsive 3-column grid
    for i in range(0, len(rows), 3):
        cols = st.columns(3, gap="large")
        batch = rows[i:i+3]
        for c, p in zip(cols, batch):
            with c:
                st.markdown(
                    f"""
                    <div class="card card-hover">
                      <img src="{p['img']}" class="project-cover" />
                      <h3 style="margin:.6rem 0 0 0;">{p['title']}</h3>
                      <p style="color:var(--muted); margin:.25rem 0 .6rem 0;">{p['desc']}</p>
                      <div class="tags">{''.join([f'<span class="tag">{t}</span>' for t in p['tags']])}</div>
                      <div style="display:flex; gap:.5rem; margin-top:.8rem;">
                        {"<a class='btn btn-ghost' href='"+p["repo"]+"' target='_blank'>Repo</a>" if p["repo"] and p["repo"]!="#" else ""}
                        {"<a class='btn btn-primary' href='#demo-"+p["demo"]+"'>Demo</a>" if p["demo"] else ""}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )



st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# =========================
# Resume (Timeline)
# =========================
st.markdown("## Highlights")
st.caption("Education, internships, and certifications")

resume_items = [
    {
        "when": "2022 — Present",
        "title": "B.Tech (Final Year) — Computer Science and Engineering",
        "where": "Parul University",
        "detail": "Coursework: ML, DL, CV, NLP, DSA, DBMS.",
        "logo": "logos/parul.png"
    },
    {
        "when": "Summer 2025",
        "title": "Data Science Summer Intern",
        "where": "Celebal Technologies Pvt. Ltd.",
        "detail": "Shipped ML features with A/B tested improvements.",
        "logo": "logos/celebal.png"
    },
    {
        "when": "2024",
        "title": "Accenture Certification",
        "where": "Data Analytics and Visualization Job Simulation",
        "detail": "Hands-on experience in data cleaning, visualization, and presenting insights.",
        "logo": "logos/accenture.png"
    },
    {
        "when": "2024",
        "title": "Cisco Certification",
        "where": "Python Essentials",
        "detail": "Built a strong foundation in Python programming, data structures, and scripting.",
        "logo": "logos/cisco.png"
    },
    {
        "when": "2024",
        "title": "Cisco Certification",
        "where": "Introduction to Data Science",
        "detail": "Gained foundational knowledge in data science concepts, tools, and techniques.",
        "logo": "logos/cisco.png"
    },
    {
        "when": "2024",
        "title": "Microsoft Certification",
        "where": "Ignite Edition Challenge",
        "detail": "Explored cloud computing concepts, AI integration, and Microsoft tools.",
        "logo": "logos/microsoft.png"
    },
]

cL, cR = st.columns([1.3, 1])
with cL:
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for it in resume_items:
        # Convert logo to base64 so it renders inline
        try:
            with open(it["logo"], "rb") as f:
                logo_b64 = base64.b64encode(f.read()).decode()
                logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:40px;height:40px;object-fit:contain;border-radius:8px;border:1px solid rgba(255,255,255,0.2);" />'
        except:
            logo_html = '<div style="width:40px;height:40px;border-radius:8px;background:rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;font-size:.8rem;color:gray;">N/A</div>'

        st.markdown(
            f"""
            <div class="timeline-item card-hover" style="display:flex; gap:1rem; align-items:center; padding:.9rem 1rem; border-radius:16px;">
              {logo_html}
              <div>
                <div style="color:#86efac; font-weight:700; font-size:.85rem;">{it['when']}</div>
                <div style="font-weight:700; margin-top:.15rem;">{it['title']}</div>
                <div style="color:var(--muted); font-size:.9rem;">{it['where']}</div>
                <div style="color:var(--muted); margin-top:.25rem; font-size:.9rem;">{it['detail']}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

with cR:
    # Load actual Resume.pdf from the same directory
    with open("Resume.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.markdown(
        """
        <style>
        .resume-card {
            background: linear-gradient(135deg, #1f2937, #111827);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            transition: transform 0.2s ease-in-out;
        }
        .resume-card:hover {
            transform: scale(1.03);
        }
        .resume-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #facc15; /* gold */
        }
        .resume-desc {
            font-size: 16px;
            color: #d1d5db;
            margin-bottom: 20px;
        }
        div.stDownloadButton > button {
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            color: white;
            border-radius: 12px;
            padding: 10px 18px;
            font-size: 16px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            font-weight: 600;
        }
        div.stDownloadButton > button:hover {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
            transform: translateY(-3px);
            box-shadow: 0px 8px 15px rgba(0,0,0,0.3);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="resume-card">
            <h3 class="resume-title">📄 My Resume</h3>
            <p class="resume-desc">Download a concise, elegant 1-page resume to know more about my journey.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button("⬇️ Download Resume", data=pdf_bytes, file_name="Resume.pdf", mime="application/pdf")


# =========================
# Contact Section
# =========================
st.markdown('<a id="contact"></a>', unsafe_allow_html=True)
st.markdown("## Contact")
st.caption("Let’s build something great together.")

contact_left, contact_right = st.columns([1.1, 1], gap="large")
with contact_left:
    with st.form("contact_form", clear_on_submit=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        msg = st.text_area("Message", height=140)
        sent = st.form_submit_button("Send Message ✉️", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if sent:
            if not (name and email and msg):
                st.warning("Please fill in all fields.")
            else:
                st.success("Thanks! Your default email app will open to send the message.")
                # Open mailto (best effort UX via markdown link)
                st.markdown(
                    f"[Click here if your email didn't open automatically](mailto:anshkedia.04@gmail.com?subject=Portfolio%20Contact%20from%20{name}&body={msg}%0A%0AFrom:%20{email})"
                )

with contact_right:
    st.markdown(
        """
        <div class="card card-hover">
          <h3>Connect</h3>
          <p style="color:var(--muted)">I’m active on these platforms — feel free to reach out.</p>
          <div style="display:grid; gap:.5rem; margin-top:.5rem;">
            <a class="btn btn-ghost" href="https://github.com/anshkedia-04" target="_blank">GitHub</a>
            <a class="btn btn-ghost" href="https://www.linkedin.com/in/ansh-kedia-249843266/" target="_blank">LinkedIn</a>
            <a class="btn btn-primary" href="mailto:anshkedia.04@gmail.com">Email</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# Footer
# =========================
st.write("")
st.markdown(
    f"""
    <div class="footer" style="text-align:center; margin:2rem 0 1rem 0;">
      © {datetime.now().year} Ansh Kedia 
    </div>
    """,
    unsafe_allow_html=True
)
