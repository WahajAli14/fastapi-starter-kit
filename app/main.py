from typing import Dict

import uvicorn
from auth.auth_routes import auth_router
from fastapi import FastAPI
from routes.item_routes import router as item_router
from routes.rabbitmq_routes import router as rabbitmq_router
from routes.user_routes import router as user_router
from routes.sql_user_routes import router as sql_user_routes 

app = FastAPI()
app.include_router(item_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, tags=["users"])
app.include_router(rabbitmq_router, tags=["rabbitmq"])
app.include_router(sql_user_routes, tags=["SQL Users"])


@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Hello World from FastAPI!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str | None = None) -> Dict:
    return {"item_id": item_id, "query_param": query_param}


# Run the app using Uvicorn if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
