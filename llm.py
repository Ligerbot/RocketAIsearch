from ollama import chat

response = chat(model='tinyllama', messages=[
    {'role': 'user', 'content': 'What is 2+2?'},
])
print(response['message']['content'])
