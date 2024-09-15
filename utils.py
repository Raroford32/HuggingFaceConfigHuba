import uuid
import os

def generate_workspace_command():
    # Generate a unique identifier for the server
    server_id = str(uuid.uuid4())
    
    # Create a command that includes the server ID
    command = f"python3 connect_to_workspace.py {server_id}"
    
    return server_id, command

def configure_tgi(websocket, model):
    # This function will be updated to use websocket instead of SSH
    # For now, we'll just return placeholder values
    tgi_address = "http://placeholder-address:8000"
    repair_log = []
    
    return tgi_address, repair_log
