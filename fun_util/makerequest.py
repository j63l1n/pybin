import requests

uri = 'http://asix.gelin.us'

response = requests.get(uri)
print(f'status code {response.status_code}')
print(f'headers:\n {response.headers}')


with open('requestout.html', 'w') as fout:
    fout.write(response.text)


