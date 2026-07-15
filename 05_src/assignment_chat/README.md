# Assignment 2 

I decided to try and make a game show host chatbot that would ask users trivia questions and engage them in a short learning experience. A further description of each compenent can be found below. 

## Service 1 

This is an API call to a trivia database https://opentdb.com/api_config.php that takes in the question and rephrases it as if a gameshow host is asking the question. The user will only respond with True/False responses and the bot assumes that is how it will respond. 

## Service 2 

Once the user answers the question, they will be told if their answer was correct or not and are asked if they want to learn more and based on the response. It then goes into a ChromaDB database to search through science related facts to provide more information about the particular question. 

## Service 3 

This is an additional fun fact provided straight from the OpenAI API and adds nuance to the second service which is pulling from the database. 

## assignment_chat organization

The assignment_chat folder, includes two python files, app.py and tools_trivia.py, and a data folder. 

> The app.py file includes the logic and initializes the chat function using Gradio. It utilizes an llm chatbot as well as an OpenAI client to be able to connect with the llm. Then it follows a simple logic to see what the user has entered in order to play the game. 

> The tools_trivia.py trivia file includes all of the helper functions that are used throughout the main code found in app.py. There are helper functions that get the trivia question from the trivia database, ones that rephrase the question, checking and revealing answers. This also includes the function for the final service that provides an additional fun fact outside of the RAG system implemented for service 2. 

> In the data folder, there is a ChromaDB database that holds the embeddings for a small subset of wikipedia articles that was downloaded to create an additional bank of answers. The embeddings were learned in the build_embeddings.ipynb file which doesn't need to be run for the submission but the code is there to demonstrate how I used it. 

Overall this is a limited implementation and there is so much to do to make it really interesting and engaging. The functionality works fairly well. 


