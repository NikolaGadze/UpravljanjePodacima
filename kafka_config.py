from confluent_kafka import Producer
import json

conf = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send_notification(topic, message):
    producer.produce(topic, value=json.dumps(message).encode('utf-8'), callback=delivery_report)
    producer.poll(1)
