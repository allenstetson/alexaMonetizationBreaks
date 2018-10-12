# alexaMonetizationBreaks
A sample program for Amazon demonstrating the failure of the monetization service

This is a fictional skill called "Camp List" which does absolutely nothing except start up and break Amazon's monetization service in the manner I have observed with all of my skills to date.

## How I created this

1. I used _developer.amazon.com/alexa/console/ask_ to create a new skill
2. I set up the interaction model to include the required built-in intents such as _AMAZON.HelpIntent_, and added one custom intent called _ShopIntent_ with invocation prompts including "shop".
3. I used the AWS Console to launch Lambda and create a new Lambda in **Python 3.6**, **us-east-1**, set the Handler to _lambda_function.handler_, added _Alexa Skills Kit_ as a trigger, and attached my custom IAM policy which includes full permissions on CloudWatch, CloudFront, Lambda, DynamoBD, EC2, Certificate Manager, Route 53, S3, IAM, and a slew of other AWS services (total overkill! but effective).
4. I associated this lambda with my skill via the Endpoint portion of the alexa developer console. _arn:aws:lambda:us-east-1:..._
5. On my local Windows 10 machine (which has ASK CLI installed already) I used ASK CLI to _ask clone_ my skill
6. I fetched my interaction model: _ask api get-model -s amzn1.ask.skill.blah-blah-blah -l en-US_
7. I used _virtualenv_ to install the ask_sdk, following instructions found here: _https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/GETTING_STARTED.html#adding-the-ask-sdk-for-python-to-your-project_
8. I pulled relevant packages out of site-packages/Lib/ and put them in the lambda/us-east-1_camplist/ -- this git repo contains all of these packages.
9. I added an isp to my skill by executing _ask add isp_
10. I altered the .json file for my isp to be compliant; this included copying the contents of an alexa sample found in github and then adding things such as valid image paths, etc. Again, this file can be found in this repo.
11. I wrote python in lambda_function.py to use the sdk and SkillBuilder to handle relevant intents, and to make the call to the monetization service as detailed here (notably, the first three lines in the handle() method found in the examples): _https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/SERVICE_CLIENTS.html#monetizationserviceclient_
12. I performed an _ask deploy_
13. Using the Test section of the developer console, I tested "Open Camp List" which worked, and then "shop" which throws the familiar 403 error.
14. I checked my CloudWatch logs for details.

## Instructions for Replicating the Error

1. Follow the first 5 steps above, setting up your skill, your lambda, and your local code directory.  (Make sure that you have an appropriate IAM role set up to assign)
2. Clone this repo into that directory on your local machine.
3. Change all instances of skill ID from my old ID to your new one.
4. _ask deploy_ and make sure that it builds correctly.
5. Follow steps 13 and 14

