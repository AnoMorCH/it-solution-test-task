from django.test import TestCase
from running_text_video_generator.entity.running_line_clip import RunningLineClip, Message
from backend.settings import MEDIA_ROOT
from moviepy.editor import CompositeVideoClip
import os


class RunningLineClipTestCase(TestCase):
    TEXT = "Hello world!"

    rlc = RunningLineClip(TEXT)
    clip = rlc.create()

    def __get_file_names(self) -> list:
        """Get list of file names from media root."""
        return [f for f in os.listdir(MEDIA_ROOT)]

    def test_text(self) -> None:
        assert self.rlc.text == self.TEXT

    def test_output_type(self) -> None:
        assert type(self.clip) is CompositeVideoClip

    @RunningLineClip.delete_saved_videos
    def test_success_msg_std_fmt(self) -> None:
        success_output_std_arg = self.rlc.send_to_client(self.clip)
        assert success_output_std_arg == Message(self.rlc.SUCCESS_MSG).get()

    @RunningLineClip.delete_saved_videos
    def test_success_msg_diff_fmt(self) -> None:
        success_output_diff_arg = self.rlc.send_to_client(self.clip, "webm")
        assert success_output_diff_arg == Message(self.rlc.SUCCESS_MSG).get()

    @RunningLineClip.delete_saved_videos
    def test_wrong_fmt_output(self) -> None:
        failure_output = self.rlc.send_to_client(self.clip, "hahaha")
        assert failure_output != Message(self.rlc.SUCCESS_MSG).get()

    @RunningLineClip.delete_saved_videos
    def test_created_video_name_with_std_fmt(self) -> None:
        self.rlc.send_to_client(self.clip)
        assert f"{self.rlc.FILE_NAME}.mp4" in self.__get_file_names()

    @RunningLineClip.delete_saved_videos
    def test_created_video_name_with_diff_fmt(self) -> None:
        self.rlc.send_to_client(self.clip, "webm")
        assert f"{self.rlc.FILE_NAME}.webm" in self.__get_file_names()
