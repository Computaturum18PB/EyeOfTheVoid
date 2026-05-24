from core.environment_variables import FAST_SPEED, NORMAL_SPEED, LOWER_SPEED
from PySide6.QtCore import Slot, QObject, Signal

class Speed(QObject):
    speed_switch = Signal()
    __current_speed = NORMAL_SPEED
        
    @staticmethod
    def up_speed():
        if (Speed.__current_speed == FAST_SPEED): pass
        elif (Speed.__current_speed == NORMAL_SPEED): Speed.__current_speed = FAST_SPEED
        elif (Speed.__current_speed == LOWER_SPEED): Speed.__current_speed = NORMAL_SPEED
        else: print("Неизвестная скорость")
                
    @staticmethod
    def down_speed():
        if (Speed.__current_speed == FAST_SPEED): Speed.__current_speed = NORMAL_SPEED
        elif (Speed.__current_speed == NORMAL_SPEED): Speed.__current_speed = LOWER_SPEED
        elif (Speed.__current_speed == LOWER_SPEED): pass
        else: print("Неизвестная скорость")
            
    @staticmethod
    def get_speed():
        return Speed.__current_speed
            
    @Slot()
    def switch_speed(self, key):
        if (key == "+"):
            self.up_speed()
        if (key == "-"):
            self.down_speed()
        self.speed_switch.emit()
        
sp = Speed()