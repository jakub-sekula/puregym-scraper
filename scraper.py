import re
import requests
from bs4 import BeautifulSoup
import time
import argparse

class AuthenticationError(Exception):
    pass

def get_gym_occupancy(username, password):


    ENTRY_URL = "https://puregym.com/members"

    session = requests.session()

    response = session.get(ENTRY_URL)

    # The login page has a hidden field with a CSRF token which we need to submit
    # along with our credentials.

    soup = BeautifulSoup(response.content, "html.parser")
    login_form = soup.find("form")
    requestVerificationToken = login_form.find(
        "input", {"name": "__RequestVerificationToken"}
    ).get("value")

    data = {
        "username": username,
        "password": password,
        "__RequestVerificationToken": requestVerificationToken,
        "button": "login",
    }

    login_response = session.post(response.url, data=data)

    if not login_response.status_code == 200:
        raise AuthenticationError(f'Authentication failed for user {args.username}')

    # If the credentials are correct, it redirects us to a page with a hidden form
    # containing OAuth parameters. We need to submit this form to get to the final
    # members' area.

    soup = BeautifulSoup(login_response.content, "html.parser")
    hidden_form = soup.find("form")

    action_url = hidden_form.get("action")
    code = hidden_form.find("input", {"name": "code"}).get("value")
    id_token = hidden_form.find("input", {"name": "id_token"}).get("value")
    scope = hidden_form.find("input", {"name": "scope"}).get("value")
    state = hidden_form.find("input", {"name": "state"}).get("value")
    session_state = hidden_form.find("input", {"name": "session_state"}).get("value")

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

    # Regular expression to extract only the number
    people_in_gym = re.search('\d+', people_in_gym).group()

    return people_in_gym

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    parser.add_argument("password")
    args = parser.parse_args()

    people_in_gym = get_gym_occupancy(args.username, args.password)
    print(people_in_gym)
    print('Finished in ', time.time() - start_time, 's')