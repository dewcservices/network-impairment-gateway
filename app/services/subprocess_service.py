import subprocess

from app.services.interfaces.iprocess_service import IProcessService


class SubprocessService(IProcessService):
    def call(cmd):
        subprocess.call(cmd)
