from typing import List
from fastapi import WebSocket
from json import dumps
from rq.registry import FinishedJobRegistry, StartedJobRegistry

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[(str, WebSocket)] = []

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections.append((client_id, websocket))

    def disconnect(self, websocket: WebSocket, client_id: str, queue):
        for job in queue.jobs:
            if str(job.args[1]) == str(client_id):
                print('found job', job.id)
                finished_job_registry = FinishedJobRegistry(queue=queue)
                started_job_registry = StartedJobRegistry(queue=queue)
                if job in finished_job_registry.get_job_ids() or job in started_job_registry.get_job_ids():
                    print('removing job', job.id)
                    job = queue.fetch_job(job.id)
                    if job:
                        print('canceling job', job.id)
                        job.cancel()
        self.active_connections.remove((client_id, websocket))

    async def send_text_update(self, id: str, client_id: str, url: str, text: str, content_type: str):
        for (client, websocket) in self.active_connections:
            if str(client) == str(client_id):
                await websocket.send_text(dumps({'id': id, 'text': text, 'url': url, 'content_type': content_type}))
