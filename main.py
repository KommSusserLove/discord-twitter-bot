import discord
from discord import app_commands

import yt_dlp
import os
import asyncio
from pathlib import Path

TOKEN = "MTU0NDA5NTY0MDA5MzU4OTYwNQ.GjvW6I.4G5U3d7HPmkAZhNvHNTnuq0t0JxFWBtZPO---8"

DOWNLOAD_FOLDER = Path("downloads")

DOWNLOAD_FOLDER.mkdir(exist_ok=True)


def download_video(url):
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(DOWNLOAD_FOLDER / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        video_path = Path(
            ydl.prepare_filename(info)
        )

    return video_path



class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()

        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(
            self,
            allowed_contexts=app_commands.AppCommandContext(
                guild=True,
                dm_channel=True,
                private_channel=True
            ),
            allowed_installs=app_commands.AppInstallationType(
                guild=True,
                user=True
            )
        )

    async def setup_hook(self):
        synced = await self.tree.sync()

        print(f"Comandos sincronizados: {len(synced)}")

        for command in synced:
            print(f"  - /{command.name}")

client = MyClient()


@client.tree.command(
    name="twitter",
    description="Descarga un video de Twitter/X"
)
@app_commands.allowed_installs(
    guilds=True,
    users=True
)
@app_commands.allowed_contexts(
    guilds=True,
    dms=True,
    private_channels=True
)
@app_commands.describe(url="URL del tweet")
async def twitter(
    interaction: discord.Interaction,
    url: str
):

    await interaction.response.defer(
        thinking=True
    )

    try:

        video_path = await asyncio.to_thread(
            download_video,
            url
        )

        await interaction.followup.send(
            file=discord.File(video_path)
        )

        os.remove(video_path)

    except Exception as e:

        await interaction.followup.send(
            f"❌ Ocurrió un error:\n`{str(e)}`"
        )



client.run(TOKEN)