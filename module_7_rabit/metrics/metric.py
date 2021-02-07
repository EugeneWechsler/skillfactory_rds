"""metric.py"""
import pika
import json
import pandas as pd
from sklearn.metrics import mean_squared_error

try:
	connection = pika.BlockingConnection(
	    pika.ConnectionParameters(host='rabbitmq'))
	channel = connection.channel()

	id_vals = pd.DataFrame(columns=["y_true","y_predict"])

	channel.queue_declare(queue='y_true')
	channel.queue_declare(queue='y_predict')

	def callback(ch, method, properties, body):		
		id_val = json.loads(body)
		id_vals.loc[id_val["id"],method.routing_key] = id_val["val"]
		ys = id_vals.dropna(axis=0)		
		rmse = mean_squared_error(ys.y_true, ys.y_predict) if ys.shape[0]>0 else 666666

		answer_string = f'Из очереди {method.routing_key} получено значение {id_val}, current rmse {rmse}'
		with open('/logs/labels_log.txt', 'a') as log:
			log.write(answer_string +'\n')

	channel.basic_consume(
		queue='y_predict', on_message_callback=callback, auto_ack=True)

	channel.basic_consume(
		queue='y_true', on_message_callback=callback, auto_ack=True)

	print('...Ожидание сообщений, для выхода нажмите CTRL+C')
	channel.start_consuming()
	
except Exception as e:
	with open('/logs/metrics_error.txt', 'a') as log:
		log.write(e)