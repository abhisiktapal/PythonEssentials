from fastapi import FastAPI, Request
import random
import string

app=FastAPI()

@app.middleware("http")#With every api endpoint(get,post,put,delete) call, this middleware will get executed everytime
async def request_id_logging(request:Request,call_next): #this creates a requestID for every request(execution of the api method or endpoint)

    response= await call_next(request) #This executes the actual endpoint like "GET /"
    #call_next(request) is an async operation.
    #Without await: response = call_next(request) , response would contain a coroutine object, not the actual response.
    #Now the code in the below blocks get executed after the request is processed and response is recieved
    
    random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(10)) #Generating a random 10letter custom RequestId
    print(f'Log {random_letters}') #Printing on terminal for debugging and logging
    response.headers["MyCustom_Request-ID"]= random_letters #Adding to headers so that we can see it in the response on api docs
    return response

@app.get('/') #This is the Route function.
async def say_hi():
    return "Hello there. We are learning middleware" #Hitting "GET /" endpoint will just show this output on screen.



#Note: When you define a middleware of http, you are basically saying FastAPI -> "Run this function for every HTTP request that reaches this application."

''' The Flow will go like below
Client Request
      ↓
Middleware
      ↓
call_next(request)
      ↓
Route Function
      ↓
Response
      ↓
Middleware (can modify response)
      ↓
Client
'''

'''
Request arrives.

Middleware executes.

Middleware calls:


    await call_next(request)

FastAPI runs the endpoint:


    @app.get("/")
    async def say_hi():
    ...

Endpoint returns a response.

Response comes back to middleware.

Middleware stores it in response.
'''