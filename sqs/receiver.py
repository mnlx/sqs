import boto3

sqs = boto3.resource('sqs')

queue = sqs.get_queue_by_name( QueueName='sqs')

message = queue.receive_messages()

print(message)

with open('received.txt', 'w') as file:
    file.write(message[0].body)

