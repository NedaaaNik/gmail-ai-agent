
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google import genai
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] 

def authenticate_gmail():
    """Handles the OAuth2 login flow securely."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def get_recent_emails(service, max_results=20):
    """Fetches the subject and snippet of the last N emails."""
    print(f"Fetching last {max_results} emails...")
    
    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    messages = results.get('messages', [])

    email_data = []
    
    if not messages:
        print("No emails found.")
        return []

    for msg in messages:
        try:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt.get('payload', {})
            headers = payload.get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            snippet = txt.get('snippet', '') 
            
            email_data.append(f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n")
        except Exception as e:
            print(f"Skipping an email due to error: {e}")
            continue

    return email_data

def analyze_with_gemini(email_text):
    """Sends the email data to Gemini for summarization."""
    print("Sending data to Gemini...")
    
    # Initialize the new Client
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    You are an executive assistant. I am providing you with my last 20 emails.
    
    YOUR TASK:
    1. Identify the 3 most important items that require my attention.
    2. Ignore newsletters, spam, or automated receipts unless they are high-value.
    3. Provide a bulleted summary.
    
    EMAILS:
    {email_text}
    """
    
    # Call the model (Gemini 2.5 Flash)
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    return response.text

if __name__ == '__main__':
    try:
        # 1. Login to Gmail
        service = authenticate_gmail()
        
        # 2. Get Data
        emails = get_recent_emails(service, max_results=20)
        
        if emails:
            email_blob = "\n---\n".join(emails)
            
            # 3. Analyze
            summary = analyze_with_gemini(email_blob)
            print("\n" + "="*30)
            print("   EXECUTIVE SUMMARY   ")
            print("="*30 + "\n")
            print(summary)
        else:
            print("No emails to analyze.")
            
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")