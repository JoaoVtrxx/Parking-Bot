import cv2
import pickle
import pyrebase

config={  
  "apiKey": "AIzaSyB7OaNJAUcce0RkYV81AQB6wjdpShBXPso",
  "authDomain": "projetointegrador2-abfb0.firebaseapp.com",
  "projectId": "projetointegrador2-abfb0",
  "databaseURL": "https://projetointegrador2-abfb0-default-rtdb.firebaseio.com/",
 "storageBucket": "projetointegrador2-abfb0.appspot.com",
 "messagingSenderId": "344867624568",
  "appId": "1:344867624568:web:ac1ca07ece7fb43be6bf8d",
  "measurementId": "G-KQ0Z1YGR0M"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


cap = cv2.VideoCapture('input/parking.mp4')

with open('park_positions', 'rb') as f:
    park_positions = pickle.load(f)

font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Parking space parameters
width, height = 40, 19
full = width * height
empty = 0.22


def parking_space_counter(img_processed):
    global counter

    counter = 0
   
    for position in park_positions:
        x, y = position
         
         
        img_crop = img_processed[y:y + height, x:x + width]
        count = cv2.countNonZero(img_crop)

        ratio = count / full

        if ratio < empty:
            color = (0, 255, 0)
            counter += 1
        else:
            color = (0, 0, 255)

        cv2.rectangle(overlay, position, (position[0] + width, position[1] + height), color, -1)
        cv2.putText(overlay, "{:.2f}".format(ratio), (x + 4, y + height - 4), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        

      
       
      
while True:
    
    

    # Video looping
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    _, frame = cap.read()
    overlay = frame.copy()

    # Frame processing
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    parking_space_counter(img_thresh)

    alpha = 0.7
    frame_new = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    w, h = 220, 60
    cv2.rectangle(frame_new, (0, 0), (w, h), (255, 0, 255), -1)
    cv2.putText(frame_new, f"{counter}/{len(park_positions)}", (int(w / 10), int(h * 3 / 4)), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
  

    cv2.imshow('frame', frame_new)
    # cv2.imshow('image_blur', img_blur)
    # cv2.imshow('image_thresh', img_thresh)

    data = {"users" : {"estacionados": f"{counter}/{len(park_positions)}"}}
    database.set(data)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
