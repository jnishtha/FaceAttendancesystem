import cv2
import face_recognition

video = cv2.VideoCapture(0)

while True:
    print("[DEBUG] Reading frame...")
    ret, frame = video.read()
    if not ret:
        break

    print("[DEBUG] Resizing...")
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = small_frame[:, :, ::-1]

    print("[DEBUG] Detecting faces...")
    try:
        # Comment out this line to test freezing
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        print(f"[DEBUG] Found {len(face_locations)} face(s)")
    except Exception as e:
        print(f"[ERROR] Face detection failed: {e}")
        continue

    print("[DEBUG] Showing window...")
    cv2.imshow("Freeze Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Quitting.")
        break

video.release()
cv2.destroyAllWindows()
