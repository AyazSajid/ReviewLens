import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """
    Searches the web for live product reviews and opinions using Tavily.
    Takes a search query (e.g., product name + 'reviews') and returns
    a cleaned string of search result snippets.
    """
    response = tavily_client.search(query=query, max_results=5)
    results = response.get("results", [])

    if not results:
        return f"No web results found for '{query}'."

    output = ""
    for r in results:
        output += f"Title: {r.get('title','')}\nSnippet: {r.get('content','')}\nSource: {r.get('url','')}\n\n"

    return output


@tool
def load_reviews(product_name: str) -> str:
    """
    Loads product reviews from the local CSV dataset for a given product name.
    Returns a cleaned string of review texts and ratings for that product.
    """
    try:
        df = pd.read_csv("data/reviews.csv")
    except FileNotFoundError:
        return "Error: reviews.csv not found in the data/ folder."

    filtered = df[df["product_name"].str.contains(product_name, case=False, na=False)]

    if filtered.empty:
        return f"No reviews found for '{product_name}' in local dataset."

    filtered = filtered.head(20)

    result = ""
    for _, row in filtered.iterrows():
        result += f"Rating: {row.get('rating', 'N/A')} | Review: {row.get('review_text', '')}\n"

    return result


@tool
def scrape_url(url: str) -> str:
    """
    Visits a given URL and extracts clean, readable text content from the page.
    Useful for getting full review details when a Tavily snippet isn't enough.
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)
        return text[:3000]
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


# ---- Tests only run when this file is executed directly, NOT when imported ----
if __name__ == "__main__":
    print(web_search.invoke("Vivo V70 Elite reviews"))