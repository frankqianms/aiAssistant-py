import os
import sys
import traceback
from typing import Any, Dict, Optional

from botbuilder.core import MemoryStorage, TurnContext
from teams import Application, ApplicationOptions, TeamsAdapter
from teams.ai import AIOptions
from teams.ai.planners import AssistantsPlanner, AssistantsPlannerOptions
from teams.state import TurnState

from config import Config

config = Config()
print(config.OPENAI_API_KEY)

planner = AssistantsPlanner[TurnState](
    AssistantsPlannerOptions(api_key=config.OPENAI_API_KEY, assistant_id=config.OPENAI_ASSISTANT_ID)
)

# Define storage and application
storage = MemoryStorage()
bot_app = Application[TurnState](
    ApplicationOptions(
        bot_app_id=config.APP_ID,
        storage=storage,
        adapter=TeamsAdapter(config),
        ai=AIOptions(planner=planner),
    )
)

@bot_app.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, state: TurnState):
    await context.send_activity("How can I help you today?")
    
@bot_app.ai.action("getCurrentWeather")
async def get_current_weather(context: TurnContext, state: TurnState):
    weatherData = {
        'San Francisco, CA': {
            'f': '71.6F',
            'c': '22C',
        },
        'Los Angeles': {
            'f': '75.2F',
            'c': '24C',
        },
    }
    # await context.send_activities("hello")
    location = context.data.get("location")
    if weatherData[location] == None:
        print(f"No weather data for ${location} found")
        # await context.send_activity(f"No weather data for ${location} found")
        return f"No weather data for ${location} found"
    
    print(weatherData[location][context.data.get("unit") if context.data.get("unit") else 'f'])
    # await context.send_activity(weatherData[location][context.data.get("unit") if context.data.get("unit") else 'f'])
    return weatherData[location][context.data.get("unit") if context.data.get("unit") else 'f']

@bot_app.ai.action("getNickname")
async def get_nickname(context: TurnContext, state: TurnState, parameters: Dict[str, Any]):
    nicknames = {
        'San Francisco, CA': 'The Golden City',
        'Los Angeles': 'LA',
    }
    location = parameters.get("location")
    
    await context.send_activity(nicknames[location]) if nicknames[location] else context.send_activity(f"No nickname for ${location} found")

@bot_app.error
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")