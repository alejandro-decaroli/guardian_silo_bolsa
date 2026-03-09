from abc import ABC, abstractmethod

class INotificatorService(ABC):
    """ Interfaz para servicios de notificación """
    @abstractmethod
    def send(self, message: str) -> None:
        """ Envía una notificación"""
        pass

