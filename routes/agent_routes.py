from fastapi import APIRouter
from database.agent_db import AgentDB
from logs.logger_config import logger
from pydantic import BaseModel

class NewAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: str

class UpdateAgent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    completed_missions: int | None = None
    failed_missions: int | None = None
    agent_rank: str | None = None


router = APIRouter()
adb = AgentDB()

@router.post('/agents')
def create_new_agent(data: NewAgent):
    logger.info("Starting to create an agent")
    _data = data.model_dump()
    fun = adb.create_agent(_data)
    if fun:
        logger.info("The agent was created successfully.")
        return {"message": "The agent was created successfully."}
    logger.warning("Agent creation failed.")
    return {"message": "Agent creation failed."}

@router.get('/agents')
def all_agents():
    logger.info("Starts running the all_agents")
    fun = adb.get_all_agents()
    if fun:
        logger.info("The operation was completed successfully.")
        return fun
    logger.warning("No agents for showing")
    return []

@router.get('/agents/{id}')
def get_agent_by_id(id: int):
    logger.info("Starts running the get_agent_by_id")
    fun = adb.get_agent_by_id(id)
    if fun:
        logger.info("The operation was completed successfully.")
        return fun
    logger.warning("No agent for showing")
    return {"message": "No agent for showing"}

@router.put('/agents/{id}')
def update_agent(id: int, data: UpdateAgent):
    logger.info("Starts running the update_agent")
    _data = data.model_dump(exclude_unset=True)
    fun = adb.update_agent(id, _data)
    if fun:
        logger.info("The operation was completed successfully.")
        return "The operation was successful."
    logger.warning("The operation failed.")
    return "The operation failed."


@router.put('/agents/{id}/deactivate')
@router.get('/agents/{id}/performance')