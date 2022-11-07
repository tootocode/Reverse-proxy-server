# coding=utf-8

import socket
import threading
from time import sleep

import pymysql


class Nat_Server:

    def __init__(self):
        super(Nat_Server, self).__init__()
        self.tcp_socket = None
        self.sever_th = None
        self.client_th = None
        self.client_socket_list = list()
        self.internal_socket_nick_list = list()
        self.internal_nick_list = list()
        self.link = False  # 用于标记是否开启了连接
        self.conn = pymysql.Connect(host='localhost', user='root', password='123456', database='project', port=3306)
        self.cursor = self.conn.cursor()

    def tcp_server_start(self):

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)
        try:
            port = 1234
            self.tcp_socket.bind(('101.76.246.1', port))
        except Exception as ret:
            # msg = '请检查端口号\n'
            # self.signal_write_msg.emit(msg)
            print("请检查端口号")
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            print("------正在开启服务器--------")
            sleep(3)
            msg = '------开启成功，正在监听端口:%s' % str(port) + '--------'
            # self.signal_write_msg.emit(msg)
            print(msg)

    def tcp_server_concurrency(self):
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as ret:
                pass
            else:
                client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表,client_address为ip和端口的元组
                self.client_socket_list.append((client_socket, client_address))
                msg = '服务端已连接IP %s' % str(client_address)
                print(msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    recv_msg = client.recv(4096)
                    # nick = client_socket.recv(1024)
                except Exception as ret:
                    pass
                else:
                    if recv_msg:
                        msg = str(recv_msg.decode('utf-8'))
                        # print(msg.__sizeof__())
                        if "nick" in msg:
                            nick = msg.split(":")[1]
                            self.internal_socket_nick_list.append((client, nick))
                            self.internal_nick_list.append(nick)
                            # print("nickname:"+nick)
                        if "/getonline/list" in msg:
                            respone_to_client = "/response/sendonline/list"
                            for client_only, nick in self.internal_socket_nick_list:
                                respone_to_client = respone_to_client + "\n" + nick
                            print(respone_to_client)
                            client.send(respone_to_client.encode())
                        if "submit*ipaddr*" in msg:
                            lists = msg.split("*")
                            if lists[2] not in self.internal_nick_list:
                                client.send("/nickname/error".encode())
                                continue
                            ipaddr = lists[3]
                            print(ipaddr)
                        if "/get/iotresult/" in msg:
                            lists = msg.split("/")
                            if lists[3] not in self.internal_nick_list:
                                client.send("/nickname/error".encode())
                                continue

                        msg = '来自IP:{}端口:{}'.format(address[0], msg)
                        print(msg)
                    else:
                        client.close()
                        self.internal_socket_nick_list.remove((client, nick))
                        print("----------" + address[0] + "已断开链接---------")
                        self.client_socket_list.remove((client, address))
                        self.internal_nick_list.remove(nick)


if __name__ == '__main__':
    NS = Nat_Server()
    NS.tcp_server_start()
