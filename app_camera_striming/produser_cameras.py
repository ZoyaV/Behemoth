import time
from kafka import KafkaProducer
from cameras import get_people_number
import random

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

life_centers = {"dream_complex":[114, 124, 123, 121, 112, 113, 77, 54, 55, 53,105, 108, 106],
                "murinski":[17, 15, 71, 16, 73, 56, 120, 32],
                "new_murino":[153, 155, 154, 10, 119]}

while True:
    mechta = random.randint(20,30)
#     murinski = get_people_number(life_centers["murinski"])
#     new_murino = get_people_number(life_centers["murinski"])

    publish_message(producer, "camera_mechta", "mechta", str(mechta))
#     publish_message(producer, "murinski", "murinski", str(murinski))
#     publish_message(producer, "newmurino", "newmurino", str(new_murino))

    time.sleep(10)
