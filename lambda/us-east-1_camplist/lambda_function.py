# =============================================================================
# IMPORTS
# =============================================================================
import logging
import random
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type
from ask_sdk_model.response import Response
from ask_sdk_model.services.monetization import (
    EntitledState, PurchasableState, InSkillProductsResponse)
from ask_sdk_model.interfaces.connections import SendRequestDirective


# =============================================================================
# LOGGING
# =============================================================================
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# =============================================================================
# CLASSES
# =============================================================================

# -----------------------------------------------------------------------------
# The following are Monetization handlers copied verbatim (*no lines changed!)
# from:
# https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#in-skill-purchase-service
# -----------------------------------------------------------------------------
class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        locale = handler_input.request_envelope.request.locale
        ms = handler_input.service_client_factory.get_monetization_service()
        product_response = ms.get_in_skill_products(locale)

        if isinstance(product_response, InSkillProductsResponse):
            total_products = len(product_response.in_skill_products)
            entitled_products = len([l for l in product_response.in_skill_products
                                     if l.entitled == EntitledState.ENTITLED])
            purchasable_products = len([l for l in product_response.in_skill_products
                                        if l.purchasable == PurchasableState.PURCHASABLE])

            speech = (
                "Found total {} products of which {} are purchasable and {} "
                "are entitled".format(
                    total_products, purchasable_products, entitled_products))
        else:
            speech = "Something went wrong in loading your purchase history."

        return handler_input.response_builder.speak(speech).response


class BuyProductIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BuyProductIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Obtain the corresponding product_id for the requested in-skill
        # product by invoking InSkillProducts API.
        # The slot variable product_name used below is only for demonstration.

        locale = handler_input.request_envelope.request.locale
        ms = handler_input.service_client_factory.get_monetization_service()

        product_response = ms.get_in_skill_products(locale)
        slots = handler_input.request_envelope.request.intent.slots
        product_ref_name = slots.get("product_name").value
        product_record = [l for l in product_response.in_skill_products
                          if l.reference_name == product_ref_name]

        if product_record:
            return handler_input.response_builder.add_directive(
                SendRequestDirective(
                    name="Buy",
                    payload={
                        "InSkillProduct": {
                            "productId": product_record[0].product_id
                        }
                    },
                    token="correlationToken")
            ).response
        else:
            return handler_input.response_builder.speak(
                "I am sorry. That product is not available for purchase"
                ).response


class CancelProductIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CancelProductIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Obtain the corresponding product_id for the requested in-skill
        # product by invoking InSkillProducts API.
        # The slot variable product_name used below is only for demonstration.

        locale = handler_input.request_envelope.request.locale
        ms = handler_input.service_client_factory.get_monetization_service()

        product_response = ms.get_in_skill_products(locale)
        slots = handler_input.request_envelope.request.intent.slots
        product_ref_name = slots.get("product_name").value
        product_record = [l for l in product_response.in_skill_products
                          if l.reference_name == product_ref_name]

        if product_record:
            return handler_input.response_builder.add_directive(
                SendRequestDirective(
                    name="Cancel",
                    payload={
                        "InSkillProduct": {
                            "productId": product_record[0].product_id
                        }
                    },
                    token="correlationToken")
            ).response
        else:
            return handler_input.response_builder.speak(
                "I am sorry. I don't know that one").response


# -----------------------------------------------------------------------------
# The following are standard handlers that I wrote to handle built-in intents.
# -----------------------------------------------------------------------------
class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """Inform the request handler of what intents/requests can be handled by this object.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            bool: Whether or not the current intent can be handled by this object.

        """
        return not (not is_intent_name("AMAZON.CancelIntent")(handler_input) and not is_intent_name(
            "AMAZON.StopIntent")(handler_input) and not is_intent_name("AMAZON.PauseIntent")(handler_input))

    def handle(self, handler_input):
        """ Handle the launch request; fetch and serve the appropriate response.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            ask_sdk_model.response.Response: Response for this intent and device.

        """
        speeches = [
            "As you wish. ",
            "Of course. ",
            "Canceling. ",
            "Disappointing, but okay. "
        ]
        speech = random.choice(speeches)


        responseBuilder = handler_input.response_builder
        responseBuilder.speak(speech).ask(speech)
        responseBuilder.set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """Inform the request handler of what intents/requests can be handled by this object.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            bool: Whether or not the current intent can be handled by this object.

        """
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        """ Handle the launch request; fetch and serve the appropriate response.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            ask_sdk_model.response.Response: Response for this intent and device.

        """
        speeches = [
            "Sure. Whatever. ",
            "Of course. ",
            "Canceling. "
        ]
        speech = random.choice(speeches)

        responseBuilder = handler_input.response_builder
        responseBuilder.speak(speech).ask(speech)
        responseBuilder.set_should_end_session(True)
        return handler_input.response_builder.response

# =============================================================================
# SKILL BUILDER
# =============================================================================
sb = StandardSkillBuilder()
# Monetization:
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BuyProductIntentHandler())
sb.add_request_handler(CancelProductIntentHandler())
# Standard:
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())


handler = sb.lambda_handler()
