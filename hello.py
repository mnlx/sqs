from flask import Flask
import boto3
import base64

app = Flask(__name__)

@app.route('/save')
def save():
    with open('bach.mp3', 'rb') as audio:
        binary = audio.read()
        save = binary[0: 255 * 1024]

    with open('bach_split.mp3', 'wb') as audio_split:
        audio_split.write(save)

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='sqs')

    with open('bach.mp3', 'rb') as audio:
        binary = audio.read()
        save = binary[0: 255 * 500]

    base64Audio = base64.b64encode(save)
    print(len(base64Audio))
    response = queue.send_message(
        MessageBody=base64Audio.decode('ascii'),
    )
    print(response)
    return 'Saved'

@app.route('/listen')
def listen():
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='sqs')
    message = queue.receive_messages()

    # base64AudioDecoded = base64.b64decode(message[0].body)
    # with open('bach_sqs.mp3', 'wb') as file:
    #     file.write(base64AudioDecoded)

    return f'<p><audio controls src="data:audio/mp3;base64,{message[0].body}"></audio></p>'


