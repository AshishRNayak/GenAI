# this is the normal tool for main concept of the use ai agent proceed to this --> a:\Work\GenAI\AI_Agents\Pydantic_AI\agent.py

import requests

BASE_URL= "https://api.openweathermap.org/data/2.5/weather"
API_KEY= "<weather-api-key>"

def find_weather(city: str) -> dict:
    """This function returns the current weather forecast for the given city """

    units= "metric"
    params= {
        'q': city,
        'appid': API_KEY,
        'units': units
    }

    response = requests.get(BASE_URL, params=params)
    result= response.json()
    return result


output = find_weather("Pune")
print(output)