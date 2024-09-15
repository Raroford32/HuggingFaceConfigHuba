import os

def generate_workspace_command(model_name):
    workspace_url = "ws://localhost:5000/ws"  # Replace with actual WebSocket URL
    return f"python3 connect_to_workspace.py {workspace_url} {model_name}"
