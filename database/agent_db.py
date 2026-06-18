from database.db_connection import DB as db

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
        return all_agent if all_agent else None

    def get_agent_by_id(self, id):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id = %s", (id,))
        agent_by_id = cursor.fetchone()
        cursor.close()
        return agent_by_id if agent_by_id else None

    def update_agent(self, id, data):
        items = [f"{key} = %s" for key in data.keys()]
        values = list(data.values())
        values.append(id)
        query = f"UPDATE agents SET {', '.join(items)} WHERE id = %s"
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute(query, tuple(values))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        
    def deactivate_agent(self, id: int):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s", (id,))
        db.conn.commit()
        is_update = cursor.rowcount > 0
        cursor.close()
        return is_update


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
        items = cursor.fetchone()
        cursor.close()
        completed = int(items["completed_missions"])
        failed = int(items["failed_missions"])
        total = completed + failed
        if total != 0:
            success_rate = (completed / total) * 100
            return {"completed": completed, "failed": failed, "total": total, "success_rate": success_rate}
        return {"completed": completed, "failed": failed, "total": total, "success_rate": 0}

    def count_active_agents(self):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS count FROM agents WHERE is_active = TRUE")
        result = cursor.fetchone()
        cursor.close()
        return result["count"] if result else 0
    