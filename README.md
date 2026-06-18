# intelligence-task-manager

# תיאור המערכת - רקע הפרוייקט ומטרתו
```text
יחידת מודיעין בשם ShadowNet זקוקה למערכת לניהול סוכנים ומשימות
המטרה של המערכת היא לנהל מול הדאטה בייס 2 טבלאות.
סוכנים.
משימות.
המערכת תאפשר להוסיף, לעדכן, ולמחוק סוכנים. ובנוסף לעדכן משימות חדשות, פעילות, וכאלה שכבר בוצעו... והכל בהתאם לרמת הסוכן והסיכון של המשימה.
```
# מבנה התיקיות
```text
intelligence-task-manager/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
|
├── routes/
│   ├── agent_routes.py
│   ├── mission_routes.py
│   └── report_routes.py
|
├── logs/
│   ├── app.log
│   ├── logger_config.py
|
├── README.md
├── requirements.txt
└── .gitignore
```

# מבנה הטבלאות
# agents
```text
id
name
specialty
is_active
completed_missions
failed_missions
agent_rank
```

# missions
```text
id
title
description
location
difficulty
importance
status
resk_level
assigned_agent_id
```

# הסבר על המחלקות
# DB_connection
```python
def get_connection() # מחזירה חיבור פעיל ל - MySql
def create_database() # יוצרת את intelligence_db אם לא קיים
def create_tables() # יוצרת את שתי הטבלאות אם לא קיימות
```

# AgentDB
```python
def create_agent(data) # יוצרת סוכן חדש ומחזירה את האובייקט של הסוכן
def get_all_agents() # מחזירה רשימת כל הסוכנים
def get_agent_by_id(id) # מחזירה סוכן אחד לפי ID, או None
def update_agent(id, data) # UPDATE לכל השורה (אין אפשרות לשנות ID)
def deactivate_agent(id) # מגדירה מצב סוכן ללא פעיל
def incremente_completed(id) # מעדכן את כמות המשימות שהושלמו 
def increment_failed(id) # מעדכן את כמות המשימות שנכשלו
def get_agent_performance(id) # מחזירה מילון עם המפתחות האלו (completed, failed, total, success_rate)
def count_active_agents() #מחזירה את מספר הסוכנים הפעילים 
```

# MissionDB
```python
def create_mission(data) # יצירת משימה חדשה ומחזירה את כל האובייקט
def get_all_missions() # מחזירה את כל המשימות
def get_mission_by_id(id) # מחזירה משימה אחת לפי ID, או None
def assign_mission(mission_id, agent_id) # משייכת משימה לסוכן
def update_mission_status(id, status) # משמשת לכל שינוי סטטוס
def get_open_missions_by_agent(id) # מחזירה משימות ASSIGNED/IN_PROGRESS של סוכן
def count_all_missions() # סה"כ משימות
def count_by_status(status) # סופרת לפי סטטוס מסוים
def count_open_missions() # סופרת משימות פתוחות
def count_critical_missions() # סופרת משימות CRITICAL
def get_top_agent() # הסוכן עם completed_missions הגבוה ביותר
```

# חוקי המערכת
```text
1: חייב להיות Junior / Senior / Commander — כל ערך אחר זורק שגיאה.

2: difficulty ו-importance חייבים להיות בין 1 ל-10 — אחרת שגיאה.

3: risk_level מחושב אוטומטית בעת יצירת משימה — המשתמש לא שולח אותו.

4: סוכן עם is_active=False לא יכול לקבל משימות.

5: סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.

6: אם risk_level=CRITICAL — רק סוכן בדרגת Commander יכול לקבל את המשימה.

7: ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.

8: ניתן להתחיל רק משימה בסטטוס ASSIGNED. לאחר: status=IN_PROGRESS.

9: ניתן לסיים רק משימה. IN_PROGRESS  ולשנות לסטטוס failed or completed

10: ניתן לבטל רק משימה בסטטוס NEW או ASSIGNED — אחרת שגיאה.
```

# רשימת Endpoints - מלאה
*agent_routes.py*
```python
@router.post('/agents') # יצירת סוכן חדש
@router.get('/agents') # כל הסוכנים
@router.get('/agents/{id}') # סוכן לפי ID
@router.put('/agents/{id}')# עדכון סוכן
@router.put('/agents/{id}/deactivate') # השבתת סוכן
@router.get('/agents/{id}/performance') # ביצועי סוכן
```

*mission_routes.py*
```python
@router.post('/missions') # צירת משימה
@router.get('/missions') # כל המשימות
@router.get('/missions/{id}') # משימה לפי ID
@router.put('/missions/{id}/assign/{agent_id}') # שיוך לסוכן (6 בדיקות מוסבר בהמשך)
@router.put('/missions/{id}/start') # התחלת משימה
@router.put('/missions/{id}/complete') # סיום בהצלחה
@router.put('/missions/{id}/fail') # סיום בכישלון
@router.put('/missions/{id}/cancel') # ביטול משימה
```

*report_routes.py*
```python
@router.get('/reports/summary') # דוח כללי של המערכת
@router.get('/reports/missions-by-status') # משימות לפי סטטוס
@router.get('/reports/top-agent') # הסוכן המצטיין (get_top_agent)
```

# זרימת המערכת
```text
The user enters the system through the server powered by FASTAPI. For example, the
user chooses to add an agent to the list... He enters - @router.post('/agents') which
activates the function - def create_agent(data) with the agent's details... The system
checks that all the data the user entered is correct according to the system settings
and the table settings. And if they are approved... the creation is successfully
created... and at the end the system returns the user the details of the newly created
agent... Another example - for assigning a task to an agent... The user enters -
@router.put('/missions/{id}/assign/{agent_id}') which runs a function -
def assign_mission(mission_id, agent_id).
and the system performs 6 checks to see
if the agent meets all the criteria for assigning a task:
1. If the task exists
2. If the agent exists
3. If the agent is active
4. If the agent does not have 3 tasks assigned to it (in progress, assigned)
5. If the task is defined as new
6. If the agent matches the task in the risk_level rating
And after everything is approved the system associates the task to the agent and updates the status to - Assigned
And at the end the system returns a success message to the user...
```

# הוראות הרצה
```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install fastapi[standard]
```

```bash
pip install mysql-connector-python
```

```bash
pip freeze -> requirements.txt
```