from fastapi import APIRouter
from database.mission_db import MissionDB
from logs.logger_config import logger
from database.agent_db import AgentDB

mdb = MissionDB()
adb = AgentDB()
router = APIRouter()

@router.get('/reports/summary') # דוח כללי של המערכת
def reports():
    active = adb.count_active_agents()
    total = mdb.count_all_missions()
    _open = mdb.count_open_missions()
    completed = mdb.count_by_status("COMPLETED")
    failed = mdb.count_by_status("FAILED")
    critical = mdb.count_critical_missions()
    return {"active_agents_count": active,
            "total_missions": total,
            "open_missions": _open,
            "completed_missions": completed,
            "failed_missions": failed,
            "critical_missions": critical
            }

@router.get('/reports/missions-by-status') # משימות לפי סטטוס
def missions_by_status():
    _open = mdb.count_open_missions()
    in_progress = mdb.count_by_status("IN_PROGRESS")
    completed = mdb.count_by_status("COMPLETED")
    failed = mdb.count_by_status("FAILED")
    critical = mdb.count_critical_missions()
    return {
        "open": _open,
        "in_progress": in_progress,
        "completed": completed,
        "failed": failed,
        "critical": critical
    }

@router.get('/reports/top-agent') # הסוכן המצטיין (get_top_agent)
def top_agent():
    return mdb.get_top_agent()