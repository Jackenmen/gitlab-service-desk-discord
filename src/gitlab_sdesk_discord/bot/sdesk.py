import asyncio
import json

from discord.ext import commands


class SDesk(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ipc_task = asyncio.create_task(self.ipc_server())

    def cog_unload(self) -> None:
        self.ipc_task.cancel()

    async def ipc_server(self) -> None:
        # could use UNIX socket instead here
        server = await asyncio.start_server(self.ipc_handler, "127.0.0.1", 8889)

        async with server:
            await server.serve_forever()

    async def ipc_handler(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        raw_data = await reader.read()
        payload = json.loads(raw_data.decode())
        writer.close()
        # do stuff with `payload`
