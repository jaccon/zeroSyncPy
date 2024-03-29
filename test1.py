import os
import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def sync_files(websocket, path):
    monitored_directory = "syncFolder"
    initial_files = set(os.listdir(monitored_directory))

    try:
        async for message in websocket:
            logging.info(f"Mensagem recebida: {message}")
            if message == "sync":
                current_files = set(os.listdir(monitored_directory))
                changed_files = current_files - initial_files
                if changed_files:
                    logging.info("Changed file")
                    await websocket.send("changed")
                initial_files = current_files

    except websockets.exceptions.ConnectionClosedError:
        logging.error("Conexão fechada inesperadamente.")

start_server = websockets.serve(sync_files, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
