from fastapi import FastAPI
from .database import engine, Base
from .routers import users, posts



app = FastAPI(title="LawVriksh Auth Service")




@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    

app.include_router(users.router)
app.include_router(posts.router)
