from django.test import TestCase
from running_text_video_generator.entity.running_line_clip import RunningLineClip
from backend.settings import MEDIA_ROOT
from moviepy.editor import CompositeVideoClip
import os

class RunningLineClipTestCase(TestCase):
    TEXT = "Hello world!"

    rlc = RunningLineClip(TEXT)
    clip = rlc.create()
    success_output_std_arg = rlc.send_to_client(clip)
    success_output_diff_arg = rlc.send_to_client(clip)
    failure_output = rlc.send_to_client(clip, "hahaha")

    def __get_file_names(self) -> list:
        """Get list of file names from media root."""
        return [f for f in os.listdir(MEDIA_ROOT)]

    def test_text(self) -> None:
        assert self.rlc.text == self.TEXT

    def test_output_type(self) -> None:
        assert type(self.clip) is CompositeVideoClip

    def test_success_msg_std_fmt(self) -> None:
        assert self.success_output_std_arg == {self.rlc.MSG_KEY: self.rlc.SUCCESS_MSG}

    def test_success_msg_diff_fmt(self) -> None:
        assert self.success_output_diff_arg == {self.rlc.MSG_KEY: self.rlc.SUCCESS_MSG}

    def test_wrong_fmt_output(self) -> None:
        assert self.failure_output != {self.rlc.MSG_KEY: self.rlc.SUCCESS_MSG}

    def test_created_video_name_with_std_fmt(self) -> None:
        fmt = "mp4"
        assert f"{self.rlc.FILE_NAME}.{fmt}" in self.__get_file_names()

    def test_created_video_name_with_diff_fmt(self) -> None:
        fmt = "webm"
        assert f"{self.rlc.FILE_NAME}.{fmt}" in self.__get_file_names()
