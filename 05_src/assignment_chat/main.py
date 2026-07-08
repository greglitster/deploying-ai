import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from typing import Optional
import os

from langchain.chat_models import init_chat_model

load_dotenv('.secrets')
load_dotenv('.env')

