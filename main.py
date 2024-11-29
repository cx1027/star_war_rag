import sys
import json
from sklearn.metrics.pairwise import cosine_similarity
import openai
import common.utils
from sentence_transformers import SentenceTransformer

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Prompt a question to get user's question
def get_user_question():
    """Prompt the user to enter a question."""
    if len(sys.argv) == 1:
        # No command-line argument provided, prompt for input
        question = input("Please enter your question: ").strip()
        if not question:
            print("Error: Question cannot be empty.")
            sys.exit(1)
        return question
    elif len(sys.argv) == 2:
        # One command-line argument provided
        question = sys.argv[1].strip()
        if not question:
            print("Error: Question cannot be empty.")
            sys.exit(1)
        return question
    else:
        # Incorrect number of arguments
        print("Usage: python script.py [\"Your question\"]")
        print("If your question contains spaces, enclose it in quotes.")
        sys.exit(1)

# Read files as corpus
def read_corpus(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
            sentences = text.split('.')
            corpus = [sentence.strip() for sentence in sentences if sentence.strip()]
        return corpus
    except FileNotFoundError:
        print(f"Error: Corpus file '{file_path}' not found.")
        sys.exit(1)
    except IOError:
        print(f"Error: Unable to read corpus file '{file_path}'.")
        sys.exit(1)

# Use SentenceTransformer to search corpus by calculate similarities of question and corpus
def search_corpus(question, corpus, top_k=1):
    if not corpus:
        print("Error: Corpus is empty.")
        return []
    
    # Initialize the SentenceTransformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Encode the question and corpus
    question_embedding = model.encode([question])
    corpus_embeddings = model.encode(corpus)
    
    # Calculate cosine similarities
    similarities = cosine_similarity(question_embedding, corpus_embeddings)[0]
    
    # Get top-k most similar sentences
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    return [corpus[i] for i in top_indices]

# Function to generate response using OpenAI API
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            # model="Gpt4o", #API from Datacom
            model="gpt-4o", #OpenAI account
            messages=[
                {"role": "system", "content": "Please adopt Yoda's speaking style and respond in Yoda's style."},
                {"role": "user", "content": prompt}
            ]
        )
        if not response.choices:
            print("Error: Empty response from OpenAI API.")
            return None
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: API request failed - {str(e)}")
        return None

# Main RAG function
def rag_system(question, corpus_file):
    corpus = read_corpus(corpus_file)
    retrieved_context = search_corpus(question, corpus)
    
    if not retrieved_context:
        print("Error: No relevant context found in corpus.")
        return None
    
    prompt = f"Question: {question}\nContext: {retrieved_context[0]}\nAnswer the question based on the context provided."
    
    system_response = generate_response(prompt)
    
    if system_response is None:
        return None
    
    return {
        "user_prompt": question,
        "retrieved_context": retrieved_context[0],
        "system_response": system_response
    }

# Main execution
if __name__ == "__main__":
    
    question = get_user_question()

    corpus_file = "./data/star_wars_corpus.txt"
    
    openai.api_key = common.utils.get_openai_api_key()
    if not openai.api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    
    result = rag_system(question, corpus_file)
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to generate response.")