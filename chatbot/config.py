import os
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET_KEY = 'secret123'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# More


MAX_ATTEMPTS = 2
MAX_HISTORY = 20
TEMPERATURE = 0.7
CHATBOT_MODEL = "gpt-4o-mini"

INDEX_STORAGE_PATH = "resources/index_storage/chroma_db"
COLLECTION_NAME = "scott_masterclass"
EMBEDDING_MODEL = "text-embedding-3-small"
SIMILAR_TOP_K = 5

DAYS_OF_WEEK = {
    0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
    4: "Friday", 5: "Saturday", 6: "Sunday"
}