from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Replace with the actual origin of your HTML page
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/process_string/")
async def process_string_route(data: dict):
    print("test")
    url = data.get("input_string")

    return {"processed_string": processed_string}
