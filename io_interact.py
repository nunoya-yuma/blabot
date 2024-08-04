from abc import ABC
from abc import abstractmethod


class IOInteractBase(ABC):

    @abstractmethod
    def start(self):
        """このメソッドはサブクラスで実装する必要があります。"""
        pass

    @abstractmethod
    def stop(self):
        """このメソッドはサブクラスで実装する必要があります。"""
        pass

    @abstractmethod
    def run_command(
            self,
            cmd: str = "",
            expect: str = "",
            timeout_sec: float = 0.2,
            attempts: int = 1) -> str:
        pass
