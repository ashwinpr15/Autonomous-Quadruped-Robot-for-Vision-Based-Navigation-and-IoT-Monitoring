import cv2
import numpy as np

def make_chunks(edge_array, size_of_chunk):
    """Divides detected edges into chunks to analyze clear paths."""
    chunks = []
    for i in range(0, len(edge_array), size_of_chunk):
        chunks.append(edge_array[i:i + size_of_chunk])
    return chunks

def navigate():
    cap = cv2.VideoCapture(0)
    step_size = 5
    
    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. Preprocessing (Bilateral Filter for noise reduction)
        blur = cv2.bilateralFilter(frame, 9, 40, 40)
        
        # 2. Edge Detection (Canny)
        edges = cv2.Canny(blur, 50, 100)
        
        height, width = edges.shape
        edge_array = []

        # 3. Vertical Scan (Simulated depth sensing)
        for j in range(0, width, step_size):
            pixel = (j, 0)
            for i in range(height-5, 0, -1):
                if edges.item(i, j) == 255:
                    pixel = (j, i)
                    break
            edge_array.append(pixel)

        # 4. Decision Logic (Chunk Analysis)
        num_chunks = 3
        chunk_size = int(len(edge_array) / num_chunks)
        chunks = make_chunks(edge_array, chunk_size)
        
        avg_distances = []
        for chunk in chunks:
            y_vals = [y for (x, y) in chunk]
            avg_y = int(np.average(y_vals))
            avg_distances.append(avg_y)

        # Simple Navigation Logic
        # NOTE: Navigation decisions are printed for clarity / logging.
        # In a full deployment, these conditions would trigger the corresponding
        # functions in 'locomotion.py' to drive the servos.
        center_dist = avg_distances[1]
        if center_dist > 250: # Threshold for "Close Obstacle"
            if avg_distances[0] < 310:
                print("Action: Turn Left")
            else:
                print("Action: Turn Right")
        else:
            print("Action: Move Forward")

        if cv2.waitKey(1) & 0xFF == 27: break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    navigate()
