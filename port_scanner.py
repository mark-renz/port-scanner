import socket
import common_ports

def check_is_ip(target):
  return target.replace('.', '').isnumeric()

def get_open_ports(target, port_range, is_verbose = False):
  print(target)
  open_ports = []
  start, end = port_range[0], port_range[-1]
  socket.setdefaulttimeout(1)
  
  is_ip = check_is_ip(target)

  if is_ip:
    try:
      addr = socket.gethostbyaddr(target)
    except socket.gaierror:
      return('Error: Invalid IP address')
    except socket.error:
      print('get hostname fail')
  
  try:
      remote_ip = socket.gethostbyname(target)
  except socket.gaierror:
      return('Error: Invalid hostname')

  try:
    for port in range(start, end + 1):
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = s.connect_ex((remote_ip, port))
      if result == 0:
        open_ports.append(port)
      s.close()
    
  except socket.error:
    print("server connection fail")
      
      
  if is_verbose:
    verbose = str()
    try:
      addr = socket.gethostbyaddr(target)
      if addr == 'hostname':
        verbose = f'Open ports for {target}\n'
      else:
        verbose = f'Open ports for {addr[0]} ({remote_ip})\n'

    except socket.error:
      verbose = f'Open ports for {target}\n'

    verbose += "PORT     SERVICE"
    for port in open_ports:
      service = common_ports.ports_and_services[port]
      verbose += f'\n{port:<8} {service}'

    return(verbose)
  return(open_ports)