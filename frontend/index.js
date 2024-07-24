const DJANGO_SCRIPT_PATH = "http://0.0.0.0:8000/running_text_video_generator"

var form = document.getElementsByTagName("form")[0];

form.addEventListener("submit", (e) => {
  e.preventDefault();
  var formData = new FormData(e.target);
  var formProps = Object.fromEntries(formData);
  var redirectLocation = `${DJANGO_SCRIPT_PATH}?text=${formProps['text']}&fmt=${formProps['fmt']}`;
  window.location = redirectLocation;
});
