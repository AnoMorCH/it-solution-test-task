from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from running_text_video_generator.entity.running_line_clip import RunningLineClip, Message
from running_text_video_generator.views import RunningLineClipView
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


class RunningLineClipViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.bad_request = self.factory.get("/running_text_video_generator")
        self.text_request = self.factory.get("/running_text_video_generator?text=Hello world")
        self.text_fmt_request = self.factory.get("/running_text_video_generator?text=Hello world&fmt=webm")
        self.text_wrong_fmt_request = self.factory.get("/running_text_video_generator?text=Hello world&fmt=hahah")
        self.bad_response = RunningLineClipView.as_view()(self.bad_request)
        self.text_response = RunningLineClipView.as_view()(self.text_request)
        self.text_fmt_response = RunningLineClipView.as_view()(self.text_fmt_request)
        self.text_wrong_fmt_response = RunningLineClipView.as_view()(self.text_wrong_fmt_request)

    def test_type(self) -> None:
        assert type(self.bad_response) is HttpResponse
        assert type(self.text_response) is HttpResponse
        assert type(self.text_fmt_response) is HttpResponse
        assert type(self.text_wrong_fmt_response) is HttpResponse

    def test_http_code(self) -> None:
        assert self.bad_response.status_code == 400
        assert self.text_response.status_code == 200
        assert self.text_fmt_response.status_code == 200
        assert self.text_wrong_fmt_response.status_code == 400

    def test_content_type(self) -> None:
        assert self.bad_response["Content-Type"] == "application/json"
        assert self.text_response["Content-Type"] == "video/mp4"
        assert self.text_fmt_response["Content-Type"] == "video/webm"
        assert self.text_wrong_fmt_response["Content-Type"] == "application/json"

    def test_if_files_are_deleted(self) -> None:
        files_before_video_generator = [f for f in os.listdir(MEDIA_ROOT)]
        self.text_fmt_request = self.factory.get("/running_text_video_generator?text=Hello world&fmt=webm")
        files_after_video_generator = [f for f in os.listdir(MEDIA_ROOT)]
        assert len(files_before_video_generator) == 0
        assert len(files_after_video_generator) == 0
    