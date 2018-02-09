APP_MODULE = "server"
APP_OBJECT = "server"

DEBUG = 'True'
LOG_LEVEL = 'DEBUG'
SCRIPT_NAME = 'risktyes'
DOMAIN = None
API_STAGE = 'risktypes'
PROJECT_NAME = 'risktypes'

REMOTE_ENV = 's3://risktypes/zappa_settings.json'
# test_env.json
#{
#    "hello": "world"
#}
#

AWS_EVENT_MAPPING = {
    'arn:aws:s3:1': 'zappa_settings.aws_s3_event',
    'arn:aws:sns:1': 'zappa_settings.aws_sns_event',
    'arn:aws:dynamodb:1': 'zappa_settings.aws_dynamodb_event',
    'arn:aws:kinesis:1': 'zappa_settings.aws_kinesis_event'
}

ENVIRONMENT_VARIABLES = {'testenv': 'envtest'}

AUTHORIZER_FUNCTION = 'zappa_settings.authorizer_event'


def prebuild_me():
    print("This is a prebuild script!")


def callback(self):
    print("this is a callback")


def aws_s3_event(event, content):
    return "AWS S3 EVENT"


def aws_sns_event(event, content):
    return "AWS SNS EVENT"


def aws_async_sns_event(arg1, arg2, arg3):
    return "AWS ASYNC SNS EVENT"


def aws_dynamodb_event(event, content):
    return "AWS DYNAMODB EVENT"


def aws_kinesis_event(event, content):
    return "AWS KINESIS EVENT"


def authorizer_event(event, content):
    return "AUTHORIZER_EVENT"


def command():
    print("command")
