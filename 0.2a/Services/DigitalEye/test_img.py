import torch
import cv2
import numpy as np





#This was the test bench for the detection script. It just grabs the janky AI made image of some dude and people walking down the road.
#Nothing more, just an early test before the live feed.





model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def detect_humans(image_path):
    img = cv2.imread(image_path)

    #convert BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(img_rgb)
    results.print()

    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    #draw boxes
    n = len(labels)
    x_shape, y_shape = img.shape[1], img.shape[0]
    for i in range(n):
        row = cord[i]
        if labels[i] == 0:  #0 person
            x1, y1, x2, y2, conf = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape), row[4]
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)  #draw
            cv2.putText(img, f'Human {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    #show img
    cv2.imshow('Human detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#PATH FOR TEST IMAGE
detect_humans('Test.png')
