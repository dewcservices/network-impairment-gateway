from app.services.interfaces.iprocess_service import IProcessService


class DebugProcessService(IProcessService):
    def call(cmd):
        print(cmd)
