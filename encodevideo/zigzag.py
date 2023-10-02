
import numpy as np

def zigzag(input):

	h = 0 #cot
	v = 0 #dong

	vmin = 0
	hmin = 0

	vmax = input.shape[0]
	hmax = input.shape[1]

	#print(vmax ,hmax )

	i = 0
	#Tao mang 1 chieu co vxmax * hmax phan tu
	output = np.zeros(( vmax * hmax))
	#----------------------------------

	while ((v < vmax) and (h < hmax)):

		if ((h + v) % 2) == 0:                 #Thuong di thang~ tien neu chan~

			if (v == vmin):   #Di ngang  o cot dau tien
				#print(1)
				output[i] = input[v, h]     

				if (h == hmax):
					v = v + 1
				else:
					h = h + 1

				i = i + 1

			elif ((h == hmax -1 ) and (v < vmax)):   # Di thang xuong o cot cuoi cung
				#print(2)
				output[i] = input[v, h]
				v = v + 1
				i = i + 1

			elif ((v > vmin) and (h < hmax -1 )):    # Di cheo tu duoi trai' len phai
				#print(3)
				output[i] = input[v, h]
				v = v - 1
				h = h + 1
				i = i + 1


		else:           #Thuong di xuong neu le~

			if ((v == vmax -1) and (h <= hmax -1)):       # di ngang o dong cuoi'
				#print(4)
				output[i] = input[v, h]
				h = h + 1
				i = i + 1

			elif (h == hmin):           #di thang xuong o truong hop v chua bang  v max -1, di ngang neu bang
				#print(5)
				output[i] = input[v, h]

				if (v == vmax -1): #Di ngang
					h = h + 1
				else: #Di thang xuong
					v = v + 1

				i = i + 1

			elif ((v < vmax -1) and (h > hmin)):  #Duong di cheo' tu phai tren xuong trai
				#print(6)
				output[i] = input[v, h]
				v = v + 1
				h = h - 1
				i = i + 1




		if ((v == vmax-1) and (h == hmax-1)):          # Luu cai phan tu cuoi cung trong mang 2 chieu qua 1 chieu
			#print(7)
			output[i] = input[v, h]
			break

	#print ('v:',v,', h:',h,', i:',i)
	return output





def inverse_zigzag(input, vmax, hmax):

	h = 0 #Cot
	v = 0 #Dong

	vmin = 0
	hmin = 0
	#Tao mang hai chieu rong co dong v cot h 
	output = np.zeros((vmax, hmax))

	i = 0
	#----------------------------------

	while ((v < vmax) and (h < hmax)):
		#print ('v:',v,', h:',h,', i:',i)
		if ((h + v) % 2) == 0:                 #Di thang tien' neu chan~

			if (v == vmin):
				#print(1)

				output[v, h] = input[i]        # Di ngang o cot dau tien

				if (h == hmax):
					v = v + 1
				else:
					h = h + 1

				i = i + 1

			elif ((h == hmax -1 ) and (v < vmax)):   # Di thang xuong o cot cuoi cung
				#print(2)
				output[v, h] = input[i]
				v = v + 1
				i = i + 1

			elif ((v > vmin) and (h < hmax -1 )):    # Di cheo tu duoi trai len tren phai
				#print(3)
				output[v, h] = input[i]
				v = v - 1
				h = h + 1
				i = i + 1


		else:                                    # Di xuong neu le~

			if ((v == vmax -1) and (h <= hmax -1)):       # Di ngang o dong cuoi
				#print(4)
				output[v, h] = input[i]
				h = h + 1
				i = i + 1

			elif (h == hmin):                  # Di thang xuong o truong hop v chua bang v max, di ngang neu bang
				#print(5)
				output[v, h] = input[i]
				if (v == vmax -1): #Di ngang
					h = h + 1
				else: #Di thang xuong
					v = v + 1
				i = i + 1

			elif((v < vmax -1) and (h > hmin)):     #Di cheo tu phai tren xuong duoi trai'
				output[v, h] = input[i]
				v = v + 1
				h = h - 1
				i = i + 1




		if ((v == vmax-1) and (h == hmax-1)):          #Luu cai phan tu cuoi cung trong mang 1 chieu qua 2 chieu
			#print(7)
			output[v, h] = input[i]
			break


	return output
