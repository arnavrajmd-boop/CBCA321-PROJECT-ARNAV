# LLM Interaction 04: Project Dependency Installation & Verification

- **Project:** CBCA321 Project #6 — Developer Contribution Visualizer
- **Student:** Arnav Rajput (S24BCAU0194)
- **Phase:** Dependency Management

---

## 1. User Request

```text
Install the project dependencies inside the existing .venv environment.

Use the virtual environment's Python directly and run:

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Do not modify any project source files.

After installation, verify that Streamlit, GitPython, Pandas, Plotly, and Pytest are installed successfully.
```

---

## 2. Assistant Response & Action Taken

1. **Pip Upgrade & Dependency Installation**:
   - Executed pip upgrade and installed all libraries from `requirements.txt`:
     ```powershell
     .\.venv\Scripts\python.exe -m pip install --upgrade pip
     .\.venv\Scripts\python.exe -m pip install -r requirements.txt
     ```
2. **Library Import & Version Verification**:
   - Executed verification script via Python CLI to import and check the version of each specified package:
     ```powershell
     .\.venv\Scripts\python.exe -c "import streamlit, git, pandas, plotly, pytest; print('Streamlit:', streamlit.__version__); print('GitPython:', git.__version__); print('Pandas:', pandas.__version__); print('Plotly:', plotly.__version__); print('Pytest:', pytest.__version__)"
     ```

---

## 3. Result / Outcome

All 5 core packages were successfully installed and verified in `.venv`:

| Package | Installed Version | Status |
|---|---|---|
| **Streamlit** | `1.65.0` | Verified |
| **GitPython** | `3.2.0` | Verified |
| **Pandas** | `2.3.3` | Verified |
| **Plotly** | `6.9.0` | Verified |
| **Pytest** | `8.4.2` | Verified |

No project source files were modified.
