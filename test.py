import subprocess


#specify the absolute paths of client and server and certification
CLIENT_FILE="~/go/src/github.com/lucas-clemente/quic-go/example/client_benchmarker/main.go"
SERVER_FILE="~/go/src/github.com/lucas-clemente/quic-go/example/main.go"
CERT_PATH="~/go/src/github.com/lucas-clemente/quic-go/example/"

REMOTE_MACHINE_HOSTNAME="miniet@ip_address"
REMOTE_MACHINE_PORT="22"

# create topo, start server and client

def start_client(bind_address,server_address,server_port,file_to_get):
    cmds = CLIENT_FILE + '-m ' + '-b ' + bind_address + '-c ' + "https://" + server_address + ':' + server_port + '/' + file_to_get
    subprocess.Popen(['ssh','-q -p',REMOTE_MACHINE_PORT,REMOTE_MACHINE_HOSTNAME]).wait()
    subprocess.Popen(['ssh','-q -p',REMOTE_MACHINE_PORT,REMOTE_MACHINE_HOSTNAME,cmds]).wait()

def start_server(server_port):
    cmds= CLIENT_FILE + '- www . -certpath ' + CERT_PATH + ' -bind ' + '0.0.0.0:' + server_port
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,cmds])

def create_topo():
    cmds="sudo ~/git/minitopo/src/mpPerf.py " + "-t" + "conf/topo/simple_para"
    subprocess.Popen(['ssh','-q',REMOTE_MACHINE_HOSTNAME,cmds]).wait()


def setup_exp_env():
    cmd = 'ssh -p ' + REMOTE_MACHINE_PORT +' ' + REMOTE_MACHINE_HOSTNAME
    create_topo()
    start_server()
    setup_client()
