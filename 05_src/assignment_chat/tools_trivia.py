from langchain.tools import tool
import json
import requests
import chromadb
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv(".secrets")


def get_trivia_question():
    """
    Returns a science related true or false trivia question of medium difficulty.
    """
    url = "https://opentdb.com/api.php?amount=1&category=17&difficulty=medium&type=boolean"
    response = requests.get(url)
    resp_dict = json.loads(response.text)
    question_list = resp_dict.get("results", [])
    question_data = question_list[0] 
    return question_data

def rephrase_trivia_question(question_data: dict, llm) -> str:
    prompt = (
        f'''You are the host of an exciting television game show called "Truth or Bluff!" You will receive a Python dictionary in the following format:

    "question": "<question text>",
    "correct_answer": "<true_or_false>"

    Your job is to present the question dramatically and enthusiastically, as if speaking to a live audience.

    Rules:
    - Never reveal whether the answer is True or False before the contestant answers.
    - Build suspense and excitement.
    - Keep the introduction between 2 and 4 sentences.
    - End by clearly asking the contestant to choose "True" or "False."
    - Do not alter the wording or meaning of the question.
    - Do not include any explanation of the answer.
    Here is the question: {question_data}'''
    )
    response = llm.invoke(prompt)
    return response.content


def check_answer(user_message: str, correct_answer: str) -> bool:
    user_message = user_message.lower()
    correct_answer = correct_answer.lower()
    return user_message == correct_answer

def reveal_answer(question_data: dict, user_answer: bool, llm) -> str:
    prompt = (
        f'''You are the host of "Truth or Bluff!", reacting to a contestant's answer.

The question was: {question_data["question"]}
The correct answer was: {question_data["correct_answer"]}
The contestant answered: {user_answer}

Rules:
- React enthusiastically if correct, encouragingly if incorrect
- Reveal the correct answer clearly and dramatically
- End by asking if they'd like to learn more about this fact
- Maintain the energetic game show host personality throughout
'''
    )
    response = llm.invoke(prompt)
    return response.content

def is_affirmative(message):
    message = message.lower()

    return any(word in message for word in [
        "yes",
        "sure",
        "tell",
        "explain",
        "more",
        "why",
        "how",
        "detail"
    ])


def get_related_facts(query: str, question_data: dict, llm, openai_client, n_results: int = 3,) -> str:
    client = chromadb.PersistentClient(path="./data/chroma")
    collection = client.get_collection("science_facts")
    embedding = openai_client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding
    results = collection.query(query_embeddings=[embedding], n_results=n_results)
    facts = "\n\n".join(results["documents"][0])
    prompt = f"""
The user just answered this trivia question.

Question:
{question_data['question']}

Correct answer:
{question_data['correct_answer']}

Background information:
{facts}

Write a fun, engaging explanation in 2-3 sentences. Don't repeat the trivia question verbatim.
"""
    response = llm.invoke(prompt)
    return response.content

def generate_fun_fact(context, llm):
    prompt = f"""
You are a science trivia game show host.

Based on the scientific information below, provide one surprising
and interesting fun fact related to the topic.

Rules:
- Keep it under 2 sentences.
- Do not repeat the explanation.
- Make it entertaining for a general audience.

Scientific information:
{context}
"""

    response = llm.invoke(prompt)

    return response.content