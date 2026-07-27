# pipeline.py

from agents import (
    web_review_agent,
    dataset_agent,
    summarizer_chain,
    bias_checker_chain,
    price_extract_chain,
)
from tools import web_search


def run_pipeline(product_name: str) -> dict:
    """
    Full pipeline:
    1. Web Review Agent fetches live reviews via Tavily
    2. Dataset Agent fetches reviews from local CSV
    3. Combine both into one review pool
    4. Summarizer Chain writes structured summary
    5. Bias Checker Chain audits the summary
    6. Price Extraction Chain fetches current price via web_search
    """

    # Step 1: Web reviews (live)
    web_result = web_review_agent.invoke({
        "messages": [{"role": "user", "content": f"Find reviews for {product_name}"}]
    })
    web_reviews = web_result["messages"][-1].content

    # Step 2: Dataset reviews (static CSV)
    dataset_result = dataset_agent.invoke({
        "messages": [{"role": "user", "content": f"Find reviews for {product_name}"}]
    })
    dataset_reviews = dataset_result["messages"][-1].content

    combined_reviews = f"--- Web Reviews ---\n{web_reviews}\n\n--- Dataset Reviews ---\n{dataset_reviews}"

    summary = summarizer_chain.invoke({"reviews": combined_reviews})

    bias_report = bias_checker_chain.invoke({
        "summary": summary,
        "reviews": combined_reviews
    })

    # Step 6: Price fetch
    price_search_results = web_search.invoke(f"{product_name} price in India")
    price = price_extract_chain.invoke({"search_results": price_search_results})

    return {
        "product": product_name,
        "raw_reviews": combined_reviews,
        "summary": summary,
        "bias_report": bias_report,
        "price": price,
    }

if __name__ == "__main__":
    product = input("Enter product name: ")
    result = run_pipeline(product)

    print("\nPRICE:\n", result["price"])
    print("\nSUMMARY:\n", result["summary"])
    print("\nBIAS REPORT:\n", result["bias_report"])