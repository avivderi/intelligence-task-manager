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
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
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
def assign_mission(m_id, a_id) # משייכת משימה לסוכן
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

# הוראות הרצה
```bash
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```