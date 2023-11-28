import google.generativeai as palm
from string import Template
import os


palm.configure(api_key=os.environ.get('palm_key', ''))

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

prompt = Template("""

Given an specific phrase in Portuguese, your task is identify the verbs and list it 

Instructions:
1. You must list all verbs
2. For each verb listed discover its infinitive 
3. The response must be in Portuguese
4. The response must be a simple list of the verbs in its infinitive

Now, considering the above instructions in following text: $text

""")


def calc_verbs(text):
    completion = palm.generate_text(
        model=model,
        prompt=prompt.substitute(text=text),
        temperature=0,
        max_output_tokens=2000,
    )
    return completion.result
