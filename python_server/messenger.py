import pika
import nltk

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='nltk_away')

def tokens(sentence):
    tokens = nltk.word_tokenize(sentence)
    return tokens

def callback(ch, method, props, body):
    print " [.] Received: %s" % (body[0:10] + body[-10:])

    response = tokens(body)

    # this is where we get into sticky territory
    channel.queue_declare(queue='nltk_back')

    ch.basic_publish(exchange='',
            routing_key='nltk_back',
            body=str(response))
    print " [x] Sent response . . ."
    channel.start_consuming()
    # that doesn't get unsticky until here

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='nltk_away')

print ' [x] Awaiting RPC requests . . .'
channel.start_consuming()
