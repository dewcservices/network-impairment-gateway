from app.services.interfaces.iprocess_service import IProcessService


class DebugProcessService(IProcessService):
    def run(self, cmd):
        print(cmd)
