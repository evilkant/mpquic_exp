import subprocess


#specify the absolute paths of client and server and certification
CLIENT_FILE="~/go/src/github.com/lucas-clemente/quic-go/example/client_benchmarker/main.go"
SERVER_FILE="~/go/src/github.com/lucas-clemente/quic-go/example/main.go"
CERT_PATH="~/go/src/github.com/lucas-clemente/quic-go/example/"

<<<<<<< HEAD
REMOTE_MACHINE_HOSTNAME="miniet@ip_address"
#REMOTE_MACHINE_PORT="22"
=======
REMOTE_MACHINE_HOSTNAME="miniet@192.168.100.129"
REMOTE_MACHINE_PORT="22"
>>>>>>> 72db2e0d3e0c820627c8b660d5ebfae1b3094ac7

# create topo, start server and client

def start_client(server_address,server_port,file_to_get):
    cmds = "Client " + CLIENT_FILE + '-m ' + '-c ' + "https://" + server_address + ':' + server_port + '/' + file_to_get
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME]).wait()
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,cmds]).wait()

def start_server(server_port,content_dir):
    cmds= "Server" + SERVER_FILE + '-www' + content_dir + ' -certpath ' + CERT_PATH + ' -bind ' + '0.0.0.0:' + server_port
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,cmds]).wait()

def create_topo():
    cmds="sudo ~/git/minitopo/src/mpPerf.py " + "-t" + "conf/topo/simple_para"
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,cmds]).wait()


# i am thinking that we need to know the virtual IP of the virtual SERVER and CLIENT

#Server-eth0 10.1.0.1
#Client-eth0 10.0.0.1
#Client-eth1 10.0.1.1

SERVER_ADDR="10.1.0.1"
SERVER_PORT="6121"
CONTENT_DIR="~/test-data"

def setup_exp_env():
    create_topo()
<<<<<<< HEAD
    start_server(SERVER_PORT,CONTENT_DIR)


#start_client(SERVER_ADDR,SERVER_PORT,"Nature.html")

def generateTcpdumpString(interface,filename,snaplen=217):
    return "sudo tcpdump -i " + interface + ' -w ' + filename + ' -s ' + snaplen + ' udp'

def run_test(testId,filename):
    print('start running test '+str(testId))

    server_dump_name="results/"+str(testId)+filename+'server.pcap'
    server_dump_cmd=generateTcpdumpString("Server-eth0",server_dump_name)

    client_eth0_dump_name="results/"+str(testId)+filename+'client_0.pcap'
    client_eth0_dump_cmd=generateTcpdumpString("Client-eth0",client_eth0_dump_name)

    client_eth1_dump_name="results/"+str(testId)+filename+'client_1.pcap'
    client_eth1_dump_cmd=generateTcpdumpString("Client-eth1",client_eth1_dump_name)

    #start tcpdump
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,server_dump_cmd])
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,client_eth0_dump_cmd])
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,client_eth1_dump_cmd])

    time.sleep(1)   #make sure tcpdump is up

    start_client(SERVER_ADDR,SERVER_PORT,filename)

    time.sleep(2)

    #stop server and remove download file

    #stop tcpdumps

    #get results from client
    
run_test(1,"Nature.html")
=======
    start_server("6121")
    start_client("0.0.0.0","localhost","6121","Nature.html")
>>>>>>> 72db2e0d3e0c820627c8b660d5ebfae1b3094ac7
