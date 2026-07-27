# 🔍 ReviewLens

**An AI-powered multi-agent system that summarizes product reviews — and audits its own summary for bias.**

Most review summarizers just repeat whatever opinion is loudest, even if it's from a handful of extreme reviewers. ReviewLens uses two collaborating AI agents: one gathers and summarizes product reviews from live web search and a local dataset, and a second agent independently checks that summary for bias — flagging overweighted extreme reviews, small sample sizes, and signs of fake/incentivized reviews.

## ✨ Features

- **Live web research** — fetches real-time product reviews via the Tavily Search API
- **Dataset-backed research** — pulls historical reviews from a local CSV/Kaggle dataset
- **AI Summarizer Agent** — condenses raw reviews into a structured verdict (Pros, Cons, Common Complaints)
- **AI Bias Checker Agent** — audits the summary and raw reviews, returning a Bias Score (0–100) with reasoning
- **Live price lookup** — fetches an approximate current price for the product
- **Clean Streamlit UI** — styled, interactive interface to run the full pipeline from a browser

## 🏗️ Architecture

```
User Input (product name)
        │
        ├──► Web Review Agent  ──► Tavily Search Tool
        │
        ├──► Dataset Agent     ──► Local CSV Tool
        │
        ▼
Combined Reviews
        │
        ▼
Summarizer Chain (LCEL)  ──►  Structured Summary
        │
        ▼
Bias Checker Chain (LCEL) ──► Bias Score + Reasoning
        │
        ▼
Streamlit UI displays Price, Summary, and Bias Report
```

- **Agents** use LangChain's `create_agent`, reasoning dynamically about when to call their tools
- **Chains** use LCEL (`prompt | llm | StrOutputParser()`) for deterministic, fast processing once data is gathered

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| LLM | Groq (Llama 3.3 70B) |
| Orchestration | LangChain (LCEL + Agents) |
| Live Search | Tavily API |
| Dataset | Pandas + local CSV (Kaggle) |
| UI | Streamlit |

## 🚀 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/AyazSajid/ReviewLens.git
   cd ReviewLens
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Mac/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API keys**

   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_key_here
   TAVILY_API_KEY=your_tavily_key_here
   ```

5. **Add a reviews dataset**

   Place a CSV file at `data/reviews.csv` with columns: `product_name`, `rating`, `review_text`

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📸 Demo

*(Add a screenshot or GIF of the Streamlit UI here)*

## 🔮 Future Improvements

- Add a `scrape_url` tool to pull full review page content (beyond search snippets)
- Add rating-distribution charts from the dataset
- Deploy live on Streamlit Cloud
