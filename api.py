import requests
from PIL import Image


category = 'nature'
categories = ['nature',
              'city',
              'technology',
              'food',
              'still_life',
              'abstract',
              'wildlife']
api_url = f'https://api.api-ninjas.com/v1/randomimage?category={category}'
response = requests.get(api_url,
                        headers={
                                'X-Api-Key': 'vUkWtBsXjrU12mz7Ep8YdQ==TYN8vUz4sZ34Rfe2',
                                'Accept': 'image/png'
                                 },
                        stream=True
                        )
if response.status_code == requests.codes.ok:
    out_file = Image.open(response.raw)
    out_file.save('yoo.png')
