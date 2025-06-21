from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import cv2

def detect_scenes(video_path):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=30.0))

    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager)
    scenes = scene_manager.get_scene_list()

    cap = cv2.VideoCapture(video_path)
    frames = []
    for i, (start, end) in enumerate(scenes):
        cap.set(cv2.CAP_PROP_POS_FRAMES, start.get_frames())
        ret, frame = cap.read()
        frame_path = f"scene_{i}.jpg"
        cv2.imwrite(frame_path, frame)
        frames.append(frame_path)
    cap.release()
    return frames
