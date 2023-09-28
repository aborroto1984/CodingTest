import requests

url = "http://127.0.0.1:5000/create_product/testName/testSku23/testTypeName"

payload = {}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)