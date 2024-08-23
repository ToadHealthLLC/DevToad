from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()



client = OpenAI()

class SummaryResponse(BaseModel):
    summary: str

def generate_summary(text: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Generate a brief summary of the following text:"},
            {"role": "user", "content": text},
        ],
    )

    event = completion.choices[0].message.content

    # parse the event to json



    print(event)

    return event



####################################################
# from pydantic import BaseModel
# from dotenv import load_dotenv
# # import litellm
# load_dotenv()

# class SummaryResponse(BaseModel):
#     summary: str


# DEFAULT_MODEL = "gpt-4o-mini"

# def unstructured(prompt: str, model: str) -> str:
#     """LLM request with unstructured output: good for chat"""
#     try:
#         response = litellm.completion(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         raise Exception(f"Error calling LLM: {str(e)}")


# def structured(prompt: str, model: str) -> str:
#     """LLM request with structured output: good for other stuff"""
#     try:
#         response = litellm.completion(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         raise Exception(f"Error calling LLM: {str(e)}")