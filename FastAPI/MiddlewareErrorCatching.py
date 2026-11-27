from fastapi import FastAPI, HTTPException, Request
import random
import string

app=FastAPI()

@app.middleware("http")
async def catch_errors(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

        raise

@app.get("/divide")
async def divide():
    return 10 / 0


''' 
When you do "http://127.0.0.1:portnumber/divide"

Log:

    [ERROR] ZeroDivisionError: division by zero

Without this middleware you may only see:

    500 Internal Server Error
'''