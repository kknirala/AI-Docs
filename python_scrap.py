import requests
from bs4 import BeautifulSoup
import json
from readability import Document
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

URLS = [
    "https://medium.com/@senthilkumar.m1901/single-llm-to-agentic-ai-genais-evolution-explained-c0670d8325f3",
    "https://medium.com/@amihai.savir/beyond-rag-the-agentic-approach-to-genai-78be49725fdf",
    # add all your URLs here
]

def extract_article(url):
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    doc = Document(res.text)
    html = doc.summary()
    
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    
    title = doc.title()
    
    return title, text


def summarize(text):
    prompt = f"""
    Summarize the following article.

    Provide:
    - summary (5 lines)
    - 5 key points
    - category (choose from: LLM, RAG, Agentic AI, AI Agents, GenAI)

    Article:
    {text[:12000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content


def process():
    results = []

    for url in URLS:
        try:
            title, text = extract_article(url)
            summary = summarize(text)

            results.append({
                "title": title,
                "url": url,
                "summary_raw": summary
            })

            print(f"Processed: {title}")

        except Exception as e:
            print(f"Failed: {url}", e)

    with open("articles.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    process()
