import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from app.core.config import settings

# Setup Jinja2 environment for email templates
template_dir = Path(__file__).parent.parent / "templates"
env = Environment(loader=FileSystemLoader(str(template_dir)))

async def send_welcome_email(user_name: str, user_email: str):
    """Send welcome email to new users using SMTP"""
    try:
        # Get the template
        template = env.get_template("welcome_email.html")
        
        # Render the HTML
        html_content = template.render(
            user_name=user_name,
            app_name="Relaii",
            login_url=f"{settings.FRONTEND_URL}/login"
        )
        
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>"
        msg['To'] = user_email
        msg['Subject'] = f"Welcome to Relaii, {user_name}!"
        
        # Attach the HTML content
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to the SMTP server
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if not settings.SMTP_SSL:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return True
        
    except Exception as e:
        print(f"Error sending welcome email: {str(e)}")
        return False

import smtplib
# test function
import smtplib
from app.core.config import settings

async def test_email_configuration():
    """Test email configuration and connection"""
    try:
        # Test SMTP Connection
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            print("1. SMTP connection successful")
            
            if not settings.SMTP_SSL:
                server.starttls()
                print("2. TLS started successfully")
            
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print("3. SMTP login successful")
            
            return True
    except Exception as e:
        print(f"Email configuration test failed: {str(e)}")
        return False
    

# using resend for testing purposes
# import httpx
# from app.core.config import settings
# from pathlib import Path
# from jinja2 import Environment, FileSystemLoader

# # Setup Jinja2 environment for email templates
# template_dir = Path(__file__).parent.parent / "templates"
# env = Environment(loader=FileSystemLoader(str(template_dir)))

# async def send_welcome_email(user_name: str, user_email: str):
#     """Send welcome email using Resend"""
#     try:
#         # Get the template
#         template = env.get_template("welcome_email.html")
        
#         # Render the HTML
#         html_content = template.render(
#             user_name=user_name,
#             app_name="Relaii",
#             login_url=f"{settings.FRONTEND_URL}/login"
#         )

#         # Prepare the email data
#         email_data = {
#             "from": f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM_ADDRESS}>",
#             "to": user_email,
#             "subject": f"Welcome to Relaii, {user_name}!",
#             "html": html_content
#         }

#         # Send using Resend API
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 "https://api.resend.com/emails",
#                 json=email_data,
#                 headers={
#                     "Authorization": f"Bearer {settings.RESEND_API_KEY}",
#                     "Content-Type": "application/json"
#                 }
#             )
            
#             print(f"Resend API Response: {response.status_code}")
#             print(f"Response body: {response.text}")
            
#             if response.status_code == 200:
#                 return True
#             else:
#                 print(f"Failed to send email. Status: {response.status_code}")
#                 return False

#     except Exception as e:
#         print(f"Error sending welcome email: {str(e)}")
#         return False