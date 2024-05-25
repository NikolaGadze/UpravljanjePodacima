import uuid
from datetime import timedelta, datetime
from redis import Redis

class SessionManager:
    def __init__(self, redis_client: Redis, session_expiry: timedelta):
        self.redis_client = redis_client
        self.session_expiry = session_expiry

    def create_session(self, user_id: str):
        session_id = str(uuid.uuid4())
        session_data = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        self.redis_client.setex(session_id, self.session_expiry, str(session_data))
        return session_id

    def get_session(self, session_id: str):
        session_data = self.redis_client.get(session_id)
        if session_data:
            return eval(session_data)
        return None

    def delete_session(self, session_id: str):
        self.redis_client.delete(session_id)

# Initialize the Redis client and session manager
from redis_config import redis_client  # Ensure redis_config.py is properly defined with redis_client

session_manager = SessionManager(redis_client, timedelta(hours=1))
