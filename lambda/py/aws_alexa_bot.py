# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import gettext
import boto3
from botocore.exceptions import ClientError

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractRequestInterceptor, AbstractExceptionHandler)
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from alexa import data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.WELCOME_MESSAGE)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

class CreateBucketIntentHandler(AbstractRequestHandler):
    """Handler for CreateBucket Intent."""

    def create_bucket(self, bucket_name, region=None):
        # Create bucket
        try:
            if region is None:
                s3_client = boto3.client('s3')
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client = boto3.client('s3', region_name=region)
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("CreateBucketIntent")(handler_input)

    def handle(self, handler_input):
        bucket_name = handler_input.attributes_manager.request_attributes["bucket_name"]
        if create_bucket(bucket_name):
            speak_output = "{} bucket has been created successfully.".format(bucket_name)
        else:
            speak_output = "sorry, the requested bucket could not be created."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask("Sorry, didn't quite get that, could you please repeat your request.")
            .response
        )

class DeleteBucketIntentHandler(AbstractRequestHandler):
    """Handler for DeleteBucket Intent."""

    def check_bucket_exists(self, bucket_name):
        s3_bucket_client = boto3.client('s3')
        buckets_response = s3_bucket_client.list_buckets()
        if bucket_name in buckets_response['Buckets']:
            return True
        else:
            return False

    def delete_bucket(self, bucket_name):
        try:
            if check_bucket_exists(bucket_name):
                s3_bucket_client = boto3.client('s3')
                response = s3_bucket_client.delete(bucket_name)
                return True
            else:
                return False
        except ClientError as e:
            logging.error(e)
            return False
        return True

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
            .ask("Sorry, didn't quite get that, could you please repeat your request.")
            .response
        )

class NumberOfBucketsIntentHandler(AbstractRequestHandler):
    """Handler for NumberOfBuckets Intent."""

    def number_of_buckets(self):
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        try:
            if response:
                speak_output = "You have {} buckets.".format(len(response['Buckets']))
            else:
                speak_output = "Sorry sir, you have no buckets in your account yet."

        except ClientError as e:
            logging.error(e)
            return False
        return True

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("NumberOfBucketsIntent")(handler_input)

    def handle(self, handler_input):
        number_of_buckets()
        return (
            handler_input.response_builder
            .speak(number_of_buckets().speak_output)
            .ask("Sorry, didn't quite get that, could you please repeat your request.")
            .response
        )

class ListBucketsIntentHandler(AbstractRequestHandler):
    """Handler for ListBuckets Intent."""

    def list_buckets(self):
        s3_client = boto3.client('s3')
        response = s3_client.list_buckets()
        list_of_buckets = ""
        for bucket in response['Buckets']:
            list_of_buckets += bucket["Name"]
            print(f'  {bucket["Name"]}')
            try:
                if response:
                    speak_output = "Your buckets are {}.".format(list_of_buckets)
                else:
                    speak_output = "Sorry sir, you have no buckets in your account yet."

            except ClientError as e:
                logging.error(e)
                return False
            return True

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListBucketsIntentHandler")(handler_input)

    def handle(self, handler_input):
        list_buckets()
        return (
            handler_input.response_builder
            .speak(list_buckets().speak_output)
            .ask("Sorry, didn't quite get that, could you please repeat your request.")
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.HELP_MSG)

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
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.GOODBYE_MSG)

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
        _ = handler_input.attributes_manager.request_attributes["_"]
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = _(data.REFLECTOR_MSG).format(intent_name)

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
        _ = handler_input.attributes_manager.request_attributes["_"]
        speak_output = _(data.ERROR)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class LocalizationInterceptor(AbstractRequestInterceptor):
    """
    Add function to request attributes, that can load locale specific data
    """

    def process(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        i18n = gettext.translation(
            'data', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes["_"] = i18n.gettext

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CreateBucketIntentHandler())
sb.add_request_handler(DeleteBucketIntentHandler())
sb.add_request_handler(NumberOfBucketsIntentHandler())
sb.add_request_handler(ListBucketsIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_global_request_interceptor(LocalizationInterceptor())

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
