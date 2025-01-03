import os
from openai import OpenAI
from app.core.config import settings
from app.db.base import chat_logs_collection
from datetime import datetime
import tiktoken
from bson import json_util
import json

# Initialize OpenAI client with explicit API key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def count_tokens(text: str) -> int:
    """Count tokens for a given text using tiktoken"""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    return len(encoding.encode(text))

async def generate_conversation(message: str, subject: str):
    # Store the user input
    # chat_logs_collection.insert_one({
    #     "message": message,
    #     "subject": subject,
    #     "timestamp": datetime.utcnow()
    # })
    
    # Construct the system message based on requirements
    system_message = f"""You are Relaii, a communication facilitator. Generate a natural conversation following these rules:

    1. Format: Use 'Relaii:' for the AI's messages and '{subject}:' for the subject's responses.
    2. Structure: 
       - Start with a neutral, casual opening (e.g., "How's your day going?")
       - Gradually transition to themes related to the input
       - End with a constructive, hopeful note
    3. Rules:
       - Never reveal or directly reference the user's input
       - Keep responses realistic and balanced
       - Don't use personal experiences or emotions for Relaii
       - Use "It seems" or "Sometimes people" instead of "I feel"
    
    Example format:
    Relaii: Hey, how's your day been going?
    {subject}: Pretty good, just busy with work.
    Relaii: Those busy days can add up. How have things been feeling overall?
    
    Keep the conversation between 10-12 messages total."""

    try:
        # Count tokens for input
        system_tokens = count_tokens(system_message)
        message_tokens = count_tokens(message)
        total_input_tokens = system_tokens + message_tokens
        
        # print(f"Token usage analysis:")
        # print(f"- System message tokens: {system_tokens}")
        # print(f"- User message tokens: {message_tokens}")
        # print(f"- Total input tokens: {total_input_tokens}")

        # Generate the conversation using OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Generate a conversation that subtly addresses this theme: {message}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        print(f"Response: {response}")
        
        # Parse the response into a structured conversation
        conversation = response.choices[0].message.content
        # Convert the conversation into a list of message objects
        messages = parse_conversation(conversation, subject)

        log_entry = {
            "subject": subject,
            "original_message": message,
            "timestamp": datetime.utcnow(),
            "conversation": json.loads(json_util.dumps(messages)),  # Convert to MongoDB-safe format
            "token_usage": {
                "system_tokens": system_tokens,
                "message_tokens": message_tokens,
                "total_input_tokens": total_input_tokens,
                "response_tokens": count_tokens(conversation)
            },
            "raw_response": conversation  # Store the raw response as well
        }

        # Insert into MongoDB
        result = chat_logs_collection.insert_one(log_entry)
        
        if not result.inserted_id:
            print("Warning: Failed to store conversation in database")

        return messages
    except Exception as e:
        print(f"Error generating conversation: {str(e)}")
        raise

def parse_conversation(conversation: str,  subject: str):
    """Parse the conversation text into a list of message objects."""
    messages = []
    lines = conversation.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or ':**' in line:  # Skip empty lines and incorrect formatting
            continue
            
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                speaker, content = parts[0].strip(), parts[1].strip()
                
                # Determine the role based on the speaker
                if speaker.lower() == "relaii":
                    role = "relaii"
                elif speaker.lower() == subject.lower():
                    role = subject.lower()
                else:
                    continue
                
                # Remove any asterisks or extra formatting
                content = content.strip('*').strip()
                
                if content:  # Only add if there's actual content
                    messages.append({
                        "role": role,
                        "content": content
                    })
    
    return messages