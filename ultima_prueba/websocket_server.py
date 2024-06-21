import asyncio
import websockets
import json
from firebase_admin import db, credentials, initialize_app
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Firebase
DATABASE_URL = os.environ.get("DATABASE_URL")
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
initialize_app(cred, {"databaseURL": DATABASE_URL})

connected_clients = set()

async def send_updates():
    ref = db.reference("/Horarios/")
    async def listener(event):
        data = event.data
        print("Sending update to clients")
        if data:
            message = json.dumps(data)
            await asyncio.wait([client.send(message) for client in connected_clients])

    ref.listen(listener)

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await send_updates()

if __name__ == "__main__":
    asyncio.run(main())