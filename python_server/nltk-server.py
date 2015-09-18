import pika
import nltk

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='nltk_queue')

def tokens(sentence):
    tokens = nltk.word_tokenize(sentence)
    return tokens

def on_request(ch, method, props, body):
    print " [.] Received body: %s" % (body[0:10] + body[-10:])

    response = tokens(body)

    ch.basic_publish(exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = \
                    props.correlation_id),
            body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='nltk_queue')

print ' [x] Awaiting RPC requests . . .'
channel.start_consuming()
