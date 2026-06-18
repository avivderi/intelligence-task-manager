from fastapi import APIRouter

router = APIRouter()

@router.post('/missions') # צירת משימה
@router.get('/missions') # כל המשימות
@router.get('/missions/{id}') # משימה לפי ID
@router.put('/missions/{id}/assign/{agent_id}') # שיוך לסוכן (6 בדיקות מוסבר בהמשך)
@router.put('/missions/{id}/start') # התחלת משימה
@router.put('/missions/{id}/complete') # סיום בהצלחה
@router.put('/missions/{id}/fail') # סיום בכישלון
@router.put('/missions/{id}/cancel') # ביטול משימה