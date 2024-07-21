from fastapi import FastAPI, status

from fastzero.schemas import Message
from fastzero.routers import auth, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
def root_route():
  return { "message": "ok!" }