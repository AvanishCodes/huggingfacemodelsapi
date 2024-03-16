# Voice models APIs

## Steps to interact with the API

- Start the application server
- - `python manage.py runserver`
- Go to [homepage](http://localhost:8000/)
- Create a user account using registration API (`/authentication/register/`)
- Generate an access token using `/authentication/register/` API by entering your username and password
- Insert the token as `Bearer {TOKEN}` in `Authorize` section. This token is valid for one hour.
- Now, you're authenticated to make requests.

- **Notes**
- - `/v1/diffusion/generations/` API takes quite a lot of time (may take 10 minutes too).
- - Use [Postman](https://www.postman.com) to use `/v1/pydub/stt/` and for file input, use form-data section in the body. I could not figure out using FILE Input in swagger in request body.
- - Unit tests do not work for authenticated APIs (when APIs require authentication).