from fastapi import APIRouter, HTTPException, status
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from logs.logger_config import logger
from pydantic import BaseModel

class NewMisson(BaseModel):
    title: str
    description: str
    location: str
    difficulty:int
    importance: int


router = APIRouter()
mdb = MissionDB()
adb = AgentDB()

@router.post('/missions')
def create_mission(data: NewMisson):
    logger.info("Starts running the create_mission")
    _data = data.model_dump()
    if not (1 <= _data["difficulty"] <= 10) or not (1 <= _data["importance"] <= 10):
        raise ValueError("Choose a number between 1 and 10")
    fun = mdb.create_mission(_data)
    if fun:
        logger.info("The operation was successful.")
        return {"message": "The operation was successful."}
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")


@router.get('/missions')
def all_mission():
    logger.info("Starts running the all_mission")
    fun = mdb.get_all_missions()
    if fun:
        logger.info("The operation was successful.")
        return fun
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")


@router.get('/missions/{id}') # משימה לפי ID
def mission_by_id(id: int):
    logger.info("Starts running the mission_by_id")
    fun = mdb.get_mission_by_id(id)
    if fun:
        logger.info("The operation was successful.")
        return fun
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")



@router.put('/missions/{id}/assign/{agent_id}')
def assign_mission(id: int, agent_id: int):
    logger.info("Starts running the assign_mission")
    agent = adb.get_agent_by_id(agent_id)
    if agent:
        if agent["is_active"] == True:
            all_mission_of_agent = mdb.get_open_missions_by_agent(agent_id)
            mission_by_id = mdb.get_mission_by_id(id)
            if mission_by_id:
                if mission_by_id["status"] == "NEW":
                    check_risk_level = mission_by_id["risk_level"]
                    if len(all_mission_of_agent) < 3:
                        if check_risk_level == "CRITICAL":
                            if agent["agent_rank"] == "Commander":
                                fun = mdb.assign_mission(id, agent_id)
                                if fun:
                                    logger.info("The operation was successful.")
                                    return {"message": "The operation was successful."}
                                logger.warning("The operation failed.")
                                return {"message": "The operation failed."}
                        fun = mdb.assign_mission(id, agent_id)
                        if fun:
                            logger.info("The operation was successful.")
                            return {"message": "The operation was successful."}
                        logger.warning("The operation failed.")
                        return {"message": "The operation failed."}
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Commander can handle critical missions")
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agent has reached maximum missions ")
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mission not available")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Agent is not active")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="agent not found")


@router.put('/missions/{id}/start') # התחלת משימה
def start_mission(id:int):
    logger.info("Starts running the start_mission")
    fun = mdb.update_mission_status(id, "IN_PROGRESS")
    if fun:
        logger.info("The operation was successful.")
        return {"message": "The operation was successful."}
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")


@router.put('/missions/{id}/complete') # סיום בהצלחה
def finish_mission(id:int):
    logger.info("Starts running the finish_mission")
    fun = mdb.update_mission_status(id, "COMPLETED")
    logger.info("The operation was successful.")
    if fun:
        logger.info("The operation was successful.")
        return {"message": "The operation was successful."}
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")


@router.put('/missions/{id}/fail') # סיום בכישלון
def failed_mission(id:int):
    logger.info("Starts running the failed_mission")
    fun = mdb.update_mission_status(id, "FAILED")
    logger.info("The operation was successful.")
    if fun:
        logger.info("The operation was successful.")
        return {"message": "The operation was successful."}
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")


@router.put('/missions/{id}/cancel') # ביטול משימה
def failed_mission(id:int):
    logger.info("Starts running the failed_mission")
    fun = mdb.update_mission_status(id, "CANCELLED")
    if fun:
        logger.info("The operation was successful.")
        return {"message": "The operation was successful."}
    logger.warning("The operation failed.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="id not found")

