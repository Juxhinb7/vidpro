import asyncio

class FFMPEGController:
    @staticmethod
    async def get_ffmpeg_version():
        version = await FFMPEGController.__try_get_ffmpeg_version_from_subprocess()
        return { "ffmpeg_version": version }

    @staticmethod
    async def __try_get_ffmpeg_version_from_subprocess() -> str:
        try:
            process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip() or "Unknown error"
                return f"Error: {error_message}"

            version_output = stdout.decode().splitlines() # Get the first line (version info)

            return version_output[0] if version_output else "Error: No output from ffmpeg"

        except FileNotFoundError:
            return "Error: ffmpeg is not installed or not found in PATH"
        except Exception as e:
            return f"Unexpected error {str(e)}"