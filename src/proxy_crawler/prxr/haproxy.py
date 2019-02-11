#!/usr/bin/python
import requests
import socket
import sys
from jinja2 import Template
import logging

class Haproxy(object):


	def __init__(self):
		self.haproxy_server="/var/run/haproxy.sock"
		self.Backend_name="backendnodes"
		self.logger = logging.getLogger()
		self.logger.setLevel(logging.INFO)
	def send_haproxy_command(self, command):
		server = self.haproxy_server
		if server[0] == "/":
			haproxy_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		else:
			haproxy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		haproxy_sock.settimeout(10)
		try:
			haproxy_sock.connect(server)
			haproxy_sock.send(command)
			retval = ""
			while True:
				buf = haproxy_sock.recv(16)
				if buf:
					retval += buf
				else:
					break
			haproxy_sock.close()
		except:
			retval = ""
			print('oops')
		finally:
			haproxy_sock.close()
		return retval


	def get_backends(self):
		# server = self.Haproxy_servers
		try:
			backends_reply = self.send_haproxy_command("show backend\n")
		except:
			return None

		if backends_reply:

			backeneds_list = backends_reply.strip()
			backeneds_list = backeneds_list.split('\n')
			if backeneds_list[0] == '# name':
				backeneds_list.pop(0)
				backeneds_list.pop(-1)

				# print(type(backends))
				return backeneds_list

			else:
				return None

	def get_slots(self, backend):

		# hserver = self.Haproxy_servers
		haproxy_slots = self.send_haproxy_command("show stat\n")
		if not haproxy_slots:
			print("Failed to get current backend list from HAProxy socket.")
			sys.exit(3)
		haproxy_slots = haproxy_slots.split('\n')
		# print(haproxy_slots)
		# print(len(haproxy_slots))
		slots_num = 0

		haproxy_active_backends = {}
		slots = []
		for server in haproxy_slots:
			server_values = server.split(",")
			if len(server_values) > 80 and server_values[0] in backend:
				server_name = server_values[1]
				# print(server_values)
				if server_name == "BACKEND":
					continue
				else:
					# print('++++==')
					server_state = server_values[17]
					server_addr = server_values[73]
					# if server_state == "MAINT":
						#Any server in MAINT is assumed to be unconfigured and free to use (to stop a server for your own work try 'DRAIN' for the script to just skip it)
						# haproxy_inactive_backends.append(server_name)
					# else:
					slots.append(server_name)
					# print(slots)
		# print(slots)
		return slots
				# slots_num += 1
				# slots_num = len(haproxy_active_backends) + len(haproxy_inactive_backends)

		# return  haproxy_active_backends
					# if server_state == "MAINT":
						#Any server in MAINT is assumed to be unconfigured and free to use (to stop a server for your own work try 'DRAIN' for the script to just skip it)
						# haproxy_inactive_backends.append(server_name)
					# else:
						# haproxy_active_backends[server_addr] = server_name
			# haproxy_slots = len(haproxy_active_backends) + len(haproxy_inactive_backends)

	def get_servers():
		pass


	def set_servers(self, servers, backend, slots):
		# backend = self.get_slots()
		slots = slots
		for server in servers:
			# print(backend)
			if server[2].lower() == backend:
				if "%s:%s" % (server[0],server[1]) in slots:
					pass
						# print (haproxy_active_backends["%s:%s" % (backend[0],backend[1])]) #Ignore backends already set
				else:
					print ((server[0],server[1]))
					if slots:
						slot_to_use = slots.pop(0)
						self.send_haproxy_command("set server %s/%s addr %s port %s\n" % (backend, slot_to_use, server[0], server[1]))
						self.send_haproxy_command("set server %s/%s state ready\n" % (backend, slot_to_use))
						self.logger.info("set server %s/%s addr %s port %s\n" % (backend, slot_to_use, server[0], server[1]))
			# elif backend == "all"
				# print ('+++++')
# if __name__ == "__main__":

#    backends_list = get_backends(Haproxy_servers)
#    # print(backends_list)

#    backend_servers = [('127.0.0.1','8118','FR'), ('127.0.0.1','8119', 'test'), ('127.0.0.1','8111','fr'), ('127.0.0.1','8138','DE')]
#    for backend in backends_list:
#       backends_slots = get_slots(backend,Haproxy_servers)
#       print(backends_slots)

#       set_servers(backend_servers, backend, backends_slots,Haproxy_servers)
