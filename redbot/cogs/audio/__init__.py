from pathlib import Path
from aiohttp import ClientSession
import shutil
import asyncio

from .audio import Audio
from .manager import start_lavalink_server
from discord.ext import commands
from redbot.core.data_manager import cog_data_path

LAVALINK_BUILD_ID_URL = (
    "https://ci.fredboat.com/app/rest/buildTypes/"
    "id:Lavalink_Build/builds/status:SUCCESS/number"
)
LAVALINK_BUILD_URL = (
    "https://ci.fredboat.com/guestAuth/repository/"
    "download/Lavalink_Build/.lastSuccessful/Lavalink.jar"
)

LAVALINK_DOWNLOAD_DIR = cog_data_path(raw_name="Audio")
LAVALINK_JAR_FILE = LAVALINK_DOWNLOAD_DIR / "Lavalink.jar"

APP_YML_FILE = LAVALINK_DOWNLOAD_DIR / "application.yml"
BUNDLED_APP_YML_FILE = Path(__file__).parent / "application.yml"


async def download_lavalink(session):
    tmp_file = LAVALINK_DOWNLOAD_DIR / 'tmp.jar'
    with tmp_file.open(mode='wb') as f:
        async with session.get(LAVALINK_BUILD_URL) as resp:
            while True:
                chunk = await resp.content.read(512)
                if not chunk:
                    break
                f.write(chunk)
    tmp_file.replace(LAVALINK_JAR_FILE)


async def maybe_download_lavalink(loop, cog):
    jar_exists = LAVALINK_JAR_FILE.exists()
    current_build = await cog.config.current_build()

    async with ClientSession(loop=loop) as session:
        async with session.get(LAVALINK_BUILD_ID_URL) as resp:
            latest_build = int(await resp.text())

    if not jar_exists or current_build < latest_build:
        LAVALINK_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        with ClientSession(loop=loop) as session:
            await download_lavalink(session)
        await cog.config.current_build.set(latest_build)

    shutil.copyfile(str(BUNDLED_APP_YML_FILE), str(APP_YML_FILE))


async def setup(bot: commands.Bot):
    cog = Audio(bot)
    await maybe_download_lavalink(bot.loop, cog)
    await start_lavalink_server(bot.loop)

    async def _finish():
        await asyncio.sleep(10)
        await cog.init_config()
        bot.add_cog(cog)

    bot.loop.create_task(_finish())
