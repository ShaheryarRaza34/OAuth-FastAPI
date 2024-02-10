import requests
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse


app = FastAPI()
load_dotenv()
github_client_id = os.getenv('GITHUB_CLIENT_ID')
github_secret_id = os.getenv('GITHUB_SECRET_ID')
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_secret_id = os.getenv('GOOGLE_SECRET_ID')
google_redirect_url = os.getenv('GOOGLE_REDIRECT_URL')


@app.get("/auth/{id}")
async def authorize(id:str):
    if id == '1':
        return  RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code = 302)
    elif id == '2':
        return  RedirectResponse(f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={google_client_id}&redirect_uri={google_redirect_url}&scope=openid%20profile%20email&access_type=offline", status_code = 302)

@app.get('/login/{id}')
async def login(code:str, id:str):
    if id == '1':
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
    elif id == '2':
        return None