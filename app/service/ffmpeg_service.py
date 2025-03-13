import asyncio

from app.exception.ffmpeg_error import FFMPEGError

class FFMPEGService:
    """
    FFMPEG Service class that is responsible for providing ffmpeg services to controllers.
    It achieves this functionality by making subprocess system calls.
    """
    @staticmethod
    async def try_get_ffmpeg_version():
        """
        Static helper method that gets the ffmpeg version from the stdout after a subprocess call.
        :returns: Result
        :raises FFMPEGError:
        """
        try:
            process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip() or "Unknown error"
                raise FFMPEGError(error_message)

            version_output = stdout.decode().splitlines() # Get the first line (version info)

            if not version_output:
                raise FFMPEGError("No output from ffmpeg")

            return version_output[0] # Return output

        except FileNotFoundError:
            raise FFMPEGError("Error: ffmpeg is not installed or not found in PATH")
        except Exception as e:
            return FFMPEGError(f"Unexpected error: {str(e)}")