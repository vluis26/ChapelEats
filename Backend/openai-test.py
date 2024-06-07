from openai import OpenAI
client = OpenAI(api_key= "sk-proj-U3w4iOCdf6zvKLZdGbANT3BlbkFJf7oQjZ3r47YFfbCpSb2X")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)