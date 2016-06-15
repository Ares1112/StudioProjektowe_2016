from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

producer.send(topic='nadajnik1', key='666333111', value=b'19.530566,50.5734449')
producer.send(topic='nadajnik1', key='660333244', value=b'19.531557,49.5738449')
producer.send(topic='nadajnik1', key='560333200', value=b'19.511557,49.5738449')
# for x in range(100):
#       producer.send(topic='nadajnik1', key='666333111'+str(x), value=b'outofrange')
producer.flush()
