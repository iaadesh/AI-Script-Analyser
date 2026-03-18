# 🎬 Bullet — Script Intelligence

A Streamlit-powered AI system that analyzes short-form scripts and generates structured story insights using LangChain and Gemini 2.5 Flash.

(I used Google Gemini cause it gives free API key)

---

## Features

| Feature | Description |
|---|---|
| **Story Summary** | 3–4 line narrative summary of the script |
| **Emotional Analysis** | Dominant emotions + 3-act emotional arc |
| **Engagement Score** | Overall score + factor breakdown (hook, conflict, tension, cliffhanger) |
| **Improvement Suggestions** | 3–5 actionable storytelling suggestions |
| **Cliffhanger Detection** | Identifies the most suspenseful moment and explains why it works |

---

## Folder Structure

```
script_analyzer/
│
├── app.py                   # Streamlit entry point
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
│
├── config/
│   ├── __init__.py
│   └── settings.py          # App config via pydantic-settings
│
├── core/
│   ├── __init__.py
│   ├── analyzer.py          # LangChain chain + JSON parsing logic
│   └── prompts.py           # All prompt templates + few-shot examples
│
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic output schemas (ScriptAnalysis, etc.)
│
└── ui/
    ├── __init__.py
    └── components.py        # Streamlit UI rendering components
```

---

## Setup

### 1. Clone / copy the project

```bash
cd script_analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## Usage

1. Open the app in your browser (default: `http://localhost:8501`)
2. Paste your script into the text area **or** click **Load Example** to try a sample
3. Click **🔍 Analyze Script**
4. Review the structured analysis across all sections

You can also enter your Gemini API key directly in the sidebar instead of using a `.env` file.

---

## Technical Design

### LangChain Chain

```
ChatPromptTemplate  →  Gemini (Gemini-2.5-Flash)  →  StrOutputParser  →  JSON Parser  →  Pydantic Model
```

### Prompt Engineering Strategy

- **Role-based system prompt**: The model is given a clear expert persona (script analyst)
- **Structured few-shot example**: A complete worked example (input → JSON output) grounds the model's output format and reasoning style
- **Output constraints**: The prompt explicitly instructs the model to return only valid JSON with no preamble or fences
- **Robust parsing**: `_extract_json()` strips markdown fences and falls back to regex-based JSON block extraction

### Schema Design (Pydantic v2)

All LLM output is validated against strict Pydantic schemas, ensuring type safety and easy access to nested analysis fields without fragile dict lookups.

---

## Customization

- **Switch models**: Change `MODEL_NAME` in `.env` or use the sidebar dropdown
- **Adjust temperature**: Lower for more consistent outputs, higher for more creative suggestions
- **Extend schemas**: Add new fields to `models/schemas.py` and reference them in `core/prompts.py`
- **Add new analysis sections**: Create a new renderer in `ui/components.py` and call it from `render_analysis()`
