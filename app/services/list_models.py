from llm import client

print("Models available for generateContent:\n")

for model in client.models.list():
    if model.supported_actions and "generateContent" in model.supported_actions:
        print(model.name)