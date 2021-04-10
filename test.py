import os


res = True if "API_KEY" in os.environ else False
print(res)
