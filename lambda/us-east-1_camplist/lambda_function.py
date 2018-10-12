import random

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk.standard import StandardSkillBuilder

sb = StandardSkillBuilder()


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """Inform the request handler of what intents can be handled by this object.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            bool: Whether or not the current intent can be handled by this object.

        """
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """ Handle the launch request; fetch and serve the appropriate response.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Raises:
            ValueError: If something other than the sanctioned app calls this intent.

        Returns:
            ask_sdk_model.response.Response: Response for this intent and device.

        """
        # Prevent someone else from configuring a skill that sends requests to this:
        if handler_input.request_envelope.session.application.application_id != \
                "amzn1.ask.skill.dd5d7a51-807e-46b4-9d35-b1dee185423a":
            raise ValueError("Invalid Application ID")

        speech = "Camp list provides a checklist of items to pack for camping trips. "
        speech += "Would you like me to help you plan a trip? "
        reprompt = "What do you want to do? "

        return handler_input.response_builder.speak(speech).ask(
            reprompt).set_should_end_session(False).response


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


class ProductShopHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """Inform the request handler of what intents can be handled by this object.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            bool: Whether or not the current intent can be handled by this object.

        """
        return is_intent_name("ShopIntent")(handler_input)

    def handle(self, handler_input):
        """ Handle the launch request; fetch and serve the appropriate response.

        Args:
            handler_input (ask_sdk_core.handler_input.HandlerInput): The input from Alexa.

        Returns:
            ask_sdk_model.response.Response: Response for this intent and device.

        """

        # productName = handler_input.request_envelope.request.intent.slots["ProductName"]["value"]
        locale = handler_input.request_envelope.request.locale
        ms = handler_input.service_client_factory.get_monetization_service()
        inSkillResponse = ms.get_in_skill_products(locale)

        if not inSkillResponse:
            speech = ("I am having trouble reaching Amazon's monetization "
                      "service. What else can I do for you?")
            reprompt = "I didn't catch that. Can you try again?"
            return handler_input.response_builder.speak(speech).ask(
                reprompt).response

        # Inform the user about what products are available for purchase
        purchasable = [l for l in inSkillResponse.in_skill_products
                       if l.entitled == EntitledState.NOT_ENTITLED and
                       l.purchasable == PurchasableState.PURCHASABLE]

        if purchasable:
            speech = ("There is currently one item for sale. ")
        else:
            owned = [x for x in inSkillResponse.in_skill_products
                     if x.entitled == EntitledState.NOT_ENTITLED]
            if len(owned) == len (list(inSkillResponse.in_skill_products)):
                speech = ("It appears as if you already own all items "
                          " What else can I help you with? ")
            else:
                speech = ("There are currently no more items "
                          "available. What can I help you with?")
        reprompt = "Try saying I'm a butt. "
        return handler_input.response_builder.speak(speech).ask(
            reprompt).response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(ProductShopHandler())

handler = sb.lambda_handler()
