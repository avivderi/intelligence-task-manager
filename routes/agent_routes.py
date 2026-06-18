from fastapi import APIRouter
from database.agent_db import adb
from logs.logger_config import logger
from pydantic import BaseModel

class NewAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: str

router = APIRouter()

@router.post('/agents')
def create_new_agent(data: NewAgent):
    logger.info("Starting to create an agent")
    _data = data.model_dump()
    fun = adb.create_agent(_data)
    if fun:
        logger.info("The agent was created successfully.")
        return {"message": "The agent was created successfully."}
    logger.info("Agent creation failed.")
    return {"message": "Agent creation failed."}



# @router.get('/agents')
# @router.get('/agents/{id}')
# @router.put('/agents/{id}')
# @router.put('/agents/{id}/deactivate')
# @router.get('/agents/{id}/performance')