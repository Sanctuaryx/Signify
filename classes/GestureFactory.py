import classes.BaseGesture as BaseGesture
from classes.AbstractGestureFactory import AbstractGestureFactory
import classes.StaticGesture as StaticGesture
import classes.DynamicGesture as DynamicGesture

class GestureFactory(AbstractGestureFactory):
    
    def create_static_gesture(self, id, name, left_hand: StaticGesture.Hand, right_hand: StaticGesture.Hand):
        return StaticGesture.StaticGesture(left_hand, right_hand, id, name)
    
    def create_static_gesture(self, left_hand: StaticGesture.Hand, right_hand: StaticGesture.Hand):
        return StaticGesture.StaticGesture(left_hand, right_hand)
    
    def create_dynamic_gesture(self, id, name, left_hand: DynamicGesture.Hand, right_hand: DynamicGesture.Hand):
        return DynamicGesture.DynamicGesture(left_hand, right_hand, id, name)
    
    def create_dynamic_gesture(self, left_hand: DynamicGesture.Hand, right_hand: DynamicGesture.Hand):
        return DynamicGesture.DynamicGesture(left_hand, right_hand)
