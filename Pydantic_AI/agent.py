import requests                                                                 # Used to call external APIs
import os                                                                       # Used to set environment variables
from pydantic import BaseModel                                                  # From Pydantic, helps define structured data (like a schema)
from pydantic_ai import Agent, RunContext                                       # used to create an AI agent and Runcontext Provides runtime context inside tools
from pydantic_ai.settings import ModelSettings                                  # Used to configure model behavior (like temperature)

os.environ["GROQ_API_KEY"]="<groq-api-key>"     # we have set the api key

# Define  the output schema for the tool

class WeatherForecast(BaseModel):                                                       # Creates a structured response format
    location: str
    description: str
    temperature_celsius: float

weather_agent = Agent(                                                                  # here we are defining the AI agent with model , model settings 
    model= "groq:llama-3.3-70b-versatile",
    model_settings=ModelSettings(temperature=0.2),
    output_type= str,
    system_prompt= ("You are a helpful weather assistant."
                    "Use the get_weather_forecast tool to find current weather conditions for any city."
                    "Provide clean and friendly answers.")
)   


# weather forecast tool

@weather_agent.tool                                                              # here we are defining the weather tool for AI agent and we are using
                                                                                 # Decorator → registers this function as a tool
                                                                                 # also The AI can call it automatically when needed   

def get_weather_forecast(ctx: RunContext, city: str) -> WeatherForecast:                       # this is the function(tool) taking runtime context and city as input parameter
    """This function returns the current weather forecast for the given city using weatherapi """
    apikey= "<weather-api-key>"                                          # passing the weather api key for connecting it with openweathermap
    baseurl= "https://api.openweathermap.org/data/2.5/weather"                      
    
    units= "metric"                                                                    # this is the payload paramters which we are providing to openweathermap
    params= {
        'q': city,
        'appid': apikey,
        'units': units
    }
    response = requests.get(baseurl, params=params)
    result = response.json()

    weather = WeatherForecast(                                                           # extracting the values from json in a formatted way
    location=result["name"],
    description=result["weather"][0]["description"].capitalize(),
    temperature_celsius=result["main"]["temp"]
    )

    print("Returning:", weather)
    return weather
    
    # response = requests.get(baseurl, params=params)                                    # taking the response in response variable
    # result= response.json()
    # print("Status Code:", response.status_code)
    # print("Response:", response.text)                                                            # printing it here

# # normal way of taking the response

# agent_response= weather_agent.run_sync("what is the weather of Mumbai")                 # executing the agent here and taking response in agent_response
# # response = requests.get(baseurl, params=params)



# result = response.json()
# print(agent_response.output)

# taking user input

question= input("Ask about the weather :")                                            # executing the agent by taking user input
result= weather_agent.run_sync(question)
print(result.output)
