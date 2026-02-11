from celery import shared_task, chain
from .models import Document
from .services.analysis import analyze_document
from .services.qcm import generate_qcm


@shared_task
def process_document_pipeline(document_id):
    return chain(
        analyze_document.s(document_id)
    )()
