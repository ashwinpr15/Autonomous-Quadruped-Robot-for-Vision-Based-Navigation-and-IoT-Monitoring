import argparse

import cv2
import numpy as np

STEP_SIZE = 5            # scan every 5th column
NUMBER_OF_CHUNKS = 3     # left, centre, right
OBSTACLE_ROW = 250       # centre edge lower than this row = obstacle is close
LEFT_RIGHT_SPLIT = 310   # x position that separates "left" from "right"


def make_chunks(edge_array, size_of_chunk):
    """Divides detected edge points into 3 chunks (Left, Center, Right)."""
    chunks = []
    for i in range(0, len(edge_array), size_of_chunk):
        chunks.append(edge_array[i:i + size_of_chunk])
    return chunks


def find_edges(frame):
    """Bilateral filter keeps edges sharp but removes noise; Canny finds the edges."""
    blur = cv2.bilateralFilter(frame, 9, 40, 40)
    return cv2.Canny(blur, 50, 100)


def scan_columns(edges, step_size=STEP_SIZE):
    """Bottom-up scan: for every 5th column, the first edge pixel is the nearest obstacle."""
    height, width = edges.shape
    edge_array = []
    for j in range(0, width, step_size):
        pixel = (j, 0)  # Default if no edge found (far away)
        for i in range(height - 5, 0, -1):
            if edges.item(i, j) == 255:
                pixel = (j, i)
                break
        edge_array.append(pixel)
    return edge_array


def decide(edge_array):
    """
    Turns the scanned edge points into a direction, following Chapter 6 of the report.
    Returns (action, chunk_averages) where each average is [y, x].
    """
    if len(edge_array) <= NUMBER_OF_CHUNKS:
        return "Forward", []
    size_of_chunk = int(len(edge_array) / NUMBER_OF_CHUNKS)
    avg_of_chunk = []
    for chunk in make_chunks(edge_array, size_of_chunk):
        if not chunk:
            continue
        # Average Y-coordinate (distance) and X-coordinate for this chunk
        avg_y = int(np.average([y for (x, y) in chunk]))
        avg_x = int(np.average([x for (x, y) in chunk]))
        avg_of_chunk.append([avg_y, avg_x])

    if len(avg_of_chunk) < 2:
        return "Forward", avg_of_chunk
    if avg_of_chunk[1][0] > OBSTACLE_ROW:  # centre obstacle is close
        # The farthest point has the smallest Y (highest up in the image)
        farthest_point = min(avg_of_chunk, key=lambda c: c[0])
        return ("Left" if farthest_point[1] < LEFT_RIGHT_SPLIT else "Right"), avg_of_chunk
    return "Forward", avg_of_chunk


def annotate(frame, action, avg_of_chunk):
    """Draws a line from the bottom centre to each chunk average, as in Fig 6.5 of the report."""
    height, width = frame.shape[:2]
    for k, (y, x) in enumerate(avg_of_chunk):
        colour = (0, 255, 0) if k == 1 else (0, 200, 255)
        cv2.line(frame, (width // 2, height), (x, y), colour, 3)
    cv2.putText(frame, f"Move {action}", (12, 36), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    return frame


def navigate(camera_index=0):
    """Live loop on the robot: camera frame -> edges -> decision. ESC exits."""
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        action, chunks = decide(scan_columns(find_edges(frame)))
        print(f"Action: Move {action}")
        cv2.imshow("navigation", annotate(frame, action, chunks))
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


def run_on_image(path, out_path):
    """Runs the same pipeline on a still photo, so it can be tried on any computer."""
    frame = cv2.imread(path)
    if frame is None:
        raise SystemExit(f"Could not read {path}")
    action, chunks = decide(scan_columns(find_edges(frame)))
    cv2.imwrite(out_path, annotate(frame, action, chunks))
    print(f"Action: Move {action}  (annotated image saved to {out_path})")
    return action


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Camera-based obstacle avoidance")
    parser.add_argument("--image", help="run on a still image instead of the live camera")
    parser.add_argument("--out", default="navigation-output.jpg", help="where to save the annotated image")
    args = parser.parse_args()
    if args.image:
        run_on_image(args.image, args.out)
    else:
        navigate()
