"""
Redrob AI Campus Hackathon — Resume Matching Engine
Streamlit Web App  |  pkl-backed edition
"""

import math
import pickle
import os
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Resume Matching Engine",
    page_icon="🎯",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background: #0f1117; }
    .block-container { padding-top: 2rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #262a3d);
        border: 1px solid #3a3f5c;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }
    .rank-badge {
        display: inline-block;
        background: #5865f2;
        color: white;
        border-radius: 50%;
        width: 28px; height: 28px;
        text-align: center;
        line-height: 28px;
        font-weight: 700;
        font-size: 13px;
        margin-right: 10px;
    }
    .rank-1 { background: #f4c542; color: #111; }
    .rank-2 { background: #adb5bd; color: #111; }
    .rank-3 { background: #cd7f32; color: #fff; }
    .score-pill {
        float: right;
        background: #5865f2;
        color: white;
        border-radius: 20px;
        padding: 2px 14px;
        font-size: 15px;
        font-weight: 600;
    }
    .skill-tag {
        display: inline-block;
        background: #2a2d3e;
        border: 1px solid #4a4f6a;
        border-radius: 6px;
        padding: 2px 10px;
        margin: 2px;
        font-size: 12px;
        color: #a8b2d8;
    }
    .skill-hit {
        background: #1a3a5c;
        border-color: #5865f2;
        color: #90c0ff;
    }
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a8b2d8;
        border-bottom: 1px solid #2a2d3e;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
    }
    .jd-card {
        background: linear-gradient(135deg, #1a1d2e, #1e2235);
        border: 1px solid #5865f2;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .vocab-chip {
        display: inline-block;
        background: #1e2235;
        border: 1px solid #3a3f5c;
        border-radius: 4px;
        padding: 1px 8px;
        margin: 2px;
        font-size: 11px;
        color: #7a82a8;
    }
    .step-box {
        background: #1a1d2e;
        border-left: 3px solid #5865f2;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        font-size: 13px;
        color: #c0c8e8;
    }
    .pkl-banner {
        background: linear-gradient(90deg, #1a3a2e, #1a2e1a);
        border: 1px solid #34d399;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        color: #6ee7b7;
        font-size: 13px;
    }
    .warn-banner {
        background: linear-gradient(90deg, #3a1a1a, #2e1a1a);
        border: 1px solid #f87171;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 1rem;
        color: #fca5a5;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SKILL ALIASES
# ══════════════════════════════════════════════════════════════════════════════
SKILL_ALIASES = {
    "python": "python", "pyhton": "python",
    "java": "java",
    "javascript": "javascript", "javascrpit": "javascript", "js": "javascript",
    "typescript": "typescript", "typescrpit": "typescript",
    "c++": "cpp", "cpp": "cpp",
    "r": "r", "kotlin": "kotlin",
    "machinelearning": "machine_learning", "machine learning": "machine_learning",
    "ml": "machine_learning", "sklearn": "machine_learning",
    "deeplearning": "deep_learning", "deep learning": "deep_learning",
    "deep-learning": "deep_learning",
    "tensorflow": "tensorflow", "pytorch": "pytorch", "keras": "keras",
    "nlp": "nlp", "bert": "bert", "xgboost": "xgboost",
    "feature engineering": "feature_engineering",
    "statistics": "statistics", "stats": "statistics",
    "regression": "regression", "clustering": "clustering",
    "data-viz": "data_visualization", "data visualization": "data_visualization",
    "data viz": "data_visualization", "matplotlib": "data_visualization",
    "tableau": "data_visualization", "power-bi": "data_visualization",
    "power bi": "data_visualization", "powerbi": "data_visualization",
    "pandas": "pandas", "numpy": "numpy",
    "react": "react", "reacts": "react", "reactjs": "react",
    "vue": "vue", "vue.js": "vue", "vuejs": "vue",
    "redux": "redux", "tailwind": "tailwind",
    "html/css": "html_css", "html css": "html_css",
    "html": "html_css", "css": "html_css",
    "jest": "jest", "graphql": "graphql",
    "node.js": "nodejs", "nodejs": "nodejs", "node js": "nodejs",
    "flask": "flask",
    "spring boot": "spring_boot", "springboot": "spring_boot",
    "rest api": "rest_api", "rest": "rest_api", "restapi": "rest_api",
    "microservices": "microservices",
    "sql": "sql", "mysql": "mysql", "mysq": "mysql",
    "postgresql": "postgresql", "postgres": "postgresql",
    "mongodb": "mongodb", "redis": "redis",
    "docker": "docker",
    "kubernetes": "kubernetes", "kubernates": "kubernetes", "k8s": "kubernetes",
    "ci/cd": "ci_cd", "cicd": "ci_cd", "ci cd": "ci_cd",
    "aws": "aws",
    "android": "android", "firebase": "firebase",
    "algorithms": "algorithms", "algoritms": "algorithms",
    "data structure": "data_structures", "data structures": "data_structures",
    "competitive programming": "competitive_programming",
    "ui/ux": "ui_ux", "ui ux": "ui_ux", "figma": "figma",
}

_MULTI  = sorted([k for k in SKILL_ALIASES if " " in k], key=len, reverse=True)
_SINGLE = {k: v for k, v in SKILL_ALIASES.items() if " " not in k}

# ══════════════════════════════════════════════════════════════════════════════
# CORE ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def normalize_skills(raw: str) -> list:
    tokens = [t.strip().lower() for t in raw.split(",")]
    result, seen = [], set()
    for token in tokens:
        canon = None
        for phrase in _MULTI:
            if token == phrase:
                canon = SKILL_ALIASES[phrase]
                break
        if canon is None and token in _SINGLE:
            canon = _SINGLE[token]
        if canon and canon not in seen:
            seen.add(canon)
            result.append(canon)
    return result

def build_vocab(resumes: list) -> list:
    all_skills = set()
    for _, skills in resumes:
        all_skills.update(skills)
    return sorted(all_skills)

def compute_tfidf(resumes: list, vocab: list) -> tuple:
    N_DOCS = len(resumes)
    df = {s: 0 for s in vocab}
    for _, skills in resumes:
        for s in skills:
            if s in df:
                df[s] += 1
    idx = {s: i for i, s in enumerate(vocab)}
    vectors = []
    for name, skills in resumes:
        N = len(skills)
        vec = [0.0] * len(vocab)
        for skill in skills:
            if skill in idx:
                vec[idx[skill]] = (1.0 / N) * math.log(N_DOCS / df[skill])
        vectors.append((name, vec))
    idf_map = {s: math.log(N_DOCS / df[s]) for s in vocab}
    return vectors, df, idf_map

def jd_binary(raw: str, vocab: list) -> tuple:
    skills = normalize_skills(raw)
    idx = {s: i for i, s in enumerate(vocab)}
    vec = [0] * len(vocab)
    hit = []
    for s in skills:
        if s in idx:
            vec[idx[s]] = 1
            hit.append(s)
    return vec, hit

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na  = math.sqrt(sum(x ** 2 for x in a))
    nb  = math.sqrt(sum(x ** 2 for x in b))
    return dot / (na * nb) if na and nb else 0.0

# ══════════════════════════════════════════════════════════════════════════════
# PKL LOADER  (cached so it only hits disk once per session)
# ══════════════════════════════════════════════════════════════════════════════
PKL_PATH = "resume_engine.pkl"

@st.cache_resource(show_spinner="Loading resume_engine.pkl …")
def load_pkl(path: str):
    """
    Returns (payload_dict, error_string).
    payload_dict keys: vocab, skill_idx, df, N_DOCS, resumes, resume_vectors, jd_vectors
    """
    if not os.path.exists(path):
        return None, f"File not found: {os.path.abspath(path)}"
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
        required = {"vocab", "skill_idx", "df", "N_DOCS",
                    "resumes", "resume_vectors", "jd_vectors"}
        missing = required - data.keys()
        if missing:
            return None, f"PKL missing keys: {missing}"
        return data, None
    except Exception as e:
        return None, str(e)


pkl_data, pkl_error = load_pkl(PKL_PATH)

# ══════════════════════════════════════════════════════════════════════════════
# DEFAULT DATASET  (fallback when pkl is absent / broken)
# ══════════════════════════════════════════════════════════════════════════════
DEFAULT_RESUMES = [
    ("Arjun Sharma",    "Pyhton, MachineLearning, SQL, pandas, numpy, Deep-learning"),
    ("Priya Nair",      "JavaScrpit, Reacts, Node.JS, MongoDb, REST api, HTML/CSS"),
    ("Rahul Gupta",     "Java, Spring Boot, MySql, Microservices, Docker, kubernates"),
    ("Sneha Patel",     "Python, TensorFlow, Keras, NLP, BERT, data-viz, matplotlib"),
    ("Vikram Singh",    "C++, Algoritms, Data Structure, competitive programming, python"),
    ("Ananya Krishnan", "javascript, vue.js, python, flask, PostgreSQL, AWS, CI/CD"),
    ("Karan Mehta",     "Python, Sklearn, XGboost, feature engineering, SQL, tableau"),
    ("Deepika Rao",     "Java, Android, Kotlin, Firebase, REST, UI/UX, figma"),
    ("Aditya Kumar",    "Reactjs, TypeScrpit, GraphQL, redux, tailwind, nodejs, jest"),
    ("Meera Iyer",      "python, R, statistics, ML, regression, clustering, Power-BI"),
]
DEFAULT_JDS = [
    ("JD-1", "Kakao",  "ML Engineer",
     "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Data Visualization,"
     " NLP, BERT, Feature Engineering, Statistics"),
    ("JD-2", "Naver",  "Backend Engineer",
     "Java, Spring Boot, MySQL, PostgreSQL, Microservices, Docker, Kubernetes,"
     " REST API, CI/CD, Redis"),
    ("JD-3", "Line",   "Frontend Engineer",
     "JavaScript, React, Vue, TypeScript, REST API, HTML/CSS,"
     " Node.js, GraphQL, Redux, Jest, AWS"),
]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Dataset")

    # ── PKL status banner ────────────────────────────────────────────────────
    if pkl_data:
        st.markdown(
            f'<div class="pkl-banner">✅ <strong>resume_engine.pkl loaded</strong><br>'
            f'{len(pkl_data["resumes"])} candidates · {len(pkl_data["vocab"])} skills<br>'
            f'<span style="opacity:.7">Sidebar edits recompute on-the-fly; pkl used as seed.</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="warn-banner">⚠️ <strong>PKL not loaded</strong> — using hardcoded defaults.<br>'
            f'<code style="font-size:11px">{pkl_error}</code></div>',
            unsafe_allow_html=True,
        )

    # ── Seed resume rows from pkl if available, else hardcoded ───────────────
    seed_resumes_raw: list[tuple[str, str]] = []
    if pkl_data:
        for name, skills in pkl_data["resumes"]:
            seed_resumes_raw.append((name, ", ".join(skills)))
    else:
        seed_resumes_raw = DEFAULT_RESUMES

    st.markdown("**Resumes**")
    resume_inputs = []
    for name, raw in seed_resumes_raw:
        col1, col2 = st.columns([2, 3])
        with col1:
            n = st.text_input("Name",   value=name, key=f"name_{name}", label_visibility="collapsed")
        with col2:
            r = st.text_input("Skills", value=raw,  key=f"raw_{name}",  label_visibility="collapsed")
        resume_inputs.append((n, r))

    st.markdown("---")
    st.markdown("**Job Descriptions**")

    # Seed JD rows: pkl stores jd_vectors as (id, company, role, bin_vec).
    # We reconstruct the raw skill string from DEFAULT_JDS since pkl doesn't
    # store the original raw text (only the binary vector).  JD inputs remain
    # fully editable regardless.
    jd_inputs = []
    for jd_id, company, role, raw in DEFAULT_JDS:
        with st.expander(f"{jd_id} — {company}"):
            company_in = st.text_input("Company", value=company, key=f"co_{jd_id}")
            role_in    = st.text_input("Role",    value=role,    key=f"ro_{jd_id}")
            raw_in     = st.text_area("Skills",   value=raw,     key=f"sk_{jd_id}", height=100)
        jd_inputs.append((jd_id, company_in, role_in, raw_in))

    # ── Reload pkl button ────────────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔄 Reload PKL from disk"):
        st.cache_resource.clear()
        st.rerun()

    # ── Export current state as pkl ──────────────────────────────────────────
    if st.button("💾 Save current state → PKL"):
        resumes_tmp  = [(n, normalize_skills(r)) for n, r in resume_inputs if n.strip()]
        vocab_tmp    = build_vocab(resumes_tmp)
        rvecs_tmp, df_tmp, _ = compute_tfidf(resumes_tmp, vocab_tmp)
        N_tmp        = len(resumes_tmp)
        df_tmp_full  = {s: df_tmp.get(s, 0) for s in vocab_tmp}
        sidx_tmp     = {s: i for i, s in enumerate(vocab_tmp)}

        jdvecs_tmp = []
        for jd_id, company, role, raw in jd_inputs:
            vec, _ = jd_binary(raw, vocab_tmp)
            jdvecs_tmp.append((jd_id, company, role, vec))

        payload = {
            "vocab":          vocab_tmp,
            "skill_idx":      sidx_tmp,
            "df":             df_tmp_full,
            "N_DOCS":         N_tmp,
            "resumes":        resumes_tmp,
            "resume_vectors": rvecs_tmp,
            "jd_vectors":     jdvecs_tmp,
        }
        try:
            with open(PKL_PATH, "wb") as f:
                pickle.dump(payload, f)
            st.success(f"Saved → {os.path.abspath(PKL_PATH)}")
            st.cache_resource.clear()
        except Exception as e:
            st.error(f"Save failed: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTE  (always live from sidebar state; pkl just seeds the inputs)
# ══════════════════════════════════════════════════════════════════════════════
resumes_norm = [(n, normalize_skills(r)) for n, r in resume_inputs if n.strip()]
vocab        = build_vocab(resumes_norm)
r_vectors, df_map, idf_map = compute_tfidf(resumes_norm, vocab)

jd_data = []
for jd_id, company, role, raw in jd_inputs:
    jd_vec, jd_hits = jd_binary(raw, vocab)
    scores = sorted(
        [(name, cosine(rv, jd_vec)) for name, rv in r_vectors],
        key=lambda x: (-x[1], x[0])
    )
    jd_data.append({
        "id": jd_id, "company": company, "role": role,
        "raw": raw, "vec": jd_vec, "hits": jd_hits,
        "scores": scores, "top3": scores[:3],
    })

# ══════════════════════════════════════════════════════════════════════════════
# TITLE
# ══════════════════════════════════════════════════════════════════════════════
st.title("🎯 Resume Matching Engine")

if pkl_data:
    st.caption(
        f"Redrob AI Campus Hackathon · TF-IDF + Cosine Similarity · "
        f"Seeded from **resume_engine.pkl** "
        f"({len(pkl_data['resumes'])} candidates, {len(pkl_data['vocab'])} skills)"
    )
else:
    st.caption(
        "Redrob AI Campus Hackathon · TF-IDF + Cosine Similarity · "
        "⚠️ PKL not found — running on hardcoded defaults"
    )

tabs = st.tabs(["🏆 Results", "📄 Resumes & JDs", "🔬 TF-IDF Debug", "📚 Vocabulary"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    cols = st.columns(3)
    for col, jd in zip(cols, jd_data):
        with col:
            st.markdown(f"""
            <div class="jd-card">
                <div style="font-size:1.15rem;font-weight:700;color:#ffffff;margin-bottom:4px">
                    {jd['id']} — {jd['company']}
                </div>
                <div style="color:#7a82a8;font-size:13px;margin-bottom:1rem">{jd['role']}</div>
            """, unsafe_allow_html=True)

            for rank, (name, score) in enumerate(jd["top3"], 1):
                st.markdown(f"""
                <div class="metric-card">
                    <span class="rank-badge rank-{rank}">{rank}</span>
                    <strong style="color:#e0e6ff">{name}</strong>
                    <span class="score-pill">{score:.2f}</span>
                </div>
                """, unsafe_allow_html=True)

            fmt = ", ".join(f"{n}({s:.2f})" for n, s in jd["top3"])
            st.code(fmt, language=None)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Full Similarity Rankings")
    for jd in jd_data:
        with st.expander(f"{jd['id']} — {jd['company']} ({jd['role']}) — All candidates"):
            for i, (name, score) in enumerate(jd["scores"], 1):
                st.markdown(f"**{i}. {name}** — `{score:.4f}`")
                st.progress(min(score, 1.0))

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — RESUMES & JDS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="section-header">📄 Normalized Resume Skills</div>', unsafe_allow_html=True)
        all_jd_hits = set()
        for jd in jd_data:
            all_jd_hits.update(jd["hits"])

        for name, skills in resumes_norm:
            tags = "".join(
                f'<span class="skill-tag skill-hit">{s}</span>'
                if s in all_jd_hits else
                f'<span class="skill-tag">{s}</span>'
                for s in skills
            )
            st.markdown(
                f'<div class="metric-card"><strong style="color:#e0e6ff">{name}</strong>'
                f'<div style="margin-top:6px">{tags}</div></div>',
                unsafe_allow_html=True
            )
        st.caption("🔵 Highlighted = skill appears in at least one JD")

    with c2:
        st.markdown('<div class="section-header">📋 Job Descriptions</div>', unsafe_allow_html=True)
        for jd in jd_data:
            tags    = "".join(f'<span class="skill-tag skill-hit">{s}</span>' for s in jd["hits"])
            dropped = [s for s in normalize_skills(jd["raw"]) if s not in vocab]
            st.markdown(
                f'<div class="jd-card">'
                f'<strong style="color:#fff">{jd["id"]} — {jd["company"]}</strong>'
                f'<div style="color:#7a82a8;font-size:12px;margin-bottom:8px">{jd["role"]}</div>'
                f'<div>{tags}</div>'
                + (f'<div style="margin-top:8px;color:#f87171;font-size:11px">⚠ Not in vocab: {", ".join(dropped)}</div>'
                   if dropped else "")
                + "</div>",
                unsafe_allow_html=True
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — TF-IDF DEBUG
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">🔬 TF-IDF Values</div>', unsafe_allow_html=True)

    # Show whether we're reading live or from pkl
    if pkl_data:
        source_label = "📦 IDF values computed from pkl-seeded dataset (live, sidebar-editable)"
    else:
        source_label = "⚙️ IDF values computed live from hardcoded defaults"
    st.caption(source_label)

    selected = st.selectbox("Select candidate", [n for n, _ in resumes_norm])
    r_skills = next(s for n, s in resumes_norm if n == selected)
    r_vec    = next(v for n, v in r_vectors   if n == selected)
    N        = len(r_skills)

    st.markdown(f"**Skills after normalization** ({N} unique): `{r_skills}`")
    st.markdown(f"**TF = 1 / {N} = {1/N:.6f}**")

    rows = []
    for skill in r_skills:
        if skill in idf_map:
            tf   = 1.0 / N
            idf  = idf_map[skill]
            rows.append({
                "Skill": skill,
                "df": df_map[skill],
                "TF": round(tf, 6),
                "IDF (ln N/df)": round(idf, 6),
                "TF-IDF": round(tf * idf, 6),
            })
    st.table(rows)

    st.markdown("---")
    st.markdown("**Cosine Similarity Breakdown per JD**")
    for jd in jd_data:
        dot_val = sum(a * b for a, b in zip(r_vec, jd["vec"]))
        norm_r  = math.sqrt(sum(x**2 for x in r_vec))
        norm_j  = math.sqrt(sum(x**2 for x in jd["vec"]))
        cos_val = dot_val / (norm_r * norm_j) if norm_r and norm_j else 0
        contributing = [
            vocab[i] for i, (a, b) in enumerate(zip(r_vec, jd["vec"])) if a > 0 and b > 0
        ]
        st.markdown(
            f'<div class="step-box">'
            f'<strong>{jd["id"]} ({jd["company"]})</strong> — cosine = <code>{cos_val:.4f}</code><br>'
            f'dot={dot_val:.4f} · |r|={norm_r:.4f} · |jd|={norm_j:.4f}<br>'
            f'Matching skills: <em>{", ".join(contributing) or "none"}</em>'
            f'</div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — VOCABULARY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    # If pkl is loaded, surface original pkl vocab alongside live vocab
    if pkl_data and pkl_data["vocab"] != vocab:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(
                f'<div class="section-header">📦 PKL Vocabulary — {len(pkl_data["vocab"])} skills</div>',
                unsafe_allow_html=True,
            )
            pkl_df = pkl_data["df"]
            chips_pkl = "".join(
                '<span class="vocab-chip" title="df=' + str(pkl_df.get(s, "?")) + '"> ' + s + '</span>'
                for s in pkl_data["vocab"]
            )
            st.markdown(f'<div style="line-height:2.2">{chips_pkl}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown(
                f'<div class="section-header">⚙️ Live Vocabulary — {len(vocab)} skills</div>',
                unsafe_allow_html=True,
            )
            chips_live = "".join(
                f'<span class="vocab-chip" title="df={df_map[s]}">{s}</span>'
                for s in vocab
            )
            st.markdown(f'<div style="line-height:2.2">{chips_live}</div>', unsafe_allow_html=True)
    else:
        label = "📦 PKL" if pkl_data else "⚙️ Live"
        st.markdown(
            f'<div class="section-header">{label} Vocabulary — {len(vocab)} skills (alphabetical)</div>',
            unsafe_allow_html=True,
        )
        chips = "".join(
            f'<span class="vocab-chip" title="df={df_map[s]}">{s}</span>'
            for s in vocab
        )
        st.markdown(f'<div style="line-height:2.2">{chips}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**IDF Table**")
    idf_rows = [
        {
            "Skill": s,
            "df": df_map[s],
            "IDF = ln(N/df)": round(math.log(len(resumes_norm) / df_map[s]), 6),
        }
        for s in vocab
    ]
    st.dataframe(idf_rows, use_container_width=True)