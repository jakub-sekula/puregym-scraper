import re
import requests
from bs4 import BeautifulSoup
import time

class AuthenticationError(Exception):
    pass

start_time = time.time()

USERNAME = "username"
PASSWORD = "password"

url = "https://puregym.com/members"

session = requests.session()

response = session.get(url)

soup = BeautifulSoup(response.content, "html.parser")
login_form = soup.find("form")
action_url = response.url
requestVerificationToken = login_form.find(
    "input", {"name": "__RequestVerificationToken"}
).get("value")

data = {
    "username": USERNAME,
    "password": PASSWORD,
    "__RequestVerificationToken": requestVerificationToken,
    "button": "login",
}

login_response = session.post(action_url, data=data)

if not login_response.status_code == 200:
    raise AuthenticationError(f'Authentication failed for user {USERNAME}')


soup = BeautifulSoup(login_response.content, "html.parser")
form = soup.find("form")
action_url = form.get("action")
code = form.find("input", {"name": "code"}).get("value")
id_token = form.find("input", {"name": "id_token"}).get("value")
scope = form.find("input", {"name": "scope"}).get("value")
state = form.find("input", {"name": "state"}).get("value")
session_state = form.find("input", {"name": "session_state"}).get("value")

data = {
    "code": code,
    "id_token": id_token,
    "scope": scope,
    "state": state,
    "session_state": session_state,
}

final_response = session.post(action_url, data=data)

soup = BeautifulSoup(final_response.content, "html.parser")
people_in_gym = soup.find("p", {"id": "people_in_gym"}).find("span").text

people_in_gym = re.search('\d+', people_in_gym).group()

print(people_in_gym)

end_time = time.time()

total_time = end_time - start_time
print('Finished in ', total_time, 's')