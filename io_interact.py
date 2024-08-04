from abc import ABC
from abc import abstractmethod


class IOInteractBase(ABC):
    def __init__(self):
        self.process = None
        self.prompt: str = None
        self.newline: str = None

    @abstractmethod
    def start(self):
        """このメソッドはサブクラスで実装する必要があります。"""
        pass

    @abstractmethod
    def stop(self):
        """このメソッドはサブクラスで実装する必要があります。"""
        pass

    @abstractmethod
    def wait_for(self, expect, timeout_sec: float = 3.0) -> str:
        pass

    @abstractmethod
    def run_command(
            self,
            cmd: str = "",
            expect: str = "",
            timeout_sec: float = 0.2,
            attempts: int = 1) -> str:
        pass
