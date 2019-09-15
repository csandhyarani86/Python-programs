#!/usr/bin/python
import sys
topic = sys.argv[1]
Edimessage = sys.argv[2]
from kafka import KafkaClient, SimpleProducer
kafka = KafkaClient('10.0.9.3:9092')
producer = SimpleProducer(kafka)
producer.send_messages(topic,Edimessage)
kafka.close()
