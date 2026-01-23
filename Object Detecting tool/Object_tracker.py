import cv2
import numpy as np
import time
from ultralytics import YOLO
from collections import defaultdict

# =========================
# SIMPLE SORT TRACKER
# =========================
class SimpleSORT:
    """Lightweight SORT-style tracker"""

    def __init__(self, max_age=30, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.tracks = []
        self.track_id_counter = 0

    def iou(self, box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        intersection = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection

        return intersection / union if union > 0 else 0

    def update(self, detections):
        for track in self.tracks:
            track['age'] += 1
            track['hits'] = 0

        if detections and self.tracks:
            iou_matrix = np.zeros((len(detections), len(self.tracks)))
            for d, det in enumerate(detections):
                for t, trk in enumerate(self.tracks):
                    iou_matrix[d, t] = self.iou(det[:4], trk['bbox'])

            matched = set()
            for _ in range(min(len(detections), len(self.tracks))):
                max_iou = np.max(iou_matrix)
                if max_iou < self.iou_threshold:
                    break

                d, t = np.unravel_index(np.argmax(iou_matrix), iou_matrix.shape)
                self.tracks[t].update({
                    'bbox': detections[d][:4],
                    'confidence': detections[d][4],
                    'class_id': int(detections[d][5]),
                    'age': 0,
                    'hits': 1,
                    'total_hits': self.tracks[t]['total_hits'] + 1
                })
                matched.add(d)
                iou_matrix[d, :] = -1
                iou_matrix[:, t] = -1

            for d, det in enumerate(detections):
                if d not in matched:
                    self.tracks.append({
                        'id': self.track_id_counter,
                        'bbox': det[:4],
                        'confidence': det[4],
                        'class_id': int(det[5]),
                        'age': 0,
                        'hits': 1,
                        'total_hits': 1
                    })
                    self.track_id_counter += 1

        elif detections:
            for det in detections:
                self.tracks.append({
                    'id': self.track_id_counter,
                    'bbox': det[:4],
                    'confidence': det[4],
                    'class_id': int(det[5]),
                    'age': 0,
                    'hits': 1,
                    'total_hits': 1
                })
                self.track_id_counter += 1

        self.tracks = [t for t in self.tracks if t['age'] < self.max_age]
        return [t for t in self.tracks if t['total_hits'] >= self.min_hits]


# =========================
# MAIN DETECTOR
# =========================
class VisionTrackerX:
    def __init__(self, model='yolov8n.pt', conf=0.5):
        print("\nLoading AI Model:", model)
        self.model = YOLO(model)
        self.conf = conf
        self.tracker = SimpleSORT()
        self.history = defaultdict(list)
        self.colors = {}

    def color(self, tid):
        if tid not in self.colors:
            np.random.seed(tid)
            self.colors[tid] = tuple(map(int, np.random.randint(50, 255, 3)))
        return self.colors[tid]

    def process(self, frame, trails=True):
        start = time.time()
        results = self.model(frame, verbose=False)[0]

        detections = []
        if results.boxes:
            for b, c, cls in zip(
                results.boxes.xyxy.cpu().numpy(),
                results.boxes.conf.cpu().numpy(),
                results.boxes.cls.cpu().numpy()
            ):
                if c >= self.conf:
                    detections.append([*b, c, cls])

        tracks = self.tracker.update(detections)
        out = frame.copy()

        for trk in tracks:
            x1, y1, x2, y2 = map(int, trk['bbox'])
            tid = trk['id']
            cname = self.model.names[trk['class_id']]
            col = self.color(tid)

            cv2.rectangle(out, (x1, y1), (x2, y2), col, 2)
            label = f"{cname.upper()} | ID {tid}"
            cv2.putText(out, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, col, 2)

            center = ((x1 + x2)//2, (y1 + y2)//2)
            self.history[tid].append(center)
            self.history[tid] = self.history[tid][-25:]

            if trails and len(self.history[tid]) > 1:
                cv2.polylines(out, [np.array(self.history[tid])],
                              False, col, 2)

        fps = int(1 / (time.time() - start + 1e-6))
        hud = f"VISION TRACKER X | FPS: {fps} | Objects: {len(tracks)}"
        cv2.rectangle(out, (0, 0), (520, 35), (20, 20, 20), -1)
        cv2.putText(out, hud, (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 180), 2)

        return out

    def run(self, source=0):
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print("Camera / video not accessible.")
            return

        print("\nControls: Q = Quit | T = Trails")
        trails = True

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.process(frame, trails)
            cv2.imshow("VISION TRACKER X", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                trails = not trails

        cap.release()
        cv2.destroyAllWindows()


# =========================
# ENTRY POINT
# =========================
def main():
    print("=" * 65)
    print("        V I S I O N   T R A C K E R   X")
    print("   AI-Powered Real-Time Object Detection System")
    print("=" * 65)

    print("\nSelect Source:")
    print("1. Webcam")
    print("2. Video File")
    ch = input("Choice: ").strip()

    src = 0 if ch == '1' else input("Video path: ").strip()
    app = VisionTrackerX()
    app.run(src)


if __name__ == "__main__":
    main()
