import requests
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse


app = FastAPI()
load_dotenv()
github_client_id = os.getenv('GITHUB_CLIENT_ID')
github_secret_id = os.getenv('GITHUB_SECRET_ID')

@app.get("/auth")
async def authorize():
    return  RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code = 302)

@app.get('/login')
async def login(code:str):
    print('here')
    params = {
        'client_id': github_client_id,
        'client_secret': github_secret_id,
        'code': code
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.post('https://github.com/login/oauth/access_token', params=params, headers=headers)
    access_token = response.json()['access_token']
    headers.update({'Authorization': f'Bearer {access_token}'})
    response = requests.get('https://api.github.com/user', headers=headers)
    return response.json()