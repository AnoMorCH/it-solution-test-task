from .running_line_clip import RunningLineClip
from moviepy.editor import CompositeVideoClip
import os


class TestRunningLineClip:
    TEXT = "Hello world!"

    rlc = RunningLineClip(TEXT)
    clip = rlc.create()
    success_output_std_arg = rlc.send_to_client(clip)
    success_output_diff_arg = rlc.send_to_client(clip)
    failure_output = rlc.send_to_client(clip, "hahaha")
    file_names = [f for f in os.listdir() if os.path.isfile(f)]

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

    def test_crated_video_name_with_std_fmt(self) -> None:
        fmt = "mp4"
        assert f"{self.rlc.FILE_NAME}.{fmt}" in self.file_names

    def test_crated_video_name_with_diff_fmt(self) -> None:
        fmt = "webm"
        self.rlc.send_to_client(self.clip, fmt)
        assert f"{self.rlc.FILE_NAME}.{fmt}" in self.file_names

