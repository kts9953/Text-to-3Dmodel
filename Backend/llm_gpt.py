from openai import OpenAI
from system_prompt_codeblock import SYSTEM_PROMPT
from codegen import extract_code_from_llm_output
import os

client = OpenAI()

def generate_user_code(prompt :str) -> str:
    
    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ],
    temperature=0.5)
    
    full_text = response.choices[0].message.content
    
    return full_text

