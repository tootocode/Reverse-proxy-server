import socket

s = socket.socket()
s.connect(('172.25.215.66', 1234))
print("----server start success----")
print("----please input nickname:",end='')
nick = input()
s.send(("nick:"+nick).encode())
print("----connect to 172.25.215.66 success---")
while True:
	
	data = (s.recv(1024)).decode()
	print(data)

