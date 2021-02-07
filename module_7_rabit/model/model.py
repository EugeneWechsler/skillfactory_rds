"""model.py"""
import pika
import json
import pickle
import numpy as np

with open('myfile.pkl', 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='Features')
    channel.queue_declare(queue='y_predict')

    def callback(ch, method, properties, body):
        print(f'Получен вектор признаков {body}')
        features = json.loads(body)
        pred = regressor.predict(np.array(features["val"]).reshape(1, -1))

        channel.basic_publish(exchange='',
                              routing_key='y_predict',
                              body=json.dumps(
                                  {
                                      "id" : features["id"],
                                      "val": pred[0]
                                  }))
        print(f'Предсказание {pred[0]} для {features["id"]} отправлено в очередь y_predict')


    channel.basic_consume(
        queue='Features', on_message_callback=callback, auto_ack=True)

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except:
    print('Не удалось подключиться к очереди')