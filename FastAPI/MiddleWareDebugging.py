from fastapi import FastAPI, HTTPException, Request
import random
import string

app=FastAPI()

users = {
    15: {"user_id": 15, "name": "John Doe"}
}

@app.middleware("http") #This middleware will print details in terminal for logging, we can add it to log file for advanced practice
async def debug(request: Request, call_next):

    print("Method:", request.method)
    print("Path:", request.url.path)
    print("Client:", request.client.host)

    response = await call_next(request)

    print("Status:", response.status_code)

    return response

@app.get('/') 
async def say_hi():
    return "Hello there. We are learning middleware" 

@app.get("/Users")
def get_users():
    return list(users.values())

@app.get("/Users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/Users")
def create_user(user_data: dict):
    user_id = max(users, default=0) + 1
    new_user = {**user_data, "user_id": user_id}
    users[user_id] = new_user
    return new_user

@app.put("/Users/{user_id}")
def update_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id]["name"] = "Updated User"
    return users[user_id]


''' Output will be like below
Request:
    PUT /users/15

Logs:
    Method: PUT
    Path: /users/15
    Client: 192.168.1.10
    Status: 200
'''