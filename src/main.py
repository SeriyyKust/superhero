import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI()
request_key: str = "(Cr_},%b5y@!S-#Tq|^@K74iA|PiG,4eYr@<="rl-woD%N!?]/$s]wX:_HuOmM*"


@app.get("/test")
async def test_handler():
    response = requests.get(url, json={"key": request_key})
    if response.status_code == 200:
        return JSONResponse(
            status_code=200,
            content={
                "message": "ok"
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "message": "error"
            }
        )
