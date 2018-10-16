# alexaMonetizationBreaks
A sample program for Amazon demonstrating the failure of the monetization service

This is a fictional skill called "Pink Unicorns" which does absolutely nothing except start up and break Amazon's monetization service in the manner I have observed with all of my skills to date.
The code is copied straight out of https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#in-skill-purchase-service and theoretically should work, although - as you'll find - does not.
## How I created this

1. I used _developer.amazon.com/alexa/console/ask_ to create a new skill
2. I set up the interaction model to include the required built-in intents such as _AMAZON.HelpIntent_, and added monetization intents _BuyProductIntent_ and _CanelProductIntent_.
3. I used the AWS Console to launch Lambda and create a new Lambda in **Python 3.6**, **us-east-1**, set the Handler to _lambda_function.handler_, added _Alexa Skills Kit_ as a trigger, and attached my custom IAM policy which includes full permissions on CloudWatch, CloudFront, Lambda, DynamoBD, EC2, Certificate Manager, Route 53, S3, IAM, and a slew of other AWS services (total overkill! but effective).
4. I associated this lambda with my skill via the Endpoint portion of the alexa developer console. _arn:aws:lambda:us-east-1:..._
5. On my local Windows 10 machine (which has ASK CLI installed already) I used ASK CLI to _ask clone_ my skill
6. I fetched my interaction model: _ask api get-model -s amzn1.ask.skill.blah-blah-blah -l en-US_
7. I used _virtualenv_ to install the ask_sdk, following instructions found here: _https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#adding-the-ask-sdk-for-python-to-your-project_
8. I pulled relevant packages out of site-packages/Lib/ and put them in the lambda/us-east-1_camplist/ -- this git repo contains all of these packages.
9. I added an isp to my skill by executing _ask add isp_
10. I altered the .json file for my isp to be compliant; this included copying the contents of an alexa sample found in github and then adding things such as valid image paths, etc. Again, this file can be found in this repo.
11. I wrote python in lambda_function.py to use the sdk and StandardSkillBuilder to handle relevant intents, and to make the call to the monetization service, copying the code from https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#in-skill-purchase-service
12. I performed an _ask deploy_
13. Using the Test section of the developer console, I tested "Open Pink Unicorns" which throws the familiar 403 error and responds "There was a problem with the requested skill's response."
14. I checked my CloudWatch logs for details.

## Instructions for Replicating the Error

1. Follow the first 5 steps above, setting up your skill, your lambda, and your local code directory.  (Make sure that you have an appropriate IAM role set up to assign)
2. Clone this repo into that directory on your local machine.
3. Change all instances of skill ID from my old ID to your new one.
4. _ask deploy_ and make sure that it builds correctly.
5. Follow steps 13 and 14

## CloudWatch Logs

You should see something like the below in your logs, noting that I added statements in the alexa sdk for the Amazon support contact Anand where the failure occurs.

