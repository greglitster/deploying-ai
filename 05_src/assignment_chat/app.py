import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from typing import Optional
import os
from pathlib import Path
from openai import OpenAI


from langchain.chat_models import init_chat_model

from tools_trivia import (rephrase_trivia_question, get_trivia_question, check_answer, reveal_answer, is_affirmative, get_related_facts,generate_fun_fact)

env_path = Path(__file__).parent.parent / ".secrets"
load_dotenv(env_path)

llm = init_chat_model(
    "gpt-4o-mini",
    model_provider="openai",
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")}
)

openai_client = OpenAI(
    base_url="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    api_key="any",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")}
)

current_question_data = None
game_state = "NEW_QUESTION"

def simple_chat(message: str, history: list[dict]) -> str:    
    global current_question_data,game_state
    if game_state == "NEW_QUESTION":
        current_question_data = get_trivia_question()
        game_state = "AWAITING_ANSWER"
        return rephrase_trivia_question(current_question_data, llm)
    elif game_state == "AWAITING_ANSWER":
        is_correct = check_answer(message, current_question_data['correct_answer'])
        game_state = "AWAITING_MORE_INFO" 
        return reveal_answer(current_question_data, message, llm)
    elif game_state == "AWAITING_MORE_INFO":
        is_yes = is_affirmative(message)
        if is_yes:
            search_query = (
                f"{current_question_data['correct_answer']} "
                f"{current_question_data['question']}"
            )

            related_facts = get_related_facts(
                query=search_query,
                question_data=current_question_data,
                llm=llm,
             openai_client=openai_client
            )

            fun_fact = generate_fun_fact(context=related_facts, llm=llm)
            return f"""{related_facts}
             
               Fun Fact: {fun_fact}"""
        else: 
            game_state ="NEW_QUESTION"
            return "Ready for another round whenever you are!"
    game_state = "NEW_QUESTION"
    return "Ready for another round whenever you are!"
        
        

gr.ChatInterface(
    fn=simple_chat,
).launch()