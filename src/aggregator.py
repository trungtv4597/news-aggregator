import re
import os
from dotenv import load_dotenv
from llama_index.core import Document, SummaryIndex, Settings
from llama_index.llms.openai import OpenAI
# from llama_index.llms.huggingface import
from llama_index.core.prompts import RichPromptTemplate

# from global_settings import INDEX_PATH, ARTICLES_STORE

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_LLM = os.getenv("OPENAI_LLM")

# Configure LLM
Settings.llm = OpenAI(api_key=OPENAI_API_KEY, model=OPENAI_LLM)
Settings.chunk_size = 512
Settings.chunk_overlap = 50

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def prepare_documents(articles):
    """
    LlamaIndex works with Document objects, which contain text and metadata.
    Best Pratices:
        - Why SimpleDirectoryReader might not be ideal for this case:
        ** Data Source Format: There are already structured making SimpleDirectoryReader unnecessary since it's designed for file-based inputs. Manual preparation ensures full control over how each articles is represented.
        ** Metadata Cstomization: While it supports metadata extraction, it's more generic and may not automatically extract NewsAPI-specific fields like source.name or publishedAt.
        - News articles are typically short, so chunking may not be needed. If articles are long, use SentenceSplitter.
    """
    # # load raw JSON data
    # with open(ARTICLES_STORE, "r", encoding="utf-8") as f:
    #     articles = json.load(f)

    # Create LlamaIndex Documents
    documents = []
    for article in articles:
        # Combine title, description, and content for full text
        text = re.sub(
            r"<[^>]+>", # Remove HTML tags
            r"",
            f"{article.get('title', '')}\n{article.get('description', '')}\n{article.get('content', '')}"
        ) 

        # Metadata for filtering/querying
        metadata = {
            "source": article["source"]["name"],
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
            "author": article.get("author", ""),
            "topic": article["topic"]
        }

        doc = Document(
            text=text,
            metadata=metadata,
            doc_id=article.get("url", str(hash(text))) # Unique ID
        )

        documents.append(doc)

    logger.info(f"Created {len(documents)}  LlamaIndex Documents")
    return documents

def summarize_news(articles):
    """
    Use SummaryIndex to enable summarization queries, as per the documentation. This is simple and iterates through all documents to synthesize answers.
    Best Pratices:
        - LLM Choice: Cost-effective, try open-source models like <mistral> via <HuggingFace>
    """
    topics = set(article.get("topic", "") for article in articles)
    
    documents = prepare_documents(articles)
    
    index = SummaryIndex.from_documents(documents)

    template = RichPromptTemplate(
        """
        Goal: {{goal_str}}
        ---
        Cotext: {{context_str}}
        ---
        Output Strucutre: 
        {{topic_str}}:
        {{key_takeaway_str}}
        """
    )

    prompt = template.format(
        goal_str="Summarize the key points from the provided articles concisely.",
        context_str="You will be a news summarization assistant, I will feed you a list of articles with titles, description, contents, and your job is aggregating inisight from that data.",
        topic_str=str(topics),
        key_takeaway_str="""
        Present your work under bullet points format like this example: 
        1. Key takeaway #1 key/term: summarized content | from source-1, source-2. 
        2. Key takeaway #2 key/term: summarized content | from source-1, source-2. 
        3. Key takeaway #3 key/term: summarized content | from source-1, source-2.
        """
    )

    # Create query engine
    query_engine = index.as_query_engine(
        response_mode="tree_summarize",
    )

    response = query_engine.query(prompt).response
    logger.info("News has been summarized.")
    return response


if __name__ == "__main__":
    from collector import fetch_articles
    topic = input("What are you searching for: ")
    articles = fetch_articles(topic)
    response = summarize_news(articles)
    print(f"LLM response: \n{response}")
