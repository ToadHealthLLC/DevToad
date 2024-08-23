from .llm import generate_summary

text = """
With the popularization of software like OpenAI’s ChatGPT and Google’s Bard,
large language models (LLMs) have pervaded many aspects of life and work. For
instance, ChatGPT can be used to provide customized recipes, suggesting
substitutions for missing ingredients. It can be used to draft research proposals,
write working code in many programming languages, translate text between
languages, assist in policy making, and more (Gao 2023). Users interact with
large language models through “prompts'', or natural language instructions.
Carefully designed prompts can lead to significantly better outputs.
"""

print(generate_summary(text))