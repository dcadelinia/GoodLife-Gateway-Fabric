from fastapi import FastAPI
app = FastAPI()
import os
import json
import yaml
import asyncio
import signal
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Response, status

app = FastAPI(title="GoodLife Gateway Fabric - Omni Service Core")

# Thread-safe lifecycle variable
LOOP_ACTIVE = True

# Pydantic schemas for data validation
class TelemetryPayload(BaseModel):
    route_uuid: str
    hardware_fault_condition: bool

def read_loop_blueprint():
    try:
        if os.path.exists("safe_state_loops.yaml"):
            with open("safe_state_loops.yaml", "r") as stream:
                return yaml.safe_load(stream)
    except Exception as parse_error:
        print(f"BASELINE ERROR: Failing to parse blueprint: {parse_error}")
    return None

async def continuous_state_orchestrator():
    global LOOP_ACTIVE
    blueprint = read_loop_blueprint()
    
    print("Omni Service State loop tracking initialized successfully.")
    
    while LOOP_ACTIVE:
        try:
            # Simulate automation loop ticks
            await asyncio.sleep(0.5) 
            
            # Write dynamic loop heartbeat validation state out to temp space
            with open("/tmp/fabric_heartbeat.lock", "w") as lock_file:
                lock_file.write("ACTIVE")
            
            # Use interval configuration parameters if available, fallback to 5 seconds
            cooldown = blueprint["safety_limits"]["cooldown_interval_seconds"] if blueprint else 5
            await asyncio.sleep(cooldown)
            
        except asyncio.CancelledError:
            print("State orchestration loop safely intercepted and closed.")
            break
        except Exception as runtime_fault:
            print(f"Exception in state loop node: {runtime_fault}")
            await asyncio.sleep(5)

def intercept_sigterm(signum, frame):
    global LOOP_ACTIVE
    print("Fly.io SIGTERM detected. Executing graceful state conservation drain...")
    LOOP_ACTIVE = False

# Capture container infrastructure lifecycle termination triggers
signal.signal(signal.SIGTERM, intercept_sigterm)

@app.on_event("startup")
async def register_background_matrices():
    asyncio.create_task(continuous_state_orchestrator())

@app.get("/")
def baseline_handshake():
    return {
        "status": "ONLINE",
        "fabric_verification": "SUCCESS",
        "subsystems": {
            "omni_service": "OPERATIONAL"
        }
    }

@app.get("/healthz")
def platform_health_gate(response: Response):
    # Verifies both HTTP visibility and underlying async task loop state health
    if os.path.exists("/tmp/fabric_heartbeat.lock") and LOOP_ACTIVE:
        return {"status": "HEALTHY", "matrix_loop": "SYNCHRONIZED"}
    
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "UNHEALTHY", "matrix_loop": "DE-SYNCHRONIZED"}
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

# Note: If 'app = FastAPI()' or similar is already at the top of omni.py,
# do not duplicate it. Just make sure the code below references your app instance name.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

class FramerContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.post("/")
async def handle_framer_submission(form_data: FramerContactForm):
    try:
        print(f"New submission from {form_data.name} ({form_data.email})")
        print(f"Message: {form_data.message}")
        return {
            "status": "SUCCESS", 
            "message": "Inquiry successfully securely routed into framework core."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        def send_email_notification(client_name: str, client_email: str, client_message: str):
    # ZenBusiness Specific Outbound SMTP Core Server Settings
    SMTP_SERVER = "mail.b.hostedemail.com"  
    SMTP_PORT = 465
    SENDER_EMAIL = "david@odynexaxis.biz" 
    
    # Enter your dedicated mailbox login password here
    SENDER_PASSWORD = "Galaways8896"  
    RECEIVER_EMAIL = "david@odynexaxis.biz"

    # Set up email headers and metadata
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"New Inquiry: {client_name} via Odynex Axis Gateway"

    body = f"""
    You have received a new contact submission from your website form:
    
    Name: {client_name}
    Email: {client_email}
    
    Message:
    ---------------------------------------------
    {client_message}
    ---------------------------------------------
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect using secure SMTP_SSL directly for ZenBusiness Port 465
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Notification email successfully dispatched.")
    except Exception as e:
        print(f"Failed to dispatch email alert: {str(e)}")
        
