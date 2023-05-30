from keras.models import Model
import math
from keras.models import load_model
from keras.layers import (
	Conv2D,
	MaxPooling2D,
	UpSampling2D,
	Dropout,
	BatchNormalization,
	Input,
)
from keras import utils
import numpy as np
from threading import current_thread, Thread
import sys
from queue import Queue
import easyocr


"""
class Printer:
	def __init__(self):
		self.queues = {}
	
	def write(self, value):
		queue = self.queues.get(current_thread().name)
		if queue:
			queue.put(value)
		else:
			sys.__stdout__.write(value)
	
	def flush(self):
		pass
	
	def register(self, thread):
		queue = Queue()
		self.queues[thread.name] = queue
		return queue

	def clean(self, thread):
		del self.queues[thread.name]

printer = Printer()
sys.stdout = printer

class Streamer:
	def __init__(self, target, args):
		self.thread = Thread(target = target, args=args)
		self.queue = printer.register(self.thread)

	def start(self):
		self.thread.start()
		print('This should be stdout')
		while self.thread.is_alive():
			try:
				item = self.queue.get_nowait()
				yield f'{item}<br>'
			except Exception:
				pass
		yield 'End'
		printer.clean(self.thread)
"""


def model():
	input_layer = Input(shape=(420, 540, 1))  # согласно размеру всех изображений

	# слои для encoder
	x = Conv2D(24, (3, 3), activation="relu", padding="same")(input_layer)
	x = Conv2D(48, (3, 3), activation="relu", padding="same")(x)
	x = BatchNormalization()(x)
	x = MaxPooling2D((2, 2), padding="same")(x)
	x = Dropout(0.5)(x)

	# слои decodera
	x = Conv2D(48, (3, 3), activation="relu", padding="same")(x)
	x = Conv2D(24, (3, 3), activation="relu", padding="same")(x)
	x = BatchNormalization()(x)

	x = UpSampling2D((2, 2))(x)

	output_layer = Conv2D(1, (3, 3), activation="sigmoid", padding="same")(x)
	model = Model(inputs=[input_layer], outputs=[output_layer])
	model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])

	return model


def image_to_list(path):
	images_width = 540
	images_height = 420
	img_pil = utils.load_img(
		path, color_mode="grayscale", target_size=(images_height, images_width)
	)  # converting image to PIL format
	img_arr = utils.img_to_array(img_pil).astype(
		"float32"
	)  # converting PIL format to array
	img_arr /= 255.0  # making all array values from 0 to 1
	return img_arr



def clear_image(image_path):
	model = load_model("model")
	model.summary()

	# image to list convertion
	#old_path = image_path
	image_path = "./" + image_path

	m_data = np.empty((420, 420, 540, 1))
	m_data[0] = image_to_list(image_path)

	result = model.predict(m_data, batch_size=32)
	utils.array_to_img(result[0]).save(image_path[:-4] + "_result.png")
	
	reader = easyocr.Reader(["en"])
	result = reader.readtext(f'{image_path[:-4] + "_result.png"}', detail = 0, paragraph = True)
	
	return image_path[:-4] + "_result.png", result[0]
