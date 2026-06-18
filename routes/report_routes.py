from fastapi import APIRouter

router = APIRouter()

@router.get('/reports/summary') # דוח כללי של המערכת
@router.get('/reports/missions-by-status') # משימות לפי סטטוס
@router.get('/reports/top-agent') # הסוכן המצטיין (get_top_agent)