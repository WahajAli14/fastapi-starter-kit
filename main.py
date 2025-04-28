from fastapi import FastAPI
from typing import Dict
from routes.user_routes import router as user_router
from routes.item_routes import router as item_router
from auth.auth_routes import auth_router
import uvicorn

app = FastAPI()
app.include_router(item_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, tags=["users"])

@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello World from FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str | None = None) -> Dict:
    return {"item_id": item_id, "query_param": query_param}

# Run the app using Uvicorn if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)