broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/1"
imports = ("app.video_processor", "app.training")
task_serializer = "pickle"
result_serializer = "pickle"
event_serializer = "json"
accept_content = ["pickle", "json"]
result_expires = 3600