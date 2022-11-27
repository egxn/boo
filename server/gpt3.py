import os
import openai

def completion_text(prompt):
  model = os.getenv("GPT3_MODEL_NAME")
  openai.organization = "Catcode"
  openai.api_key = os.getenv("OPENAI_API_KEY")
  return openai.Completion.create(model, prompt, 6, 0)
