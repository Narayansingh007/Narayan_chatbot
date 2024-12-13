import os
import chromadb
from openai import OpenAI
from llama_index.core import Document, VectorStoreIndex, StorageContext, VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from prompt import SALE_PROMPT
from scheduling import convert_iso_datetime, convert_timestamp_to_datetime, get_two_weeks_later, get_first_valid_date
from config import CHATBOT_MODEL, TEMPERATURE, MAX_ATTEMPTS, MAX_HISTORY, \
    INDEX_STORAGE_PATH, COLLECTION_NAME, EMBEDDING_MODEL, SIMILAR_TOP_K
from config import OPENAI_API_KEY



def setup():

    # Set up storage config
    db = chromadb.PersistentClient(path=INDEX_STORAGE_PATH)
    chroma_collection = db.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL, embed_batch_size=10)
    Settings.embed_model = embed_model

    # Load index from storage
    index = VectorStoreIndex.from_vector_store(
        vector_store, storage_context=storage_context
    )

    # Create a similarity retriever
    retriever = index.as_retriever(similarity_top_k=SIMILAR_TOP_K)

    # Setup openAI model
    openai_client = OpenAI(
        api_key=OPENAI_API_KEY,
        timeout=30
    )
    return retriever, openai_client

def sale_script_welcome_message():
    return "Hi. I'm Scott from Freedom Property Investors. We're excited to share some amazing " \
           "property investment opportunities! Are you interested in learning more about " \
           "property investment strategies and our masterclass?"
           
def sale_script_reply_message(retriever, openai_client, history, date_time_condition):

    # Get relevant information
    # nodes = retriever.retrieve(history[-1]["content"])
    # relevant_documents = '\n=======\n\n'.join([
    #     f"Transcript #{i + 1}\n....\n{nodes[i].node.text}" for i in range(len(nodes))
    # ])

    # print("====== DEBUGING =====")
    # print("Questions:", history[-1]["content"])
    # print("Relevant information:")
    # print(relevant_documents)
    # print("=====================")
    # Send request to OpenAI
    system_prompt = SALE_PROMPT
    # system_prompt = system_prompt.replace("<<relevant_documents>>", relevant_documents)

    if "timestamp" in history[-1]:
        dt = convert_iso_datetime(history[-1]["timestamp"])
        today = convert_timestamp_to_datetime(dt)
        first_valid_date = get_first_valid_date(dt)
        system_prompt = system_prompt.replace("<<current_date_time>>", today)
        system_prompt = system_prompt.replace("<<first_valid_date>>", convert_timestamp_to_datetime(first_valid_date))
        system_prompt = system_prompt.replace("<<date_time_condition>>", date_time_condition)

    messages = [
        {"role": "system", "content": system_prompt}
    ]
    format_history = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
    messages.extend(format_history)

    for i in range(MAX_ATTEMPTS):
        try:
            response = openai_client.chat.completions.create(model=CHATBOT_MODEL,
                                                             messages=messages,
                                                             temperature=TEMPERATURE)
            answer = response.choices[0].message.content
        except:
            answer = "Our team will be in touch soon to provide more details. " \
                     "We're excited to help you on your property investment journey!"
    return answer