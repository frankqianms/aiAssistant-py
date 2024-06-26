import json
import asyncio, os
from teams.ai.planners import AssistantsPlanner, AssistantsPlannerOptions
from openai.types.beta import AssistantCreateParams
from openai.types.beta.function_tool_param import FunctionToolParam
from openai.types.shared_params import FunctionDefinition

from dotenv import load_dotenv

load_dotenv(f'{os.getcwd()}/env/.env.testtool.user')

async def main():
    with open(
        f"{os.getcwd()}/src/utils/tool_schema.json", "r", encoding="utf-8"
    ) as file:
        tools = json.load(file)
    options = AssistantCreateParams(
        name="Assistant",
        instructions="\n".join([
            "You are an intelligent bot that can",
            "- write and run code to answer math questions",
            "- use the provided functions to answer questions"
        ]),
        tools=[
            # {
            #     "type": "code_interpreter",
            # },
            FunctionToolParam(
                type="function",
                function=FunctionDefinition(
                    name="getCurrentWeather",
                    description="Get the weather in location",
                    parameters=tools
                )
            )
            # FunctionToolParam(
            #     type="function",
            #     function=FunctionDefinition(
            #         name="getNickname",
            #         description="Get the nickname of a city",
            #         parameters={
            #             "type": "object",
            #             "properties": {
            #                 "location": {
            #                     "type": "string",
            #                     "description": "The city and state e.g. San Francisco, CA",
            #                 },
            #             },
            #             "required": ["location"],
            #         }
            #     )
            # )            
        ],
        model="gpt-3.5-turbo",
    )

    assistant = await AssistantsPlanner.create_assistant(api_key=os.getenv("SECRET_OPENAI_API_KEY"), organization="", endpoint="", request=options)
    print(assistant.tools)
    print(f"Created a new assistant with an ID of: {assistant.id}")

asyncio.run(main())