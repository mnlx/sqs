import boto3

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name( QueueName='sqs')


with open('contents.txt', 'r') as file:
    data = file.read()

response = queue.send_message(
    MessageBody=data,
    # MessageGroupId='loveFest1'
)