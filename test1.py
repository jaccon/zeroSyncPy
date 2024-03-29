import os
import asyncio
import logging
import websockets

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def websocket_handler(websocket, path):
    if path == "/server":
        await handle_server(websocket)
    elif path == "/client":
        await handle_client(websocket)

async def handle_server(websocket):
    monitored_directory = "syncFolder"
    initial_files = set(os.listdir(monitored_directory))

    try:
        remote_address = websocket.remote_address[0]
        logging.info(f"Conectado com: {remote_address}")

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

async def handle_client(websocket):
    await websocket.send("Teste de conexão")
    response = await websocket.recv()
    logging.info(f"Resposta: {response}")

async def start_server():
    server = await websockets.serve(websocket_handler, "localhost", 8765)
    logging.info("Servidor WebSocket iniciado.")
    await server.wait_closed()

async def start_client():
    async with websockets.connect('ws://localhost:8765/server') as websocket:
        await handle_client(websocket)

if __name__ == "__main__":
    mode = input("Selecione 'A' para servidor ou 'B' para cliente: ").strip().upper()

    if mode == 'A':
        asyncio.get_event_loop().run_until_complete(start_server())
    elif mode == 'B':
        asyncio.get_event_loop().run_until_complete(start_client())
    else:
        print("Modo inválido. Use 'A' para servidor ou 'B' para cliente.")
