from datetime import datetime
from app.db.base import users_collection
from app.schemas.user import UserCreate, UserInDB
from app.services.email import send_welcome_email
from fastapi import BackgroundTasks

async def create_user(user: UserCreate, background_tasks: BackgroundTasks) -> UserInDB:
    # Prepare user data for database
    user_dict = user.model_dump()
    user_dict["created_at"] = datetime.utcnow()
    
    # Insert into database
    result = users_collection.insert_one(user_dict)
    
    # Add welcome email to background tasks
    background_tasks.add_task(
        send_welcome_email,
        user_name=user.name,
        user_email=user.email
    )
    
    return UserInDB(
        id=str(result.inserted_id),
        **user_dict
    )