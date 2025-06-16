import requests

new_post = {
    'title': 'foo',
    'body': 'bar',
    'userId': 1
}

response = requests.post('https://jsonplaceholder.typicode.com/posts', json=new_post)

print("Статус-код ответа:", response.status_code)
print("\nСодержимое ответа:")
print(response.json())