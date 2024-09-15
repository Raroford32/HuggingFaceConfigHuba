import sys
import asyncio
import websockets
import json
import psutil
import argparse
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

try:
    import pynvml
    pynvml.nvmlInit()
    has_gpu = True
except:
    has_gpu = False

async def send_server_info(websocket):
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        if has_gpu:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            gpu_memory = pynvml.nvmlDeviceGetMemoryInfo(handle).used / pynvml.nvmlDeviceGetMemoryInfo(handle).total * 100
        else:
            gpu_util = None
            gpu_memory = None
        
        server_info = {
            'type': 'server_info',
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'gpu_util': gpu_util,
            'gpu_memory': gpu_memory
        }
        
        await websocket.send(json.dumps(server_info))
        await asyncio.sleep(5)  # Send updates every 5 seconds

async def start_tgi_server(model, tokenizer):
    # Placeholder for TGI server setup
    # In a real implementation, you would start the TGI server here
    print(f"Starting TGI server with model: {model.config.model_type}")
    return "http://localhost:8000"  # Return a placeholder TGI server address

async def main():
    parser = argparse.ArgumentParser(description='Connect to TGI workspace and start server')
    parser.add_argument('workspace_url', help='WebSocket URL of the workspace')
    parser.add_argument('model_name', help='Name of the Hugging Face model to use')
    args = parser.parse_args()

    print(f"Connecting to workspace: {args.workspace_url}")
    print(f"Loading model: {args.model_name}")

    # Download and load the model
    model = AutoModelForCausalLM.from_pretrained(args.model_name)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    # Start the TGI server
    tgi_address = await start_tgi_server(model, tokenizer)
    print(f"TGI server started at: {tgi_address}")

    async with websockets.connect(args.workspace_url) as websocket:
        server_info_task = asyncio.create_task(send_server_info(websocket))
        
        try:
            await server_info_task
        except asyncio.CancelledError:
            print("Server info task cancelled")

if __name__ == "__main__":
    asyncio.run(main())
