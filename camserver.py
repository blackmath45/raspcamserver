import io
import socket
import struct
import cv2
import numpy as np
import picamera
import time

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

while True :
	# Accept a single connection and make a file-like object out of it
	connection = server_socket.accept()[0].makefile('wb')
	try:
		with picamera.PiCamera() as camera:
			camera.resolution = (1920, 1080)
			camera.framerate = 30
			# Start a preview and let the camera warm up for 2 seconds
			camera.start_preview()
			time.sleep(2)

			# Note the start time and construct a stream to hold image data
			# temporarily (we could write it directly to connection but in this
			# case we want to find out the size of each capture first to keep
			# our protocol simple)
			stream = io.BytesIO()
			for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
				# Write the length of the capture to the stream and flush to
				# ensure it actually gets sent
				connection.write(struct.pack('<L', stream.tell()))
				connection.flush()
				# Rewind the stream and send the image data over the wire
				stream.seek(0)
				connection.write(stream.read())

				# Reset the stream for the next capture
				stream.seek(0)
				stream.truncate()
	except:
		connection.close()
		print("Connection closed")