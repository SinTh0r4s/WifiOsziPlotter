# To run this script you will have to install some python libs.
# Install matplotlib and scipy on your python environment
# or execute 'pip install matplotlib scipy' on you terminal.
# If you python installation does not ship with tkinter,
# as on Ubuntu you want to also run 'apt install python3-tk'
# on your terminal. Enjoy


import socket
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.io

# Tell matplotlib to use a backend that allows manual zoom of the data
matplotlib.use('TkAgg')


localIP = "192.168.43.134"
#localIP = "192.168.1.3"
localPort = 7567
bufferSize = 1446


# init UDP
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")

# The arduino will partition the measurements into:
numDatagrams = 10
dataPerDatagram = 1000

# As long as the connection is from device to device not reordering can occur.
# Listen for incoming datagrams and display them
figureNumber = 1
while True:
    datagrams = []
    for i in range(numDatagrams):
        [message, address] = UDPServerSocket.recvfrom(bufferSize)

        clientMsg = "Message from Client:{}".format(message)
        clientIP = "Client IP Address:{}".format(address)

        samplePoints = np.frombuffer(message, dtype='uint8')
        datagrams = np.append(datagrams, samplePoints)

    # interpret values
    mV = datagrams * 1650 / 255
    # TODO: time interpretation

    # plot data
    plt.figure()
    plt.title("Figure " + str(figureNumber))
    plt.ylabel("mV")
    plt.xlabel("Sample ID")
    plt.plot(mV)
    plt.ylim(0, 3300)
    plt.show()
    # Please note: plt.shot() is ui blocking! You will need to close a plot to see the next.
    # Sadly this is a limitation of matplotlib and linked to the functionality to provide
    # interactive zoom. Luckily, no data can be lost UNTIL the ethernet input buffer is full.

    # save data
    scipy.io.savemat('figure_' + str(numDatagrams) + '.mat', {'samples': mV})

    figureNumber = figureNumber + 1
