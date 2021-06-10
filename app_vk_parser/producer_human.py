import time
import json
import random
from kafka import KafkaProducer
import datetime

def publish_message(producer, topic_name, key, value):
    try:
        producer.send(topic_name, key=key, value=value)
        #producer.flush()
        print('Message published successfully.')
        time.sleep(1)
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))



producer = KafkaProducer(bootstrap_servers="kafka-svc:9092",
                         key_serializer=str.encode,
                         value_serializer=str.encode)

mechta_info = json.loads(open("../data/mechta.json", "r").read())

topicnames = []

for d in mechta_info:

    topicname = 'male'
    if "sex" in d.keys() and \
       d["sex"] is not None and \
       int(d["sex"]) == 1:
        topicname = "female"

    topicnames.append((str(d["id"]),topicname))

    age = 0
    topicname = "18-"
    if d["age"] is None:
        if "bdate" in d.keys():
            date = d["bdate"].split(".")
            if len(date) == 3:
                age = 2021 - int(date[-1])
    else:
        age = int(d["age"])

    if age >= 18 and age < 27:
        topicname = "18-27"
    if age >= 27 and age < 40:
        topicname = "27-40"
    if age >= 40 and age < 60:
        topicname = "40-60"
    if age >= 60:
        topicname = "60-"

    topicnames.append((str(d["id"]),topicname))
    
    count_interests = random.randint(1,3)
    
    for i in range(count_interests):
        topicname = random.choice(["other", "sport", "music", "it"])
        topicnames.append((str(d["id"]),topicname))

for id, topicname in topicnames:
    dt = datetime.datetime.now()
    timestamp = int((time.mktime(dt.timetuple()) + dt.microsecond/1000000.0)*1000)
    message = '{"value":"%s","timestamp":%d}'%(topicname, timestamp)
    if topicname in ["other", "sport", "music", "it"]:
        publish_message(producer, "hobbi"+topicname, 'mechta', id)
    else:
        publish_message(producer, "id"+topicname, 'mechta', message)
