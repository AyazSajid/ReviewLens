

import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from tools import web_search, load_reviews

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


RETRY_KWARGS = dict(stop_after_attempt=6, wait_exponential_jitter=True)


web_review_agent = create_agent(
    model=llm,
    tools=[web_search],
    system_prompt="You are a research agent. Use the web_search tool to find live product reviews and opinions for the given product."
).with_retry(**RETRY_KWARGS)

dataset_agent = create_agent(
    model=llm,
    tools=[load_reviews],
    system_prompt="You are a research agent. Use the load_reviews tool to fetch reviews from the local dataset for the given product."
).with_retry(**RETRY_KWARGS)


summarizer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a product review summarizer. Based on the reviews provided, write a structured summary with: Overall Verdict, Pros, Cons, and Common Complaints."),
    ("human", "Reviews:\n{reviews}")
])

summarizer_chain = (summarizer_prompt | llm | StrOutputParser()).with_retry(**RETRY_KWARGS)


bias_checker_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a bias auditor. Review the given product summary and raw reviews it was based on. Check for:
- Overweighting of extreme (1-star or 5-star) reviews
- Small sample size issues
- Opinion presented as fact
- Signs of fake/incentivized reviews

Give a Bias Score out of 100 (100 = completely unbiased) and explain your reasoning."""),
    ("human", "Summary:\n{summary}\n\nRaw Reviews:\n{reviews}")
])

bias_checker_chain = (bias_checker_prompt | llm | StrOutputParser()).with_retry(**RETRY_KWARGS)


price_extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a price extraction assistant. From the given search results, extract ONLY the current approximate price of the product in INR (₹) and mention the source briefly. If multiple prices are found, give a typical/starting price range. If no price is found, respond with exactly: 'Price not available'. Keep your answer to one short line, no extra explanation."),
    ("human", "Search results:\n{search_results}")
])

price_extract_chain = (price_extract_prompt | llm | StrOutputParser()).with_retry(**RETRY_KWARGS)