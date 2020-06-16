import os
import sys
import logging
import json
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)


# Ref: https://github.com/googlesamples/assistant-sdk-python/blob/master/google-assistant-sdk/googlesamples/assistant/grpc/textinput.py

DEVICE_ID = os.getenv('DEVICE_ID')
DEVICE_MODEL_ID = os.getenv('DEVICE_MODEL_ID')
CREDENTIALS = os.path.join(os.environ['HOME'], '.config/google-oauthlib-tool/credentials.json')
ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5
LANG_CODE = 'ja-JP'


def gassist(text_query):
    # Load OAuth 2.0 credentials.
    try:
        with open(CREDENTIALS, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        logging.error('Error loading credentials', exc_info=True)
        sys.exit(-1)

    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, ASSISTANT_API_ENDPOINT)
    # Create an assistant.
    assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(grpc_channel)

    def assist(text_query):
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=LANG_CODE,
                    conversation_state=None,
                    is_new_conversation=True,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=DEVICE_ID,
                    device_model_id=DEVICE_MODEL_ID,
                ),
                text_query=text_query,
                )
            req = embedded_assistant_pb2.AssistRequest(config=config)
            yield req

        text_response = None
        html_response = None
        for resp in assistant.Assist(iter_assist_requests(), DEFAULT_GRPC_DEADLINE):
            if resp.screen_out.data:
                html_response = resp.screen_out.data
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        return text_response, html_response

    text, html = assist(text_query)
    logging.info(text)
    return text

