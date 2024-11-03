from app.services.interfaces.iprocess_service import IProcessService


class DebugProcessService(IProcessService):
    def run(self, cmd, error_check: bool = True):
        print(cmd)
