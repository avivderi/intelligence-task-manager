from database.db_connection import DB as db
from database.agent_db import AgentDB

agent_db = AgentDB()

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

    def create_mission(self, data):
        risk_level = self.calculte_risk_level(data)
        value = list(data.values())
        value.append(risk_level)
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO missions (title, description, location, difficulty, importance, risk_level) VALUES (%s, %s, %s, %s, %s, %s)",
            tuple(value)
        )
        db.conn.commit()
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
        return all_missions if all_missions else None

    def get_mission_by_id(self, id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id = %s", (id,))
        missions_by_id = cursor.fetchone()
        cursor.close()
        return missions_by_id if missions_by_id else None
    
    def assign_mission(self, mission_id, agent_id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET assigned_agent_id = %s, status = 'ASSIGNED' WHERE id = %s", (agent_id, mission_id))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        return is_update

    def update_mission_status(self, id, status):
        cursor = db.conn.cursor(dictionary=True)
        mission = self.get_mission_by_id(id)
        if (mission["status"] == "ASSIGNED" and status == "IN_PROGRESS") or (mission["status"] == "IN_PROGRESS" and status in ('FAILED', 'COMPLETED')) or (mission["status"] == "NEW" and status == "CANCELLED"):
            cursor.execute("UPDATE missions SET status = %s WHERE id = %s", (status, id))
            db.conn.commit()
            is_update = cursor.rowcount > 0
            cursor.close()
            return is_update

    def get_open_missions_by_agent(self, id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id = %s AND status IN ('ASSIGNED', 'IN_PROGRESS')", (id,))
        all_missions = cursor.fetchall()
        cursor.close()
        return all_missions if all_missions else []

    def count_all_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM missions")
        count_missions = cursor.fetchone()
        cursor.close()
        return count_missions["count"] if count_missions else 0

    def count_by_status(self, status):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM missions WHERE status = %s", (status,))
        count_by_status = cursor.fetchone()
        cursor.close()
        return count_by_status["count"] if count_by_status else 0

    def count_open_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM missions WHERE status = 'ASSIGNED' OR status = 'IN_PROGRESS'")
        count_open_mission = cursor.fetchone()
        cursor.close()
        return count_open_mission["count"] if count_open_mission else 0

    def count_critical_missions(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM missions WHERE risk_level = 'CRITICAL'")
        count_critical = cursor.fetchone()
        cursor.close()
        return count_critical["count"] if count_critical else 0

    def get_top_agent(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC")
        id_agent = cursor.fetchone()
        agent = agent_db.get_agent_by_id(id_agent)
        cursor.close()
        return agent if agent else None
