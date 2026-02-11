from celery import shared_task, chain

from .services.analysis import analyze_document


@shared_task
def process_document_pipeline(document_id):
    return chain(
        analyze_document.s(document_id)
    )()
