from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import cv2
import imagehash
from PIL import Image

def detect_scenes(video_path, threshold=5):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=20.0))

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scenes = scene_manager.get_scene_list()

    cap = cv2.VideoCapture(video_path)

    unique_frames = []
    last_hash = None

    for i, (start, end) in enumerate(scenes):
        cap.set(cv2.CAP_PROP_POS_FRAMES, start.get_frames())
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert frame to PIL Image for hashing
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        current_hash = imagehash.average_hash(pil_img)

        # If it's the first frame or the hash is different enough, keep it
        if last_hash is None or (current_hash - last_hash) > threshold:
            frame_path = f"scene_{i}.jpg"
            cv2.imwrite(frame_path, frame)
            unique_frames.append(frame_path)
            last_hash = current_hash

    cap.release()
    return unique_frames
