from tempMain import app
import json
import requests
url = "http://openstates.org/api/v1/metadata/tx/"
params = {"apikey":"3df8f699b8654d5ca218a7db79c8b0c4"}
resp = requests.get(url=url, params = params)
text = json.loads(resp.text)
print (text)

if __name__ == "__main__":
    app.run()
