from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from routes.agent_routes import router as agent_routes
from routes.mission_routes import router as mission_routes
from routes.report_routes import router as report_routes
from logs.logger_config import logger
from mysql.connector import errors as mysql_errors
from contextlib import asynccontextmanager
from database.db_connection import db

@asynccontextmanager
async def lifspen_app(app: FastAPI):
    db.connect()
    db.create_database()
    db.create_tables()
    yield
    db.close_db()

app = FastAPI(lifespan=lifspen_app)
app.include_router(agent_routes)
app.include_router(mission_routes)
app.include_router(report_routes)

@app.exception_handler(Exception)
def all_exception(requests: Request, e: Exception):
    logger.error(f"action failed: {str(e)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=f"action failed: {str(e)}"
    )
    
@app.exception_handler(mysql_errors.Error)
def exeption_mysql(req: Request, e: mysql_errors.Error):
    logger.error(f"Database action failed: {e.msg} (Code: {e.errno})")
    if e.errno == 1062:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "not found."}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Database error occurred: {e.msg}"}
    )

