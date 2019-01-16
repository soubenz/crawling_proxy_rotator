#!/usr/bin/python
import requests
import socket
import sys
from jinja2 import Template

Consul_api_server="http://localhost:8500"
Consul_service="my-cluster"
Haproxy_servers="/var/run/haproxy.sock"
Backend_name="backendnodes"

#The following are only used for building the configuration from template
Haproxy_template_file="/home/haproxy/haproxy/haproxy.tmpl"
Haproxy_config_file="/home/haproxy/haproxy/haproxy.cfg"
Haproxy_spare_slots=4
Backend_base_name="websrv"

def send_haproxy_command(server, command):
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

def build_config_from_template(backends):
   backend_block=""
   i=0
   for backend in backends:
      i+=1
      backend_block += "   server %s%d %s:%s cookie %s%d check\n" % (Backend_base_name, i,backend[0], backend[1],Backend_base_name, i)
   for disabled_slot in range(0,Haproxy_spare_slots):
      i+=1
      backend_block += "   server %s%d 0.0.0.0:80 cookie %s%d check disabled\n" % (Backend_base_name, i,Backend_base_name, i)
   try:
      haproxy_template_fh = open(Haproxy_template_file, 'r')
      haproxy_template = Template(haproxy_template_fh.read())
      haproxy_template_fh.close()
   except:
      print("Failed to read HAProxy config template")
   template_values = {}
   template_values["backends_%s"%(Backend_name)] = backend_block
   try:
      haproxy_config_fh = open(Haproxy_config_file,'w')
      haproxy_config_fh.write(haproxy_template.render(template_values))
      haproxy_config_fh.close()
   except:
      print("Failed to write HAProxy config file")



def get_backends(server):
   try:
      backends_reply = send_haproxy_command(server,"show backend\n")
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

def get_slots(backend, hserver):


   haproxy_slots = send_haproxy_command(hserver,"show stat\n")
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


def set_servers(servers, backend,slots, haproxy):
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
               send_haproxy_command(haproxy, "set server %s/%s addr %s port %s\n" % (backend, slot_to_use, server[0], server[1]))
               send_haproxy_command(haproxy, "set server %s/%s state ready\n" % (backend, slot_to_use))
            
            # print ('+++++')
if __name__ == "__main__":

   backends_list = get_backends(Haproxy_servers)
   # print(backends_list)

   backend_servers = [('127.0.0.1','8118','FR'), ('127.0.0.1','8119', 'test'), ('127.0.0.1','8111','fr'), ('127.0.0.1','8138','DE')]
   for backend in backends_list:
      backends_slots = get_slots(backend,Haproxy_servers)
      print(backends_slots)

      set_servers(backend_servers, backend, backends_slots,Haproxy_servers)
         # if len(haproxy_inactive_backends) > 0:
   # #             backend_to_use = haproxy_inactive_backends.pop(0)
   #       send_haproxy_command(haproxy_server, "set server %s/%s addr %s port %s\n" % (Backend_name, backend_to_use, backend[0], backend[1]))
   # #             send_haproxy_command(haproxy_server, "set server %s/%s state ready\n" % (Backend_name, backend_to_use))
   #          else:
   #             print("WARNING: Not enough backend slots in backend")
   #    for remaining_server in haproxy_active_backends:
   #       send_haproxy_command(haproxy_server, "haproxy_server, set server %s/%s state maint\n" % (Backend_name, remaining_server))
   # #Finally, rebuild the HAProxy configuration for restarts/reloads
   # build_config_from_template(backend_servers)

   '''
   
   #First, get the servers we need to add
#    try:
#       consul_json = requests.get("%s/v1/catalog/service/%s" % (Consul_api_server, Consul_service))
#       consul_json.raise_for_status()
#       consul_service = consul_json.json()
#    except:
#       print("Failed to get backend list from Consul.")
#       sys.exit(1)
#    backend_servers=[]
#    for server in consul_service:
#       backend_servers.append([server['Address'], server['ServicePort']])
#    if len(backend_servers) < 1:
#       print("Consul didn't return any servers.")
#       sys.exit(2)


   #Now update each HAProxy server with the backends in question

   
   for haproxy_server in Haproxy_servers:
      haproxy_slots = send_haproxy_command(haproxy_server,"show stat\n")
      if not haproxy_slots:
         print("Failed to get current backend list from HAProxy socket.")
         sys.exit(3)
      haproxy_slots = haproxy_slots.split('\n')

      haproxy_active_backends = {}
      haproxy_inactive_backends = []
      # print(haproxy_slots)
      for backend in haproxy_slots:
         backend_values = backend.split(",")
         # print(backend_values[0] == Backend_name)
         if len(backend_values) > 80 and backend_values[0] == Backend_name:
            server_name = backend_values[1]
            if server_name == "BACKEND":
               continue
            server_state = backend_values[17]
            # print(server_state)
            server_addr = backend_values[73]
            if server_state == "MAINT":
               #Any server in MAINT is assumed to be unconfigured and free to use (to stop a server for your own work try 'DRAIN' for the script to just skip it)
               haproxy_inactive_backends.append(server_name)
            else:
               haproxy_active_backends[server_addr] = server_name
      haproxy_slots = len(haproxy_active_backends) + len(haproxy_inactive_backends)
      
      backend_servers = [('127.0.0.1','8118')]
      for backend in backend_servers:
         if "%s:%s" % (backend[0],backend[1]) in haproxy_active_backends:
            print (haproxy_active_backends["%s:%s" % (backend[0],backend[1])]) #Ignore backends already set
         else:
            if len(haproxy_inactive_backends) > 0:
               backend_to_use = haproxy_inactive_backends.pop(0)
               send_haproxy_command(haproxy_server, "set server %s/%s addr %s port %s\n" % (Backend_name, backend_to_use, backend[0], backend[1]))
               send_haproxy_command(haproxy_server, "set server %s/%s state ready\n" % (Backend_name, backend_to_use))
            else:
               print("WARNING: Not enough backend slots in backend")
      for remaining_server in haproxy_active_backends:
         send_haproxy_command(haproxy_server, "haproxy_server, set server %s/%s state maint\n" % (Backend_name, remaining_server))
   #Finally, rebuild the HAProxy configuration for restarts/reloads
   build_config_from_template(backend_servers)

   '''