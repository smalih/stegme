import requests
import shutil


category = 'nature'
categories='nature, city, technology, food, still_life, abstract, wildlife'.split(", ")
api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
response = requests.get(api_url, headers={'X-Api-Key': 'vUkWtBsXjrU12mz7Ep8YdQ==TYN8vUz4sZ34Rfe2', 'Accept': 'image/jpg'}, stream=True)
if response.status_code == requests.codes.ok:
    with open('img.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
else:
    print("Error:", response.status_code, response.text)

