from core.environment_variables import FAST_SPEED, NORMAL_SPEED, LOWER_SPEED
from PySide6.QtCore import Slot, QObject, Signal

class Speed(QObject):
    global NORMAL_SPEED
    global FAST_SPEED
    global LOWER_SPEED
    __current_speed = NORMAL_SPEED
        
    @staticmethod
    def up_speed():
        if (Speed.__current_speed == FAST_SPEED): pass
        elif (Speed.__current_speed == NORMAL_SPEED): Speed.__current_speed = FAST_SPEED
        elif (Speed.__current_speed == LOWER_SPEED): Speed.__current_speed = NORMAL_SPEED
                
    @staticmethod
    def down_speed():
        if (Speed.__current_speed == FAST_SPEED): Speed.__current_speed = NORMAL_SPEED
        elif (Speed.__current_speed == NORMAL_SPEED): Speed.__current_speed = LOWER_SPEED
        elif (Speed.__current_speed == LOWER_SPEED): pass
            
    @staticmethod
    def get_current_speed():
        return Speed.__current_speed
        
sp = Speed()