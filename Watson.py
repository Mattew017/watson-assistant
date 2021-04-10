from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


ASSISTANT_ID = '29d5f536-595c-449b-8268-fb0c08bd8c1c'
APIKEY = 'k2HZ7nDmVWepBWQ6jqhfCZ2VicW4N2InnctgYS9SrINW'
URL = 'https://api.eu-gb.assistant.watson.cloud.ibm.com/instances/72d13037-b6e2-4af5-bd83-e13749154e98'
WORKSPACE_ID = '57256cdd-c343-410d-86e5-25ecd7f1c476'


class Watson:
    session_is_active = False

    def __init__(self):
        self.authenticator = IAMAuthenticator(APIKEY)
        self.assistant = AssistantV2(
            version='2021-01-15',
            authenticator=self.authenticator
        )
        self.assistant.set_service_url(URL)
        self.session = None
        self.session_id = None

    def start_session(self):

        # session start
        self.session_is_active = True
        self.session = self.assistant.create_session(assistant_id=ASSISTANT_ID)
        self.session_id = self.session.get_result()['session_id']
        print(f"SESSION  {self.session_id} STARTED")

    def send(self, command):
        try:
            response = self.assistant.message(
                assistant_id=ASSISTANT_ID,
                session_id=self.session_id,
                input={'text': command}
            ).get_result()['output']['generic'][0]['text']
            return response
        except Exception as exp:
            pass

    def end_session(self):
        # session delete
        try:
            if self.session_id and self.session_is_active:
                self.assistant.delete_session(assistant_id=ASSISTANT_ID, session_id=self.session_id)
                print(f"SESSION {self.session_id} ENDED")
                self.session_is_active = False
        except Exception as e:
            pass
