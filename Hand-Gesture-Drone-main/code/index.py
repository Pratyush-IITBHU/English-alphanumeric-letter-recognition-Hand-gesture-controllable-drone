import cv2
from gesture import gesture_control
from drone_sim import Drone
from arduino import Controller

cap = cv2.VideoCapture(0)
drone = Drone()             #Turn the drone_sim on
#controller = Controller()  #Turn the controller on

while True:

    frame, x_out_mc, y_out_mc, z_out_mc, x_out_sim, y_out_sim, z_out_sim = gesture_control(cap)  # Calculate Voltages and Actions corresponding to Gestures

    drone.show(x_out_sim, y_out_sim, z_out_sim)                 # Show drone sim

    #controller.analog_out(x_out_mc, y_out_mc, z_out_mc)        # Write voltages to microcontroller

    cv2.imshow("Gesture Control", frame)                        # Show the gesture frame

    k = cv2.waitKey(10)
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
#controller.close()
