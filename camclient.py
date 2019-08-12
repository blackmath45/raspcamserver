import io
import socket
import struct
import cv2
import numpy as np
import datetime

cv2.namedWindow('test',cv2.WINDOW_NORMAL)
cv2.resizeWindow('test',800,600)

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.100', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(4))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        # Construct a numpy array from the stream
        data = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)

        # "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)

        #image = cv2.flip(image, 0)		
        
        cv2.imshow("test", image)
        c = cv2.waitKey(7) % 0x100
        
        if c == 27 or c == 10:
            break
			
        if c == 115:
            now = datetime.datetime.now()
            cv2.imwrite(now.strftime('%Y-%m-%d-%H-%M-%S') + ".jpg", image);

finally:
    cv2.destroyAllWindows()
    connection.close()
    client_socket.close()
