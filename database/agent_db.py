from db_connection import DB as db
from pydantic import BaseModel

class NewAgent(BaseModel):
    name: str
    specialty: str
    agent_rank: str

class UpdateAgent(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    completed_missions: int | None = None
    failed_missions: int | None = None
    agent_rank: str | None = None


class AgentDB:
    def create_agent(self, data: list):
        cursor = db.conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)", (data,))
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
        return agent_by_id if agent_by_id else []

    def update_agent(self, id: int, data: dict):
        cursor = db.conn.cursor(dictionary=True)
        items = [data.items()]

        cursor.execute("UPDATE agents SET (%s) WHERE id =")

    def deactivate_agent(self, id):
        pass

    def incremente_completed(self, id):
        pass

    def increment_failed(self, id):
        pass

    def get_agent_performance(self, id):
        pass

    def count_active_agents(self):
        pass