from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set

router = APIRouter(prefix="/ws", tags=["ws"])

active_connections: Set[WebSocket] = set()

@router.websocket("/leaderboard")
async def ws_leaderboard(ws: WebSocket):
    await ws.accept()
    active_connections.add(ws)
    try:
        while True:
            # Apenas manter a conexão viva; se quiser ping/pong, receber mensagens
            _ = await ws.receive_text()
    except WebSocketDisconnect:
        active_connections.discard(ws)

async def broadcast_leaderboard_update(payload: dict):
    # Envie para todos; ignore erros de sockets fechados
    dead = []
    for conn in active_connections:
        try:
            await conn.send_json(payload)
        except Exception:
            dead.append(conn)
    for d in dead:
        active_connections.discard(d)