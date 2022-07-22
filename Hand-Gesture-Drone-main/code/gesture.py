import cv2
import mediapipe as mp
mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
hands = mpHands.Hands()


fwidth = 640
fheight = 480


def mean_hand_pos(hand_landmarks): # Function to find mean (x,y,z) position of the hand
    global fwidth, fheight

    idxs = [0, 1, 2, 5, 9, 13, 17]
    x_sum = 0
    y_sum = 0
    z_sum = 0
    for idx in idxs:
        x_sum += hand_landmarks[idx].x
        y_sum += hand_landmarks[idx].y
        z_sum += hand_landmarks[idx].z

    x_mean_norm = x_sum/len(idxs)
    y_mean_norm = y_sum/len(idxs)
    z_mean_norm = z_sum/len(idxs)

    x_mean = x_mean_norm * fwidth
    y_mean = y_mean_norm * fheight

    return int(x_mean), int(y_mean), z_mean_norm


def interp(x, in_min, in_max, out_min, out_max): # Arduino Map Function
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def gesture_control(cap):
    global fwidth, fheight

    x_out_mc = 0
    y_out_mc = 0
    z_out_mc = 0
    x_out_sim = 0
    y_out_sim = 0
    z_out_sim = 0

    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            x_mean, y_mean, z_norm = mean_hand_pos(list(handLms.landmark))          # Find mean hand pos
            z_mean = int(z_norm*150)
            x_rel = x_mean - int(fwidth/2)                                # Shift origin to center of frame
            y_rel = -1*(y_mean - int(fheight/2))                          # Shift origin to center of frame
            x_out_mc = interp(x_rel, -320, 320, 0, 1)                     # Map position to (0,1) for microcontroller
            y_out_mc = interp(y_rel, -240, 240, 0, 1)                     # Map position to (0,1) for microcontroller
            z_out_mc = -1*(z_norm)
            x_out_sim = interp(x_rel, -320, 320, -1, 1)                   # Map position to (-1,1) for drone_sim
            y_out_sim = interp(y_rel, -320, 320, -1, 1)                   # Map position to (-1,1) for drone_sim
            z_out_sim = z_out_mc
            cv2.circle(img, (x_mean, y_mean), 10, (255, 0, 0), cv2.FILLED)  # Show mean position
            cv2.putText(img, f"X : {x_rel} Y : {y_rel} Z : {z_mean}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)   # Draw Landmarks

    cv2.line(img, (int(fwidth/2), 0), (int(fwidth/2), fheight), (0, 255, 0), 2) # Draw Gridlines
    cv2.line(img, (0, int(fheight/2)), (fwidth, int(fheight/2)), (0, 255, 0), 2)

    return img, x_out_mc, y_out_mc, z_out_mc, x_out_sim, y_out_sim, z_out_sim
