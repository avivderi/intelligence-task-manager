from db_connection import DB as db
from pydantic import BaseModel
from agent_db import db as agent_db

class NewMisson(BaseModel):
    title: str
    description: str
    location: str
    difficulty:int
    importance: int

class FixInt(BaseModel):
    difficulty:int | None = None
    importance: int

class MissionDB:
    def calculte_risk_level(self, data: int):
        risk_level = (data["difficulty"] * 2) + data["importance"]
        if risk_level in range(0,10):
            level = "LOW"
        elif risk_level in range(10,18):
            level = "MEDIUM"
        elif risk_level in range(18, 25):
            level = "HIGH"
        elif risk_level >= 25:
            level = "CRITICAL"
        return level

    def create_mission(self, data: NewMisson):
        _data = data.model_dump()
        value = [v for v in _data.values()]
        risk_level = self.calculte_risk_level(_data)
        value.append(risk_level)
        if _data["difficulty"] or _data["importance"] not in range(1,11):
            raise TypeError ("Choose a number between 1 and 10")
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO missions (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)", (value,))
        row_id = cursor.lastrowid
        cursor.execute("SELECT * FROM missions WHERE id = %s", (row_id,))
        mission = cursor.fetchone()
        cursor.close()
        return mission

    def get_all_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        all_missions = cursor.fetchall()
        cursor.close()
        return all_missions if all_missions else []

    def get_mission_by_id(self, id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
        missions_by_id = cursor.fetchone()
        cursor.close()
        return missions_by_id if missions_by_id else None
    
    def assign_mission(self, mission_id, agent_id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET assigned_agent_id = %s WHERE id = %s", (agent_id, mission_id))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."

    def update_mission_status(self, id, status):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status, id))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."

    def get_open_missions_by_agent(self, id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id = %s", (id,))
        all_missions = cursor.fetchall()
        cursor.close()
        return all_missions if all_missions else []

    def count_all_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions")
        count_missions = cursor.fetchone()
        cursor.close()
        return count_missions if count_missions else 0

    def count_by_status(self, status):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status = %s", (status,))
        count_by_status = cursor.fetchone()
        cursor.close()
        return count_by_status if count_by_status else 0

    def count_open_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status = 'ASSIGNED' OR status = 'IN_PROGRESS'")
        count_open_mission = cursor.fetchone()
        cursor.close()
        return count_open_mission if count_open_mission else 0

    def count_critical_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) FROM missions WHERE risk_level = 'CRITICAL'")
        count_critical = cursor.fetchone()
        cursor.close()
        return count_critical if count_critical else 0

    def get_top_agent(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT assigned_agent_id FROM missions GROUP BY assigned_agent_id ORDER BY COUNT id DESC")
        id_agent = cursor.fetchone()
        agent = agent_db.get_agent_by_id(id_agent)
        cursor.close()
        return agent if agent else None

