"""
Functions to handle predictions
"""

from config import PROD_CLIENT
from indico.queries import ModelGroupPredict, JobStatus


def predict(samples, model_id, client=PROD_CLIENT):
    """
    Get json predictions for each sample in samples

    Arguments:
        samples {List[str]} -- list of page text
        model_id {int} -- model_id number (found in the models Explain page)
        client {IndicoClient} -- Indico Client object containing auth data

    Returns:
        List[dict] -- list containing json output from indico predict api call

    """

    job = client.call(
        ModelGroupPredict(model_id=model_id,
                          data=samples)
    )

    predictions = client.call(JobStatus(id=job.id, wait=True)).result
    return predictions


def get_top_classification(classification_preds):
    """
    Given a list of classification prediction dicts, return the highest
    confidence label as well as confidence value
    """
    labels = []
    confidences = []
    for pred in classification_preds:
        label = max(pred, key=pred.get)
        labels.append(label)
        confidences.append(pred[label])

    return labels, confidences