```
START RequestId: dde2fe66-d106-11e8-bd56-a77369e14463 Version: $LATEST
*-> ANAND: Now inside ask_sdk_model.services.base_service_client.py
*-> ANAND: Initializing BaseServiceClient()...
*-> ANAND: invoke() on BaseServiceClient()...
*-> ANAND: ApiClientRequest created and populated with the following data:
*-> ANAND: url: https://api.amazonalexa.com/v1/users/~current/skills/~current/inSkillProducts
*-> ANAND: method: GET
*-> ANAND: headers: [('Accept-Language', 'en-US'), ('Content-type', 'application/json'), ('Authorization', 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLmRkNWQ3YTUxLTgwN2UtNDZiNC05ZDM1LWIxZGVlMTg1NDIzYSIsImV4cCI6MTUzOTY3MjQwNSwiaWF0IjoxNTM5NjY4ODA1LCJuYmYiOjE1Mzk2Njg4MDUsInByaXZhdGVDbGFpbXMiOnsiY29uc2VudFRva2VuIjpudWxsLCJkZXZpY2VJZCI6ImFtem4xLmFzay5kZXZpY2UuQUdHUkNFQktYR1g3VFNHTUlOSERGTFpDRTY0WVg0QTZRSFU2NFJYTExKSkNJU0lRMkhJU1NUWkxERTVFV0I0WlBJN1hSUVdDTEdMSE1FS09KTFdXQkdCS0lCS0FGVFQ1VUhSQVlIWlNKQTNQVldGQ0xaRDZDRkpDTDIyQkpLNzVaQzVVREpWS002NzU2WDM0UlFLSTdCWUhQNDNRIiwidXNlcklkIjoiYW16bjEuYXNrLmFjY291bnQuQUhHVjRRMlhGVVVKNkxVWTZMN002Q0NXTFJGVTVDR1ZVVzJNMkpGRTJTNkpCSDJOUk9YQ1pUSFM2VFFSUUpFT05HVVlFWVBXT1dRVFU2NVZYTkpaQ1U2N1JYTENSTTM2SjdRNVpQQkpRWEtDWFRIMkZaRk9PWk9XM0czSUtBSlZZRlRCNlJGSlRWR0ZXS0NXR0pFMzdPV1RVR0FRQk41N01ZNTRLSE5QNURMWVBRRUxORjZUWlc0MjRRU0NHV1RMNEFBVFNYSUZCS0FNWVVJIn19.QzTj59CPDj08XZw2I54pG9Zdnk48Vi5JP-2GPd6lJ_nRQE6XL_8y9LmjHIZSPNX8GbpYQcfoTc3FmxibpRxQW4twQtapQvIF6ervhOit52UzQcaf0eJPJKNq9UwZ-oDOQFmAP65ugdyagvg9HtZktyUqp-gDh3EazB6OD06KuZK1v3SgjXB5IQlRr4j1PxomSk1koqGJgysjwVbx1cgrvvFv4fEV3KPLbDEsXISm4xho7jJeSJfEp-sZ-X_Kkkat8ex3z7HJGiq63h9sQrSv-HorCOQHEpn3J_AejvgZKDVeim56fJKpWJG1VH3Myh4o5-C4h7fL1G30bLW4kCZFfg')]
*-> ANAND: body: None
*-> ANAND: calling self._api_client.invoke(request)
*-> ANAND: api client invocation successful; no Exception raised.
*-> ANAND (!!!): BaseServiceClient.__is_code_successful(response.status_code) returned false.
*-> ANAND: No response_definitions were passed into this method... raising a ServiceException
*-> ANAND: ServiceException message: Unknown Error
*-> ANAND: ServiceException status_code: 403
*-> ANAND: ServiceException headers: [('Server', 'CloudFront'), ('Date', 'Tue'), ('Date', '16 Oct 2018 05:46:46 GMT'), ('Content-Type', 'text/html'), ('Content-Length', '556'), ('Connection', 'keep-alive'), ('X-Cache', 'Error from cloudfront'), ('Via', '1.1 51c76241371dfc20d25094a51b4759eb.cloudfront.net (CloudFront)'), ('X-Amz-Cf-Id', 'q3OA_ysVzjypuMJtFmeIS1exW9-5FY8NiKJhtvSxsx5RB67zPGj0TQ==')]
*-> ANAND: ServiceException body: <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<HTML><HEAD><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=iso-8859-1">
<TITLE>ERROR: The request could not be satisfied</TITLE>
</HEAD><BODY>
<H1>403 ERROR</H1>
<H2>The request could not be satisfied.</H2>
<HR noshade size="1px">
Bad request.

<BR clear="all">
<HR noshade size="1px">
<PRE>
Generated by cloudfront (CloudFront)
Request ID: q3OA_ysVzjypuMJtFmeIS1exW9-5FY8NiKJhtvSxsx5RB67zPGj0TQ==
</PRE>
<ADDRESS>
</ADDRESS>
</BODY></HTML>
Unknown error: ServiceException
Traceback (most recent call last):
File "/var/task/ask_sdk_core/skill_builder.py", line 187, in wrapper
request_envelope=request_envelope, context=context)
File "/var/task/ask_sdk_core/skill.py", line 191, in invoke
response = self.request_dispatcher.dispatch(handler_input)
File "/var/task/ask_sdk_core/dispatch.py", line 164, in dispatch
raise e
File "/var/task/ask_sdk_core/dispatch.py", line 149, in dispatch
response = self.__dispatch_request(handler_input)
File "/var/task/ask_sdk_core/dispatch.py", line 217, in __dispatch_request
handler_input=handler_input, handler=request_handler)
File "/var/task/ask_sdk_core/dispatch_components/request_components.py", line 478, in execute
return handler.handle(handler_input)
File "/var/task/lambda_function.py", line 40, in handle
product_response = ms.get_in_skill_products(locale)
File "/var/task/ask_sdk_model/services/monetization/monetization_service_client.py", line 120, in get_in_skill_products
response_type="ask_sdk_model.services.monetization.in_skill_products_response.InSkillProductsResponse")
File "/var/task/ask_sdk_model/services/base_service_client.py", line 129, in invoke
message="Unknown error", status_code=response.status_code, headers=response.headers, body=response.body)
ask_sdk_model.services.service_exception.ServiceException: Unknown error

END RequestId: dde2fe66-d106-11e8-bd56-a77369e14463
```