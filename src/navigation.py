import cv2
import numpy as np

def make_chunks(edge_array, size_of_chunk):
    """Divides detected edge points into 3 chunks (Left, Center, Right)."""
    chunks = []
    for i in range(0, len(edge_array), size_of_chunk):
        chunks.append(edge_array[i:i + size_of_chunk])
    return chunks

def navigate():
    """
    Main Navigation Loop.
    Logic: Canny Edge -> Vertical Scan -> Chunk Average -> Decision
    Reference: Project Report Page 3.
    """
    cap = cv2.VideoCapture(0)
    step_size = 5

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. Preprocessing
        # Use Bilateral filter to keep edges sharp but remove noise
        blur = cv2.bilateralFilter(frame, 9, 40, 40)
        edges = cv2.Canny(blur, 50, 100)

        height, width = edges.shape
        edge_array = []

        # 2. Vertical Scan (Bottom-Up)
        # Scans every 5th column to find the first "edge" (obstacle)
        for j in range(0, width, step_size):
            pixel = (j, 0) # Default if no edge found (far away)
            for i in range(height-5, 0, -1):
                if edges.item(i, j) == 255:
                    pixel = (j, i)
                    break
            edge_array.append(pixel)

        # 3. Chunking Logic
        number_of_chunks = 3
        if len(edge_array) > number_of_chunks:
            size_of_chunk = int(len(edge_array) / number_of_chunks)
            chunks = make_chunks(edge_array, size_of_chunk)

            avg_of_chunk = []
            for chunk in chunks:
                if not chunk: continue
                # Calculate average Y-coordinate (distance) for this chunk
                y_vals = [y for (x, y) in chunk]
                x_vals = [x for (x, y) in chunk]
                avg_y = int(np.average(y_vals))
                avg_x = int(np.average(x_vals))
                avg_of_chunk.append([avg_y, avg_x])

            # 4. Decision Making (Page 4 Logic)
            if len(avg_of_chunk) >= 2:
                forward_edge_y = avg_of_chunk[1][0] # Center chunk Y

                # Visual Debugging
                cv2.line(frame, (int(width/2), height), (avg_of_chunk[1][1], avg_of_chunk[1][0]), (0, 255, 0), 3)

                # Logic: If center obstacle is closer than Y=250
                if forward_edge_y > 250:
                    # Find the "farthest" point (minimum Y value means higher up in image)
                    farthest_point = min(avg_of_chunk, key=lambda x: x[0])

                    if farthest_point[1] < 310: # If farthest point is on Left
                        print("Action: Move Left")
                    else:
                        print("Action: Move Right")
                else:
                    print("Action: Move Forward")

        if cv2.waitKey(1) & 0xFF == 27: # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    navigate()
