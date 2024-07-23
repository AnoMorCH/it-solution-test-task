from django.http import HttpResponse
from django.views.generic import View
from running_text_video_generator.entity.running_line_clip import RunningLineClip
from backend.settings import MEDIA_PATH
from wsgiref.util import FileWrapper
import json


class RunningLineClipView(View):
    def get(self, request) -> HttpResponse:
        text = request.GET.get("text")
        fmt = request.GET.get("fmt")

        rlc = RunningLineClip(text)

        if not text:
            output = {rlc.MSG_KEY: "The text cannot be empty."}
            return HttpResponse(json.dumps(output), content_type="application/json", status=400)
        
        clip = rlc.create()
        fmt = "mp4" if fmt is None else fmt
        output = rlc.send_to_client(clip, fmt)
    
        if output[rlc.MSG_KEY] == rlc.SUCCESS_MSG:
            file_name = f"{rlc.FILE_NAME}.{fmt}"
            file = FileWrapper(open(f"{MEDIA_PATH}/{file_name}", "rb"))
            response = HttpResponse(file, content_type=f"video/{fmt}")
            response["Content-Disposition"] = f"attachment; filename={file_name}"
            return response
        else:
            return HttpResponse(json.dumps(output), content_type="application/json", status=400)

