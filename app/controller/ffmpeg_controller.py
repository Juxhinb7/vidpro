import asyncio

class FFMPEGController:
    @staticmethod
    async def get_ffmpeg_version():
        version = await FFMPEGController.__get_ffmpeg_version_from_subprocess()
        return { "ffmpeg_version": version }

    @staticmethod
    async def __get_ffmpeg_version_from_subprocess() -> str:
        process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        version_output = stdout.decode().splitlines()[0] # Get the first line (version info)

        return version_output