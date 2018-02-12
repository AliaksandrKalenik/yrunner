from celery import task
from text_style_transfer.models import WEIGHTS_PATH, TrainModelRequest, \
    StyleTransferRequest
from text_style_transfer.neural_network import TextStyleTransfer


DEFAULT_TRAINING_DATA = 'https://s3.amazonaws.com/text-datasets/nietzsche.txt'

@task
def train_model(train_model_request_id, train_data_url=DEFAULT_TRAINING_DATA):
    train_model_request = TrainModelRequest.objects.filter(id=train_model_request_id).first()
    try:
        train_model_request.status = TrainModelRequest.IN_PROGRESS
        train_model_request.log = "Training in progress\n"
        train_model_request.save()
        tst = TextStyleTransfer(train_data_url, WEIGHTS_PATH)
        tst.train(20)
        train_model_request.log += "Completed"
        train_model_request.status = TrainModelRequest.COMPLETED
    except Exception as err:
        import traceback
        err_message = traceback.format_exc()
        train_model_request.log += "Exception: {}.\n{}\n".format(err, err_message)
        train_model_request.log += "Failed"
        train_model_request.status = TrainModelRequest.FAILED
    finally:
        train_model_request.save()


@task
def transfer_style(style_transfer_request_id, text):
    style_transfer_request = StyleTransferRequest.objects.filter(id=style_transfer_request_id).first()
    try:
        text = text.replace('\r', '').replace('\n', ' ')
        train_data_url = TrainModelRequest.objects.filter(
            status=TrainModelRequest.COMPLETED
        ).order_by(
            "-record_created"
        ).values_list(
            'train_data_url', flat=True
        ).first() or DEFAULT_TRAINING_DATA

        style_transfer_request.status = TrainModelRequest.IN_PROGRESS
        style_transfer_request.log = "Training in progress\n"
        style_transfer_request.save()
        tst = TextStyleTransfer(train_data_url, WEIGHTS_PATH)
        blanks = tst.fill_blanks(text)
        res = []
        blanks_i = 0
        for word in text.split(" "):
            if word == "_":
                res.append(blanks[blanks_i])
                blanks_i += 1
            else:
                res.append(word)
        style_transfer_request.result_text = " ".join(res)
        style_transfer_request.log += "Completed"
        style_transfer_request.status = TrainModelRequest.COMPLETED
    except Exception as err:
        import traceback
        err_message = traceback.format_exc()
        style_transfer_request.log += "Exception: {}.\n{}\n".format(err, err_message)
        style_transfer_request.log += "Failed"
        style_transfer_request.status = TrainModelRequest.FAILED
    finally:
        style_transfer_request.save()
