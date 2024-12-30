from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.user import UserCreate, UserInDB
from app.services.user import create_user

router = APIRouter()

@router.post("/join", response_model=UserInDB)
async def join_relaii(user: UserCreate, background_tasks: BackgroundTasks):
    try:
        new_user = await create_user(user, background_tasks)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from app.services.email import test_email_configuration, send_welcome_email
@router.post("/test-email")
async def test_email():
    """Test endpoint to verify email configuration"""
    # First test the configuration
    config_test = await test_email_configuration()
    if not config_test:
        raise HTTPException(status_code=500, detail="Email configuration test failed")
    
    # Try sending a test email
    test_result = await send_welcome_email(
        user_name="Test User",
        user_email="raoahsan110@gmail.com"  # Replace with your email
    )
    
    if not test_result:
        raise HTTPException(status_code=500, detail="Email sending test failed")
        
    return {"message": "Email configuration and sending test passed successfully"}