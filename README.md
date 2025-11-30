# Candidate Fit Predictor

This is a small Streamlit app that predicts a candidate fit probability using a toy logistic regression model.

Quick start

1. Create and activate a Python 3.11 virtual environment (recommended):

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app with Streamlit:

```bash
streamlit run candidate_fit_app.py
```

4. Open `http://localhost:8501` in your browser.

Notes
- Rename or remove any file that shadows `streamlit` imports (e.g. `import streamlit as st.py`).
- This project recommends Python 3.11 for smooth dependency installation.

Deploying
- To publish code: create a GitHub repository and push the code (instructions below).
- To deploy the app online, consider Streamlit Cloud (share.streamlit.io) or Render/Heroku.

Streamlit Cloud (recommended)
-----------------------------

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click "New app" → "From a GitHub repo".
3. Fill the form:
	- Repository: `mbouabid25/candidate-fit-predictor`
	- Branch: `main`
	- Main file path: `candidate_fit_app.py`
	- (Optional) Set Python version to `3.11` in Advanced settings.
4. Click "Deploy". Streamlit Cloud will install packages from `requirements.txt`.
5. Watch the build logs; when deployment completes you'll get a live URL you can share.

Troubleshooting
---------------
- If Streamlit Cloud shows dependency build errors, ensure `requirements.txt` lists the packages and try setting Python `3.11`.
- If the app doesn't appear or errors on start, copy the build logs and paste them here; I can help fix the issue.


License
- Add your license or keep it private if you prefer.
