import asyncio

from fastapi import  status
from fastapi.responses import JSONResponse

from app.schema.result import Result


class FFMPEGController:
    @staticmethod
    async def get_ffmpeg_version():
        """
        Handler that outputs the ffmpeg version.
        """
        result = await FFMPEGController.__try_get_ffmpeg_version_from_subprocess()

        if result.has_error:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=result.model_dump())

        return JSONResponse(status_code=status.HTTP_200_OK, content=result.model_dump())

    @staticmethod
    async def __try_get_ffmpeg_version_from_subprocess() -> Result:
        """
        Static helper method that gets the ffmpeg version from the stdout after a subprocess call.
        """
        try:
            process = await asyncio.create_subprocess_exec(
            'ffmpeg', '-version', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip() or "Unknown error"
                return Result(output=error_message, has_error=True)

            version_output = stdout.decode().splitlines() # Get the first line (version info)

            if version_output:
                return Result(output=version_output[0], has_error=False)
            else:
                return Result(output="Error: No output from ffmpeg", has_error=True)

        except FileNotFoundError:
            return Result(output="Error: ffmpeg is not installed or not found in PATH", has_error=True)
        except Exception as e:
            return Result(output=f"Unexpected error {str(e)}", has_error=True)