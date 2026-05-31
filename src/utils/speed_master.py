from core.environment_variables import FAST_SPEED, NORMAL_SPEED
from PySide6.QtCore import QObject

class Speed(QObject):
    global NORMAL_SPEED
    global FAST_SPEED
    __current_speed = NORMAL_SPEED
        
    @staticmethod
    def real_speed():
        Speed.__current_speed = NORMAL_SPEED
                
    @staticmethod
    def fast_speed():
        Speed.__current_speed = FAST_SPEED
            
    @staticmethod
    def get_current_speed():
        return Speed.__current_speed
        
sp = Speed()