import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)  # Disable auto white balance
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)  # Adjust color temperature if supported
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Disable auto exposure
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)  # Adjust brightness
cap.set(cv2.CAP_PROP_CONTRAST, 0.5)  # Adjust contrast

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Codec for .mp4 files
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(
    "invisibility_cloak.mp4", fourcc, 20.0, (frame_width, frame_height)
)

# Capture the background
ret, background = cap.read()
if not ret:
    print("Failed to grab background")
    cap.release()
    cv2.destroyAllWindows()
    exit()

background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # # Define blue color range
    # lower_blue = np.array([100, 150, 0])
    # upper_blue = np.array([140, 255, 255])

    # # Create mask for blue areas
    # mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #     # Define improved blue color range
    # lower_blue = np.array([90, 50, 30])  # Expanded range for better detection
    # upper_blue = np.array([150, 255, 255])
    # lower_blue = np.array([90, 50, 60])  # Higher minimum value for the saturation and brightness
    # upper_blue = np.array([130, 255, 255])  # Narrow the range
    lower_blue = np.array([90, 50, 70])  # More defined lower bound to avoid dark areas
    upper_blue = np.array([130, 255, 255])  # Defined upper bound
    # Define the new HSV range around the blue-gray color #5c749a
    # lower_blue = np.array([100, 40, 40])  # Lower bound of HSV for #5c749a
    # upper_blue = np.array([140, 120, 180])  # Upper bound of HSV for #5c749a

    # Create mask for blue areas
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)  # Fill gaps

    # Optional: Smooth the mask
    # mask = cv2.GaussianBlur(mask, (15, 15), 0)


    # Replace blue areas with background
    mask_inv = cv2.bitwise_not(mask)
    background_resized = cv2.resize(background, (frame.shape[1], frame.shape[0]))
    non_blue_areas = cv2.bitwise_and(frame, frame, mask=mask_inv)
    background_areas = cv2.bitwise_and(
        background_resized, background_resized, mask=mask
    )

    result = cv2.add(non_blue_areas, background_areas)

    # Write the frame to the output video
    out.write(result)

    # Show the result in real-time
    cv2.imshow("Invisibility Cloak", result)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video writer and webcam
out.release()
cap.release()
cv2.destroyAllWindows()

print("Video saved as 'invisibility_cloak.mp4'")