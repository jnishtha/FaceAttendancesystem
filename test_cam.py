import cv2

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break

    cv2.imshow("Test Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
