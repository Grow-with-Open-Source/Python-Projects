
### 3. **Add Comments in Code**

Adding comments in your code can help explain complex sections and improve readability.

**Example:**
```python
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (required by Mediapipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to obtain pose landmarks
    results = pose_detector.process(frame_rgb)

    # Draw landmarks on the frame (optional for visualization)
    draw_landmarks_on_image(frame, results)

    # Extract 3D landmarks
    landmark_positions_3d = read_landmark_positions_3d(results)
    if landmark_positions_3d is not None:
        # Send landmark positions to Unity via UDP
        data = json.dumps(landmark_positions_3d.tolist())  # Convert to JSON format
        sock.sendto(data.encode('utf-8'), server_address)  # Send data to Unity
        print(f'3D Landmarks: {landmark_positions_3d}')  # Optional: Print landmarks to console

    # Display the frame with landmarks drawn
    cv2.imshow('Real-Time 3D Pose Estimation', frame)

    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
