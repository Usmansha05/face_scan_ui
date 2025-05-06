import tkinter as tk
from tkinter import messagebox
import face_recognition
import cv2
import os
import time
import csv

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir('known_faces'):
    if filename.endswith(('.jpg', '.png')):
        image_path = os.path.join('known_faces', filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)
        if encoding:  # make sure encoding is not empty
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

# GUI setup
window = tk.Tk()
window.title("Aditya University - Face Attendance App")
window.geometry("600x400")
window.configure(bg="#111111")  # Dark background for a more modern look

# Title
title = tk.Label(window, text="Aditya University", font=("Helvetica", 32, "bold"), bg="#111111", fg="#00FFFF", pady=20)
title.pack()

# Subtitle
subtitle = tk.Label(window, text="Face Attendance System", font=("Helvetica", 20), bg="#111111", fg="#FFFFFF")
subtitle.pack(pady=10)

# Output Label
output_label = tk.Label(window, text="", font=("Helvetica", 16), bg="#111111", fg="#00FF00")
output_label.pack(pady=20)

# Button styles
style = {
    "bg": "#FF00FF",  # Pink background
    "fg": "#111111",  # Black text
    "font": ("Helvetica", 16, "bold"),
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "padx": 20,
    "pady": 10,
    "activebackground": "#FF80FF",  # Lighter pink when active
    "activeforeground": "#111111",
    "cursor": "hand2"
}

def mark_attendance(name):
    # Write the name and time to a CSV file for attendance
    try:
        with open('attendance.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, time.strftime("%Y-%m-%d %H:%M:%S")])
        print(f"Attendance marked for {name}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        messagebox.showerror("Error", "Failed to mark attendance.")

def recognize_faces(known_face_encodings, known_face_names):
    video_capture = cv2.VideoCapture(0)
    
    # Check if the camera is opened correctly
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        messagebox.showerror("Error", "Failed to open webcam.")
        return

    face_found = False  # Flag to stop the loop after recognizing a face
    name = "Unknown"

    while True:
        # Capture a frame from the video feed
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Find all face locations and encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop over each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                # Mark attendance
                mark_attendance(name)
                face_found = True  # Face found, exit the loop after recognition

                # Display the name of the recognized person
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Show the frame with the face location and name
        cv2.imshow('Video', frame)

        # If we have found a face and marked attendance, break the loop
        if face_found:
            time.sleep(2)  # Wait for 2 seconds before closing the webcam
            break

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    video_capture.release()
    cv2.destroyAllWindows()

    return name  # Return the name detected

def start_attendance():
    output_label.config(text="Scanning...")
    name = recognize_faces(known_face_encodings, known_face_names)
    if name and name != "Unknown":
        output_label.config(text=f"Welcome, {name}!")
    else:
        output_label.config(text="Face not recognized.")

# Button with hover effects
def on_enter(event):
    start_button.config(bg="#FF80FF")

def on_leave(event):
    start_button.config(bg="#FF00FF")

start_button = tk.Button(window, text="Start Attendance", command=start_attendance, **style)
start_button.pack(pady=30)

start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# Running the GUI
window.mainloop()
