

# class NumberOfBucketsIntentHandler(AbstractRequestHandler):
#     """Handler for NumberOfBuckets Intent."""

#     def number_of_buckets(self):
#         s3_client = boto3.client('s3')
#         response = s3_client.list_buckets()
#         try:
#             if response:
#                 speak_output = "You have {} buckets.".format(len(response['Buckets']))
#             else:
#                 speak_output = "Sorry sir, you have no buckets in your account yet."

#         except ClientError as e:
#             logging.error(e)
#             return False
#         return True

#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("NumberOfBucketsIntent")(handler_input)

#     def handle(self, handler_input):
#         number_of_buckets()
#         return (
#             handler_input.response_builder
#             .speak(number_of_buckets().speak_output)
#             .ask("Sorry, didn't quite get that, could you please repeat your request.")
#             .response
#         )

# class ListBucketsIntentHandler(AbstractRequestHandler):
#     """Handler for ListBuckets Intent."""

#     def list_buckets(self):
#         s3_client = boto3.client('s3')
#         response = s3_client.list_buckets()
#         list_of_buckets = ""
#         for bucket in response['Buckets']:
#             list_of_buckets += bucket["Name"]
#             # print(f'  {bucket["Name"]}')
#             try:
#                 if response:
#                     speak_output = "Your buckets are {}.".format(list_of_buckets)
#                 else:
#                     speak_output = "Sorry sir, you have no buckets in your account yet."

#             except ClientError as e:
#                 logging.error(e)
#                 return False
#             return True

#     def can_handle(self, handler_input):
#         return ask_utils.is_intent_name("ListBucketsIntentHandler")(handler_input)

#     def handle(self, handler_input):
#         list_buckets()
#         return (
#             handler_input.response_builder
#             .speak(list_buckets().speak_output)
#             .ask("Sorry, didn't quite get that, could you please repeat your request.")
#             .response
#         )



# devops cloud assistant
# what s three buckets do i have
# create me a bucket with the name {bucket_name}


import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.utils import is_intent_name, get_slot_value
from botocore.exceptions import ClientError

import boto3

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sts_client = boto3.client('sts')
assumed_role_object=sts_client.assume_role(RoleArn="arn:aws:iam::xxxxx:role/alexa_assume_s3", RoleSessionName="AssumeRoleSession")
credentials=assumed_role_object['Credentials']

s3_client = boto3.client('s3',
                        aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'],
                        region_name='us-east-1')

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = ("Welcome back sir. how may i help you today?")
        reprompt = "I did not catch that, what was that again?"

        return (
            handler_input.response_builder
                .speak(speech_text)
                .ask(reprompt)
                .response
        )

class ListBucketsIntentHandler(AbstractRequestHandler):
    """Handler for President Name Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListBucketsIntent")(handler_input)

    def handle(self, handler_input):
        response = s3_client.list_buckets()
        list_of_buckets = ""
        name_count = len(response['Buckets'])
        # for i in response['Buckets']
        nameCount = len(response['Buckets'])
        for i in range(len(response['Buckets'])):
            list_of_buckets += "{}".format(response['Buckets'][i]["Name"])
            if i == (nameCount - 2):
                list_of_buckets += ", and "
            elif i != (nameCount - 1):
                list_of_buckets += ", "

        speech_text = ("These are the buckets you have sir: {}. ".format(list_of_buckets))
        reprompt = "I didn't quite get what you said, say that again?"

        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(reprompt)
            .response
        )

class CreateBucketIntentHandler(AbstractRequestHandler):
    """Handler for CreateBucket Intent."""
    def create_bucket(self, bucket_name, region=None):
        speak_output = ""
        # Create bucket
        try:
            s3_client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            if e.response['Error']['Code'] == "BucketAlreadyExists":
                speak_output += "The requested bucket name is either not available, already exists or not unique to AWS, please select a different name and try again."
            return False
        return True

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CreateBucketIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = ""
        bucket_name = get_slot_value(handler_input=handler_input, slot_name="bucket_name")
        if self.create_bucket(bucket_name):
            speak_output += "{} bucket has been created successfully.".format(bucket_name)
        else:
            speak_output += "The requested bucket name is either not available, already exists or not unique to AWS, please select a different name and try again."
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Sorry, didn't quite get that, could you please repeat your request.")
            .response
        )

class DeleteBucketIntentHandler(AbstractRequestHandler):
    """Handler for DeleteBucket Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("DeleteBucketIntent")(handler_input)

    def handle(self, handler_input):
        bucket_name = handler_input.attributes_manager.request_attributes["bucket_name"]
        if delete_bucket(bucket_name):
            speak_output = "{} bucket has been deleted successfully.".format(bucket_name)
        else:
            speak_output = "sorry, the requested bucket could not be deleted, make sure you \
            have deleted all files in the bucket before you attempt deleting it or you could \
                try saying \"alexa, delete all files in {} bucket.\"".format(bucket_name)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Sorry, didn't quite get that, could you please repeat your request")
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Try sayng something like, what s three buckets do i have"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you"ve
# defined are included below. The order matters - they"re processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ListBucketsIntentHandler())
sb.add_request_handler(CreateBucketIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn"t override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

