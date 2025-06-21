from scene_detect import detect_scenes
from frame_caption import caption_frames
from summarize import generate_summary

video_path = "app/your_trip_videos.mp4"
scene_frames = detect_scenes(video_path)
captions = caption_frames(scene_frames)
summary = generate_summary(captions)

print("\n=== Trip Summary ===\n")
print(summary)
