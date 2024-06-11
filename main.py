import uvicorn
from fastapi import FastAPI

from trips import router as trips_router

app = FastAPI(root_path="/api/v1")


app.include_router(trips_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
