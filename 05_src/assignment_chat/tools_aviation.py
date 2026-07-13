from langchain.tools import tool
import json
import requests



@tool
def get_early_flight(n:int=1):
    """
    Returns n of the first flights of the day from whichever airport the user specifies.
    """
    url = "https://api.aviationstack.com/v1/flights?access_key=
    params = {
        "count": n
    }
    response = requests.get(url, params=params)
    resp_dict = json.loads(response.text)
    flight_list = resp_dict.get("data", [])
    flights = "\n".join([f"{i+1}. {fact}\n" for i, fact in enumerate(flights_list)])
    return facts