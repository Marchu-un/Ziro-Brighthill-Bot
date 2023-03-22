import openai
import config

openai.api_key = config.token
engine="gpt-3.5-turbo" 


while True:
    prompt = str(input())

    completion = openai.ChatCompletion.create(
      model=engine,
      messages=[
        {"role": "user", "content": prompt}
      ]
    )

    print(completion['choices'][0]['message']['content'])

