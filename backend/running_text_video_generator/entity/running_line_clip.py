from moviepy.editor import TextClip, ColorClip, CompositeVideoClip
from typing import Callable
from backend.settings import MEDIA_PATH
from .message import Message
import os
import shutil


class RunningLineClip:
    """The running line of some text generating the result as video 100x100 of
    three seconds."""

    OX_SPAN, OY_SPAN = 100, 100
    BACKGROUND_SIZE_PX = (OX_SPAN, OY_SPAN)
    TEXT_FONT_SIZE = 10
    DURATION_SEC = 3
    ACCEPTABLE_FMTS = ["mp4", "webm"]
    COLOR_RGB = [50, 50, 50]
    VIDEO_FPS = 24
    TEXT_COLOR = "white"

    SUCCESS_MSG = "success"
    WRONG_FMT_MSG = "The video format is wrong. Only MP4 and WEBM are acceptable."

    FILE_NAME = "running-link"

    def __init__(self, text: str) -> None:
        self.text = text

    def create(self) -> CompositeVideoClip:
        """Create a clip based on the given text."""
        txt_clip = TextClip(self.text, color=self.TEXT_COLOR, fontsize=self.TEXT_FONT_SIZE)
        movement_oxy_func = self.__generate_movement_oxy_func(txt_clip.size[0])
        txt_clip = txt_clip.set_position(movement_oxy_func).set_duration(self.DURATION_SEC)
        color_clip = ColorClip(size=self.BACKGROUND_SIZE_PX, duration=self.DURATION_SEC, color=self.COLOR_RGB)
        return CompositeVideoClip([color_clip, txt_clip])
    
    def send_to_client(self, clip: CompositeVideoClip, fmt: str = "mp4") -> dict:
        """Send the video of the clip to the client."""
        try:
            self.__validate_fmt(fmt)
            video_path = f"{MEDIA_PATH}/{self.FILE_NAME}.{fmt}"
            clip.set_duration(self.DURATION_SEC).write_videofile(video_path, fps=self.VIDEO_FPS)
            return Message(self.SUCCESS_MSG).get()
        except Exception as e:
            return Message(str(e)).get()
    
    def delete_saved_videos(func: Callable) -> None:
        def inner(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            shutil.rmtree(MEDIA_PATH)
            os.makedirs(MEDIA_PATH)
            return response
        return inner

    def __generate_movement_oxy_func(self, text_length_px: int) -> Callable:
        """Generate a function which makes movement from right to left showing 
        the whole message."""
        start_ox_pos = self.OX_SPAN
        step_ox_pos = (self.OX_SPAN + text_length_px) / self.DURATION_SEC
        return lambda t: ((start_ox_pos - t * step_ox_pos) , "center" )
        
    def __validate_fmt(self, fmt: str) -> None:
        """Validate the format of the created clip (only mp4 and webm are
        available). If something is wrong, raise an exception."""
        if fmt not in ["mp4", "webm"]:
            raise AttributeError(self.WRONG_FMT_MSG)
