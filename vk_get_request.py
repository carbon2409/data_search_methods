import requests, json
link = 'https://api.vk.com/method/friends.getOnline?v=5.52&access_token=c68fa958c......'
req = requests.get(link)
if req.ok:
    with open('vk_friends.json', 'w') as f:
        json_repos = json.dump(req.text, f)