import json

from celery import shared_task

from .qcm import generate_qcm
from ..models import Exercise, Document
from ..services.openai_vision import ExerciseVisionService


@shared_task
def analyze_document(document_id):

    document = Document.objects.get(id=document_id)

    document.processing_status = "analyzing"
    document.save()

    raw_text = ExerciseVisionService.analyze_exercise(
        file_url=document.file.path,
        subject="maths"
    )
    json_text = raw_text[7:len(raw_text)-3].strip()
    with open("./openai.response.json", "w") as f:
        f.write(json_text)

    json_object = json.loads(json_text)

    for key, value in json_object.items():

        exercise = Exercise.objects.create(
            title=key,
            document=document,
            subject="maths",
            raw_text=value
        )
        generate_qcm.delay(str(exercise.id))

    return str(document.id)
