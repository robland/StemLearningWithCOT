from celery import shared_task

from ..models import Exercise, Step, QCM, Choice


@shared_task
def generate_qcm(exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    steps_data = exercise.raw_text

    for step_data in steps_data:
        step = Step.objects.create(
            exercise=exercise,
            step_number=step_data["step_number"],
            objective=step_data["objective"],
            explanation=step_data.get("explanation", "")
        )

        qcm = QCM.objects.create(
            step=step,
            question=step_data["question"],
            correct_choice=step_data["correct_answer"]
        )

        for choice in step_data["choices"]:
            Choice.objects.create(
                qcm=qcm,
                label=choice[0],
                text=choice[3:]  # "A. texte"
            )

    exercise.document.processing_status = "done"
    exercise.document.save()
