import requests
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.responses import RedirectResponse


app = FastAPI()
load_dotenv()

#Github Auth Credentials
github_client_id = os.getenv('GITHUB_CLIENT_ID')
github_secret_id = os.getenv('GITHUB_SECRET_ID')



#Google Auth Credentials
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_secret_id = os.getenv('GOOGLE_CLIENT_SECRET_ID')
google_redirect_url = os.getenv('GOOGLE_REDIRECT_URL')




@app.get("/auth/{id}")
async def authorize(id:str):

    if id == '1':

        authorization_url = os.getenv('GITHUB_AUTHORIZATION_URL')

        return  RedirectResponse(f'{authorization_url}{github_client_id}', status_code = 302)

    elif id == '2':

        authorization_url = os.getenv('GOOGLE_AUTHORIZATION_URL')

        return  RedirectResponse(f'{authorization_url}{google_client_id}&redirect_uri={google_redirect_url}&scope=openid%20profile%20email&access_type=offline', status_code = 302)

@app.get('/login/{id}')
async def login(code:str, id:str):
    
    if id == '1':
        
        token_url = os.getenv('GITHUB_TOKEN_URL')
        params = {
            'client_id': github_client_id,
            'client_secret': github_secret_id,
            'code': code
        }
        headers = {
            'Accept': 'application/json'
        }

        response = requests.post(token_url, params=params, headers=headers)

        access_token = response.json()['access_token']

        

        headers.update({'Authorization': f'Bearer {access_token}'})

        info_url = os.getenv('GITHUB_USER_INFO_URL')

        response = requests.get(info_url, headers=headers)

        return response.json()

    elif id == '2':

        token_url = os.getenv('GOOGLE_TOKEN_URL')

        params = {
        "code": code,
        "client_id": google_client_id,
        "client_secret": google_secret_id,
        "redirect_uri": google_redirect_url,
        "grant_type": "authorization_code",
         }

        response =  requests.post(token_url, params= params)

        access_token =  response.json()['access_token']
        
        headers = {'Authorization': f'Bearer {access_token}'}

        info_url = os.getenv('GOOGLE_USER_INFO_URL')
        
        user_info = requests.get(info_url, headers = headers)

        return user_info.json()

       
    

