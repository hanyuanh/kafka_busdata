from time import sleep
from pykafka import KafkaClient
import json
import uuid
import time
from datetime import datetime

# read coordinates
input_file = open('./data/bus_csueb_route_c.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']
# coordinates = json_array['features'][0]


# generate uuid for the data
def generate_uuid():
    return uuid.uuid4()

#kafka producer
client = KafkaClient(hosts="localhost:9092")
topic = client.topics['geodata_final123']
producer = topic.get_sync_producer()

#CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}
data['busline'] = '00003' # route c

def generate_checkpoint(coordinates):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)

        #if bus reaches last coordinate, start from beginning
        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

generate_checkpoint(coordinates)

'''
# kafka producer
client = KafkaClient(hosts="localhost:9092")

topic = client.topics['testBusdata']

producer = topic.get_sync_producer()

count = 1
while True:
    msg = "hello {}".format(count).encode('ascii')
    producer.produce(msg)
    sleep(1)
'''