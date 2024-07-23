from django.urls import path
from . import views


app_name = "running_text_video_generator"

urlpatterns = [
    path("running_text_video_generator/", views.RunningLineClipView.as_view())
]
