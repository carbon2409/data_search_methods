import requests
import json
main_link = 'https://api.github.com'
user = str(input('Введите имя пользователя '))
req = requests.get(f'{main_link}/users/{user}/repos')
#Get запрос выдает список словарей, количество элементов в списке совпадает с кол-вом репозиториев
if req.ok:
    data = json.loads(req.text)
    count = len(data)
    repo_list = []
    for n in range(count):
        repo_list.append(data[n]['name'])

print(repo_list)
#Сохраняем в json
with open('repos.json', 'w') as f:
    json_repos = json.dump(req.text, f)
    




