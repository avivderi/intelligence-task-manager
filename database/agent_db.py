from db_connection import DB_connection
from pydantic import BaseModel

db = DB_connection()

class UpdateAgent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    completed_missions: int | None = None
    failed_missions: int | None = None
    agent_rank: str | None = None


class AgentDB:
    def create_agent(self, data: dict):
        value = list(data.values())
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)", tuple(value))
        db.conn.commit()
        row_id = cursor.lastrowid
        cursor.execute("SELECT * FROM agents WHERE id = %s", (row_id,))
        agent = cursor.fetchone()
        cursor.close()
        return agent

    def get_all_agents(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents")
        all_agent = cursor.fetchall()
        cursor.close()
        return all_agent if all_agent else []

    def get_agent_by_id(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        agent_by_id = cursor.fetchone()
        cursor.close()
        return agent_by_id if agent_by_id else None

    def update_agent(self, id: int, data: UpdateAgent):
        _data = data.model_dump(exclude_unset=True)
        items = [f"{key} = %s" for key in _data.keys()]
        values = list(_data.values())
        values.append(id)
        query = f"UPDATE agents SET {', '.join(items)} WHERE id = %s"
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute(query, tuple(values))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."

    def deactivate_agent(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s", (id,))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."


    def incremente_completed(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s", (id,))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."



    def increment_failed(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s", (id,))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        if is_update:
            return "The operation was successful."
        return "The operation failed."

    def get_agent_performance(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT completed_missions, failed_missions FROM agents WHERE id = %s", (id,))
        items = cursor.fetchall()
        cursor.close()
        total = int(items["completed_missions"])
        failed = int(items["failed_missions"])
        completed = total + failed
        if completed != 0:
            success_rate = (total / completed) * 100
            return {"total": total, "failed": failed, "completed": completed, "success_rate": success_rate}
        return {"total": total, "failed": failed, "completed": completed, "success_rate": 0}

    def count_active_agents(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM agents WHERE is_active = TRUE")
        result = cursor.fetchone()
        cursor.close()
        return result["count"] if result else 0
    

adb = AgentDB()