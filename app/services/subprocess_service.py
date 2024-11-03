import subprocess

from app.exception.request_processing_exception import RequestProcessingException
from app.services.interfaces.iprocess_service import IProcessService


class SubprocessService(IProcessService):

    def run(self, cmd: str, error_check: bool = True):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(cmd)
        # Check if the command was successful
        if result.returncode != 0 and error_check:
            raise RequestProcessingException(
                status_code=500,
                detail=f"Command {cmd} failed with return code {result.returncode}.",
                stack_trace=f"Error: {result.stderr}",
            )
