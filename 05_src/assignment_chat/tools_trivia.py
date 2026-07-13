from langchain.tools import tool
import json
import requests

from dotenv import load_dotenv

load_dotenv(".secrets")

@tool
def get_early_flight(n:int=1):
    """
    Returns the first n flights departing the specific airport the user wants.
    """
    url = "https://api.aviationstack.com/v1/flights?access_key=" + str(AVIATION_API_KEY)
    params = {
        "count": n
    }
    response = requests.get(url, params=params)
    resp_dict = json.loads(response.text)
    flights_list = resp_dict.get("data", [])
    flights = "\n".join([f"{i+1}. {fact}\n" for i, fact in enumerate(flights_list)])
    return flights