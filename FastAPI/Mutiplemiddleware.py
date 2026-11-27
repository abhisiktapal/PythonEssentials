from fastapi import FastAPI, Request
import time
import uuid

app = FastAPI()

# Middleware 1: Request Logger
@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"[REQUEST] {request.method} {request.url.path}")

    response = await call_next(request)

    print(f"[RESPONSE] Status={response.status_code}")

    return response


# Middleware 2: Request Timer
@app.middleware("http")
async def measure_time(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start
    print(f"[TIME] {process_time:.3f}s")

    return response


# Middleware 3: Request ID
@app.middleware("http")
async def request_id(request: Request, call_next):
    req_id = str(uuid.uuid4())[:8]

    response = await call_next(request)

    response.headers["X-Request-ID"] = req_id

    print(f"[ID] {req_id}")

    return response


@app.get("/")
async def home():
    return {"message": "Home"}


@app.get("/users")
async def users():
    return {"users": ["Tom", "Jerry"]}


@app.post("/users")
async def create_user():
    return {"created": True}

'''Suppose you hit: GET /users. The flow will be :

Request-ID Middleware
    ↓
Timer Middleware
    ↓
Logger Middleware
    ↓
users() endpoint
    ↓
Logger Middleware resumes
    ↓
Timer Middleware resumes
    ↓
Request-ID Middleware resumes
'''

'''
Think of middlewares like nested wrappers:
Middleware3{}
    Middleware2(
        Middleware1(
            Route
        )
    )
)
'''

'''
Output:
    [REQUEST] GET /users
    [RESPONSE] Status=200
    [TIME] 0.001s
    [ID] 4af12c9d
'''

'''
If asked:
Why use middleware instead of putting print statements in every endpoint?

Answer:
Middleware executes for every request (GET, POST, PUT, DELETE, etc.), 
so common tasks like logging, authentication, timing, request tracking, and error handling can be written once and 
automatically applied to all endpoints. This avoids code duplication and makes debugging easier.
'''