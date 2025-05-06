# attendance_main.py
import cv2
import face_recognition
import numpy as np

def recognize_faces(known_face_encodings, known_face_names):
    # Start the webcam
    video_capture = cv2.VideoCapture(0)  # 0 is for the default camera

    while True:
        # Capture a frame from the webcam
        ret, frame = video_capture.read()

        # Find all face locations and encodings in the current frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"  # Default to "Unknown" if no match is found

            # Check if we have a match
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Optionally mark attendance (could add to CSV here as well)
                print(f"Recognized: {name}")

                # Display the name on the frame
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()

    # Return the recognized name if any
    if name != "Unknown":
        return name
    else:
        return None
