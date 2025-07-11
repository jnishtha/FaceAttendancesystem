from dotenv import load_dotenv
import face_recognition
import os
import cv2
import numpy as np
from datetime import datetime
import psycopg2
import csv

def start_attendance(update_log_callback=None, update_table_callback=None):
    if update_log_callback:
        update_log_callback("[INFO] Entry marked for XYZ")
    if update_table_callback:
        update_table_callback("Nishtha", "18:50:57", "Entry")

    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user =DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        print("[INFO] Connected to PostgreSQL database successfully")
    except Exception as e:
        print("[ERROR] Could not connect to database",e)
        exit()


    # Path to folder with known faces
    KNOWN_FACES_DIR = 'known_faces'

    # Delete corrupted CSV file if exists
    # if os.path.exists("attendance_log.csv"):
    #     os.remove("attendance_log.csv")
    #     print("[INFO] Old attendance_log.csv deleted for clean export.")

    # Lists to store known encodings and names
    known_encodings = []
    known_names = []
    print("[INFO] Loading known faces")

    # Load known face encodings
    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith(('.jpg', '.png')):
            image_path = os.path.join(KNOWN_FACES_DIR, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)
            else:
                print(f"[WARNING] No face found in {filename}")


    # Dictionary to store recent actions and their timestamps
    recent_actions = {}  # Format: { "Name": {"last_entry": datetime, "last_exit": datetime} }
    COOLDOWN_SECONDS = 60  # Prevent re-logging within 60 seconds

    # Start webcam
    video = cv2.VideoCapture(0)
    print("[INFO] Starting webcam... Press 'q' to quit.")

    if not video.isOpened():
        print("[ERROR] Cannot open webcam")
        exit()

    # print("[INFO] Starting webcam... Press 'q' to quit.")
    while True:
        ret, frame = video.read()
        if not ret:
            print("[ERROR] Failed to grab frame.")
            break

        # Resize frame to 1/4 size for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        # rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB

        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            name = "Unknown"
            if face_distances.size > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]

                    # inserting attendance into postgresql
                    now = datetime.now()
                    today_date= now.date()
                    current_time=now.time()
                    last_action = recent_actions.get(name, {})
                    # Check if attendance record exists for today
                    
                    cursor.execute(
                        "SELECT id, entry_time, exit_time, date FROM attendance WHERE name=%s ORDER BY id DESC LIMIT 1",
                        (name,)
                    )
                    record = cursor.fetchone()

                    if record is None or record[2] is not None and record[3] ==today_date:
                        last_entry = last_action.get("last_entry")
                        if not last_entry or(now - last_entry).total_seconds()>COOLDOWN_SECONDS:

                            cursor.execute(
                                "INSERT INTO attendance (name, date, entry_time) VALUES (%s, %s, %s)",
                                (name, today_date, current_time)
                            )

                            print(f"[INFO] Entry marked for {name} at {now.strftime('%H:%M:%S')}.")
                            if name not in recent_actions:
                                recent_actions[name] = {}
                                recent_actions[name] = {"last_entry": now}
                        else:
                            print(f"[INFO] Skipped duplicate entry for {name}.")
                        
                    elif record[2] is None and record[3] ==today_date:
                        last_exit = last_action.get("last_exit")
                        if (not last_exit or (now-last_exit).total_seconds() > COOLDOWN_SECONDS) :
                            cursor.execute(
                                "UPDATE attendance SET exit_time=%s WHERE id=%s",
                                (current_time, record[0])
                            )
                            print(f"[INFO] Exit marked for {name} at {now.strftime('%H:%M:%S')}.")
                            if name not in recent_actions:
                                recent_actions[name] = {}
                            recent_actions[name]["last_exit"] = now
                        # else:
                        #      print(f"[INFO] Skipped duplicate entry for {name}.")


                        # Calculate and display time spent
                            cursor.execute(
                            "SELECT entry_time, exit_time FROM attendance WHERE id=%s",
                            (record[0],)
                            )
                            updated_record = cursor.fetchone()
                            if updated_record and updated_record[0] and updated_record[1]:
                            # record_date = record[3] 
                                entry_dt = datetime.combine(today_date, updated_record[0])
                                exit_dt = datetime.combine(today_date, updated_record[1])
                                duration = exit_dt - entry_dt
                                print(f"[INFO] {name} spent {str(duration)} in total today.")

                                cursor.execute("UPDATE attendance SET duration = %s WHERE id = %s", (duration, record[0]))

                                # def export_attendance_to_csv(filename ="attendance_export.csv"):
                                try:
                                    with open("attendance_log.csv", mode="a", newline="") as file:
                                        writer = csv.writer(file)
                                        if file.tell() == 0:
                                            writer.writerow(["Name", "Date", "Entry Time", "Exit Time", "Duration"])
                                        writer.writerow([
                                            name,
                                            today_date.strftime("%Y-%m-%d"),
                                            updated_record[0].strftime("%H:%M:%S"),
                                            updated_record[1].strftime("%H:%M:%S"),
                                            str(duration)
                                        ])

                                        print("[INFO] Attendance exported to attendance_log.csv")
                                except Exception as e:
                                    print("[ERROR] Failed to export CSV:", e)
                        else:
                            print(f"[INFO] Skipped duplicate exit for {name}.")
                    connection.commit()

            # Scale face location back to original frame size
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Show the result
        cv2.imshow("Face Recognition Attendance", frame)
        key = cv2.waitKey(1)
        print(f"[DEBUG] Key pressed: {key}")
        if key & 0xFF == ord('q'):
            print("[INFO] 'q' pressed. Exiting...")
            break


    # Release resources
    video.release()
    cv2.destroyAllWindows()
    cursor.close()
    connection.close()

    key = cv2.waitKey(1)
   
