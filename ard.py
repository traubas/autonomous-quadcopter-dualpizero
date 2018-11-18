import sys
from serial import Serial
from time import sleep



class QuadSerial():
	ser = Serial('/dev/ttyUSB0',)
	ser.baudrate = 115200


	def send(self,ch1, ch2, ch3, ch4):
		return self.send2((int(-127 + ch1 * 254)),
		(int(-127 + ch2 * 254)),
		(int(-127 + ch3 * 254)),
		(int(-127 + ch4 * 254)))
		# i=0;
		# while (i<len(controls)):
		# 	print (controls[i])
		# 	i=i+1
		# print("\n")

		#return sendRaw(controls, len(controls));
	def send2(self,ch1,ch2,ch3,ch4):
		controls = [
			0xFF,
			self.toSignBitFormat(self.clampInt(ch1, -127, 127)),
			self.toSignBitFormat(self.clampInt(ch2, -127, 127)),
			self.toSignBitFormat(self.clampInt(ch3, -127, 127)),
			self.toSignBitFormat(self.clampInt(ch4, -127, 127)),
			0, 0, 0];
		return self.sendRaw(controls, len(controls))

	def toSignBitFormat(self,n):
		result = 0

		if (n >= 0):
			result = n
		else:
			result = -n
			result |= 0x80

		return result

	def clampInt(self,n, minVal, maxVal):
		if (n > maxVal):
			return maxVal
		if (n < minVal):
			return minVal
		return n
	def sendRaw(self,data,length):
		return self.write(data,length)

	def write(self,data,length):
		self.ser.write(bytes(data))
		# arduino.write(data)
		# while(1):
		# 	print(arduino.readline())

	# def main():
	    

	# 	print(ser.readline())
	# 	send(0.5, 0.5, 0.0, 0.5)
	# 	sleep(1)
	# 	send(0.5, 0.7, 0.1, 0.5)
	# 	sleep(0.2)
	# 	send(0.5, 0.5, 0.0, 0.5)
	# 	sleep(0.2)
	# 	send(0.5, 0.3, 0.1, 0.5)
	# 	sleep(0.2)
	# 	send(0.5, 0.5, 0.0, 0.5)
	# 	sleep(0.2)
	# 	send(0.7, 0.5, 0.1, 0.5)
	# 	sleep(0.2)
	# 	send(0.5, 0.5, 0.0, 0.5)
	# 	sleep(0.2)
	# 	send(0.3, 0.5, 0.1, 0.5)
	# 	sleep(0.2)
	# 	send(0.5, 0.5, 0.0, 0.5)

	# 	return 0

	# if __name__ == '__main__':
	#     sys.exit(main())
