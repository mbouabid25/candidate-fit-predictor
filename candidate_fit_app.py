import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Candidate Fit Predictor", layout="centered")

# --- SESSION STATE INITIALIZATION ---
if "page" not in st.session_state:
    st.session_state.page = "Introduction"

# Initialize slider values in state if they don't exist
defaults = {
    "sql_need": 5,
    "python_need": 5,
    "strategy_need": 5,
    "vibe_check": 5
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- HELPER FUNCTIONS ---
def next_page(target_page):
    st.session_state.page = target_page
    st.rerun()

def show_progress():
    pages = ["Introduction", "SQL", "Python", "Strategy", "Vibe", "Results"]
    current_index = pages.index(st.session_state.page)
    progress_value = current_index / (len(pages) - 1)
    
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(progress_value)
    with col2:
        st.caption("⏳ Est. time: < 2 mins")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio(
    "Go to:", 
    ["Introduction", "SQL", "Python", "Strategy", "Vibe", "Results"],
    index=["Introduction", "SQL", "Python", "Strategy", "Vibe", "Results"].index(st.session_state.page)
)

if page_selection != st.session_state.page:
    st.session_state.page = page_selection
    st.rerun()

# --- MODEL TRAINING FUNCTION ---
@st.cache_resource
def get_trained_model():
    np.random.seed(42)
    n_samples = 200
    
    # Features: SQL, Python, Strategy, Vibe
    X = np.random.randint(0, 11, size=(n_samples, 4))
    
    # Weights determine "importance". 
    weights = np.array([0.8, 1.2, 1.0, 0.5]) 
    
    # We add a "Base Awesomeness" intercept (+8) 
    # This ensures that even if specific needs are low, the candidate's inherent value keeps them in the running.
    base_awesomeness = 8 
    
    score = np.dot(X, weights) + base_awesomeness + np.random.normal(0, 2, n_samples)
    
    # Threshold for "Hired" (15). With the base boost, it's easier to cross this line.
    y = (score > 15).astype(int)
    
    model = LogisticRegression()
    model.fit(X, y)
    return model

# --- PAGE LOGIC ---

# 1. INTRODUCTION PAGE
if st.session_state.page == "Introduction":
    st.title("📊 Welcome to the Candidate Fit Predictor")
    st.markdown(""" 
    The job market is rough, and I need all the help I can get!! 
    
    The problem is that people are busy, and I struggle to make them notice me on LinkedIn. So I decided to make this cool web app, hopefully, it can catch YOUR attention.
    
    This app uses a **logistic regression model** to predict the probability of a candidate being a good fit for your team based on your specific needs and data scraped on my resume. In this case, it will probably predict a great match! 
    (I promise I am awesome). 

    ### How It Works:
    1. You'll answer a few questions about your team's requirements.
    2. The model evaluates these inputs and calculates a match probability.
    3. Insights on the match are provided to help you make informed decisions.

    Click "Next" to begin!
    """)
    if st.button("Next: Data Needs"):
        next_page("SQL")
    
    show_progress()

# 2. SQL PAGE
elif st.session_state.page == "SQL":
    st.title("Does your team do a lot of SQL?")
    st.markdown("Every team deals with messy data. How much wrangling is required?")
    
    st.slider("Rate the need for SQL / Data Wrangling", 0, 10, key='sql_need')
    
    if st.button("Next: Python Needs"):
        next_page("Python")
        
    show_progress()

# 3. PYTHON PAGE
elif st.session_state.page == "Python":
    st.title("Does your team need predictive modeling?")
    st.markdown("Do you need someone to build models, automations, or pipelines in Python?")
    
    st.slider("Rate the need for Python / Modeling", 0, 10, key='python_need')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"): next_page("SQL")
    with col2:
        if st.button("Next: Strategy"): next_page("Strategy")
        
    show_progress()

# 4. STRATEGY PAGE
elif st.session_state.page == "Strategy":
    st.title("Does your team need business strategy?")
    st.markdown("Is it enough to just code, or do you need someone who understands the 'Why'?")
    
    st.slider("Rate the need for Business Strategy", 0, 10, key='strategy_need')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"): next_page("Python")
    with col2:
        if st.button("Next: Culture Fit"): next_page("Vibe")
        
    show_progress()

# 5. VIBE PAGE
elif st.session_state.page == "Vibe":
    st.title("Final Check: The Vibe")
    st.markdown("Cultural fit is key. How tolerant is your team of nerdy humor?")
    
    st.slider("Rate tolerance for Bad Stats Jokes", 0, 10, key='vibe_check')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"): next_page("Strategy")
    with col2:
        if st.button("Calculate Results 🚀"): next_page("Results")
        
    show_progress()

# 6. RESULTS PAGE
elif st.session_state.page == "Results":
    st.title("📊 The Verdict")
    st.markdown("Based on your inputs, here is the predicted probability of a successful hire.")
    
    model = get_trained_model()
    
    input_data = np.array([[
        st.session_state.sql_need,
        st.session_state.python_need,
        st.session_state.strategy_need,
        st.session_state.vibe_check
    ]])
    
    prediction_prob = model.predict_proba(input_data)[0][1]

    # --- DISPLAY METRICS ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.metric(label="Match Probability", value=f"{prediction_prob:.1%}")
        
        # Logic: If probability is reasonably high OR if it's low but we want to be cheeky
        if prediction_prob > 0.6:
            st.balloons()
            st.success("Result: It's a Match! 🚀")
        else:
            # Humorous fallback for low scores
            st.warning("Result: ...Outlier? 🤔")

    with col2:
        coefs = model.coef_[0]
        features = ['SQL', 'Python', 'Strategy', 'Team Vibe']
        impact = input_data[0] * coefs
        
        fig = go.Figure(go.Bar(
            x=impact,
            y=features,
            orientation='h',
            marker_color='#4F8BF9'
        ))
        fig.update_layout(
            title="Driver Analysis",
            xaxis_title="Impact Score",
            yaxis_title=None,
            height=300,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # --- DYNAMIC CONCLUSION ---
    if prediction_prob > 0.6:
        st.markdown("""
        ### Conclusion
        The model indicates a high probability of fit! 
        
        **Hypothesis:** I can help your team reach its goals.
        **Next Step:** Validate this hypothesis with a 15-minute intro.
        """)
    else:
        st.markdown(f"""
        ### Conclusion: The Model is Clearly Missing Something...
        
        Wait, only **{prediction_prob:.1%}**? 🤨 
        
        This simple algorithm fails to account for **Soft Skills**, **Drive**, and **Adaptability**. 
        If there's a skill gap, I'll close it in 2 weeks. Here are the latent variables the model missed:
        
        * ✅ **Fast Learner:** I picked up Streamlit just to build this app.
        * ✅ **Communication:** I can explain complex data to non-technical stakeholders.
        * ✅ **Grit:** I don't give up when the model predicts a 0 (or when code breaks).
        * ✅ **Juggling:** Literal juggling. It helps with multitasking.
        
        **Let's chat anyway. I bet I'm a better fit than this `LogisticRegression` thinks.**
        """)

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📧 Email Me", "mailto:marwa.bouabid@duke.edu")
    with c2:
        # Check if "resume.pdf" exists in the root directory. 
        # If yes, show download button. If no, fallback to LinkedIn so app doesn't crash.
        resume_file = "resume.pdf"
        if os.path.exists(resume_file):
            with open(resume_file, "rb") as f:
                pdf_data = f.read()
            st.download_button(
                label="📄 Download My Resume",
                data=pdf_data,
                file_name="Candidate_Resume.pdf",
                mime="application/pdf"
            )
        else:
            st.link_button("📄 View My Resume", "https://linkedin.com/in/yourprofile")
            
    if st.button("Start Over"):
        next_page("Introduction")
    
    show_progress()