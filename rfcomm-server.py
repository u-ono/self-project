import bluetooth
import os
import jtalk

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

client_sock, address = server_sock.accept()
print "Accepted connection from ", address

speed = 8
volume = 80

while(True):
    data = client_sock.recv(1024)
    if data[0:2] == 's+':
        speed += 1
        speed = max([speed, 13])
        continue
    elif data[0:2] == 's-':
        speed -= 1
        speed = min([speed, 3])
        continue
    elif data[0:2] == 'v+':
        volume += 5
        volume = max([volume, 100])
        os.system('amixer -c 0 sset PCM {}%'.format(volume))
        continue
    elif data[0:2] == 'v-':
        volume -= 5
        volume = min([volume, 0])
        os.system('amixer -c 0 sset PCM {}%'.format(volume))
        continue
    print "received [%s]" % data
    jtalk.jtalk(data, speed/10.0)

client_sock.close()
server_sock.close()
