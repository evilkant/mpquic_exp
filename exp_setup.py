import sys, getopt
import math

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from subprocess import Popen,PIPE

topoParamFile = None

def parseArgs(argv):
    global topoParamFile

    try:
        opts,args=getopt.getopt(argv,"t:",["topoParam="])
    except getopt.GetoptError:
        sys.exit(1)
    for opt,arg in opts:
        if opt in ("-t",'--topoParam'):
            topoParamFile=arg
    if topoParamFile is None:
        print("Missing the topo...")
        sys.exit(1)

class attributed_link():
    def __self__(self,id,delay,queueSize,bandwidth,loss,back_up=False):
        self.id=id
        self.delay=delay
        self.queueSize=queueSize
        self.bandwidth=bandwidth
        self.loss=loss
        #self.queuingDelay
        self.back_up=back_up

    def asDict(self):
        d={}
        d['bw']=float(self.bandwidth)
        d['delay']=self.delay+"ms"
        d['loss']=float(self.loss)
        d['max_queue_size']=int(self.queueSize)
        return d


class MpParamTopo(paramFile):

    # this object holds paramDic and linkAttrs

    LSUBNET="leftSubnet"
    RSUBNET="rightSubnet"
    netemAt="netemAt_"
    changeNetem="changeNetem"
    defaultValue={}
    defaultValue[LSUBNET]="10.1."
    defaultValue[RSUBNET]="10.2."
    defaultValue[changeNetem]="false"

    def __init__(self,paramFile):
        self.paramDic={}
        self.loadParamFile(paramFile)   #flesh out the paramDic
        self.linkAttrs=[]
        self.loadLinkAttrs()

    def loadParamFile(self,paramFile):
        file=open(paramFile)
        i=0
        for line in file:
            i=i+1
            if line.startswith("#"):    #ignore comments
                continue
            tab=line.split(":")
            if len(tab)==2:
                k=tab[0]
                v=tab[1][:-1]   #[:-1] is used to get rid of \n
                if k in self.paramDic:
                    if not isinstance(self.paramDic[k],list):
                        self.paramDic[k]=[self.paramDic[k]]
                    self.paramDic[k].append(v)
                else:
                    self.paramDic[k]=v
            else:
                print("Ignored line "+str(i) + "In file "+ paramFile)
        f.close()

    def loadLinkAttrs(self):
        i=0
        for k in sorted(self.paramDic): # i do not see why we need to sort it
            if k.startswith("path"):
                tab=self.paramDic[k].split(",")
                backup=False
                loss="0.0"
                if len(tab)==5:
                    loss=tab[3]
                    backup=(tab[4]=='True')
                if len(tab)==4:
                    try:
                        loss=float(tab[3])
                        loss=tab[3]
                    except ValueError:
                        backup=(tab[3]=='True')
                if len(tab)==3 or len(tab)==4 or len(tab)==5:
                    path=attributed_link(i,tab[0],tab[1],tab[2],loss,backup)
                    #id delay queueSize bandwidth loss back_up
                    self.linkAttrs.append(path)
                    i=i+1
                else:
                    print("Ignored path "+self.paramDic[k])

    def getParamFromTopoParamDic(self,k):
        if k in self.paramDic:
            return self.paramDic[k]
        return None


class MpTopo:

    #static properties
    clientName="Client"
    serverName="Server"
    routerName="Router"
    switchNamePrefix="s"
    routerNamePrefix="r"

    def __init__(self,topoBuilder,topoParam):

        self.topoBuilder=topoBuilder
        self.topoParamObj=topoParam

        self.client=self.addHost(clientName)
        self.server=self.addHost(serverName)
        self.router=self.addHost(routerName)
        self.switch=[]

        for link in self.topoParam.linkAttrs:
            self.switch.append(self.addOneSwitchPerLink(link))
            self.addLink(self.client,self.switch[-1])
            self.addLink(self.switch[-1],self.router,**link.asDict())
            self.addLink(self.router,self.server)

    def addOneSwitchPerLink(self,link):
        return self.addSwitch(switchNamePrefix+str(link.id))

    def getAttributedLinks(self):
        return self.topoParamObj.linkAttrs

    def commandTo(self,who,cmd):
        return self.topoBuilder.commandTo(who,cmd)

    def getHost(self,who):
        return self.topoBuilder.getHost(who)

    def addHost(self,host):
        return self.topoBuilder.addHost(who)

    def addSwitch(self,host):
        return self.topoBuilder.addSwitch(who)

    def addLink(self,fromA,toB,**kwargs):
        self.topoBuilder.addLink(formA,toB,**kwargs)

    def getCLI(self):
        self.topoBuilder.startNetwork()

    def stopNetwork(self):
        self.topoBuilder.stopNetwork()


class MpConfig:
    def __init__(self,topo,param):
        self.topo=topp
        self.param=param

    def configureNetwork(self):
        self.configureInterfaces()
        self.configureRoute()

    def configureInterfaces():  #we did not configure switch though
        self.client = self.topo.getHost(MpTopo.clientName)
		self.server = self.topo.getHost(MpTopo.serverName)
		self.router = self.topo.getHost(MpTopo.routerName)

		i = 0
		netmask = "255.255.255.0" #why do we need the netmask

		links = self.topo.getAttributedLinks()
		for l in self.topo.switch:
			cmd = self.interfaceUpCommand(
					self.getClientInterface(i),
					self.getClientIP(i), netmask)

			self.topo.commandTo(self.client, cmd)

			clientIntfMac = self.client.intf(self.getClientInterface(i)).MAC()

			self.topo.commandTo(self.router, "arp -s " + self.getClientIP(i) + " " + clientIntfMac)

			#if(links[i].back_up):
			#	cmd = self.interfaceBUPCommand(
			#			self.getClientInterface(i))
			#	self.topo.commandTo(self.client, cmd)

			cmd = self.interfaceUpCommand(
					self.getRouterInterfaceSwitch(i),
					self.getRouterIPSwitch(i), netmask)

			self.topo.commandTo(self.router, cmd)

			routerIntfMac = self.router.intf(self.getRouterInterfaceSwitch(i)).MAC()

            self.topo.commandTo(self.client, "arp -s " + self.getRouterIPSwitch(i) + " " + routerIntfMac)

            print(str(links[i]))

			i = i + 1

		cmd = self.interfaceUpCommand(self.getRouterInterfaceServer(),
				self.getRouterIPServer(), netmask)
		self.topo.commandTo(self.router, cmd)
		routerIntfMac = self.router.intf(self.getRouterInterfaceServer()).MAC()
		self.topo.commandTo(self.server, "arp -s " + self.getRouterIPServer() + " " + routerIntfMac)

		cmd = self.interfaceUpCommand(self.getServerInterface(),
				self.getServerIP(), netmask)
		self.topo.commandTo(self.server, cmd)
		serverIntfMac = self.server.intf(self.getServerInterface()).MAC()
		self.topo.commandTo(self.router, "arp -s " + self.getServerIP() + " " + serverIntfMac)

    def configureRoute(self):
        i=0
        for l in self.topo.switch:
            cmd=self.addRouteTableCommand(self.getClientIP(i),i)
            self.topo.commandTo(self.client,cmd)

            cmd=self.addRouteScopeLinkCommand(  #route scope, maybe related to subnet
                self.getClientSubnet(i),
                self.getClientInterface(i),
                i
            )
            self.topo.commandTo(self.client,cmd)

            cmd.self.addRouteDefaultCommand(self.getRouterIPSwitch(i),i)
            self.topo.commandTo(self.client,cmd)
            i=i+1

        cmd=self.addRouteDefaultGlobalCommand(self.getRouterIPSwitch(0),
            self.getClientInterface(0))
        self.topo.commandTo(self.client,cmd)

        cmd=self.addRouteDefaultSimple(self.getRouterIPServer())
        self.topo.commandTo(self.server,cmd)

    def getClientIP(self,interfaceID):
        lSubnet=self.param.getParam(MpParamTopo.LSUBNET)
        clinetIP=lSubnet+str(interfaceID)+".1"
        return clientIP

    def getClientSubnet(self,interfaceID):
        lSubnet=self.param.getParam(MpParamTopo.LSUBNET)
        clinetSubnet=lSubnet+str(interfaceID)+".0/24"
        return clinetSubnet

    def getRouterIPSwitch(self,interfaceID):
        lSubnet=self.param.getParam(MpParamTopo.LSUBNET)
        routerIP=lSubnet+str(interfaceID)+".2"
        return routerIP

    def getRouterIPServer(self):
        rSubnet=self.param.getParam(MpParamTopo.RSUBNET)
        routerIP=rSubent+"0.2"
        return routerIP

    def getServerIP(self):
        rSubnet=self.param.getParam(MpParamTopo.RSUBNET)
        serverIP=rSubnet+"0.1"
        return serverIP

    def getClientInterfaceCount(self):
		return len(self.topo.switch)

	def getRouterInterfaceServer(self):
		return self.getRouterInterfaceSwitch(len(self.topo.switch))

	def getClientInterface(self, interfaceID):
		return  MpTopo.clientName + "-eth" + str(interfaceID)

	def getRouterInterfaceSwitch(self, interfaceID):
		return  MpTopo.routerName + "-eth" + str(interfaceID)

	def getServerInterface(self):
		return  MpTopo.serverName + "-eth0"

	def getMidLeftName(self, id):
		return MpTopo.switchNamePrefix + str(id)

	def getMidRightName(self, id):
		return MpTopo.routerName

	def getMidL2RInterface(self, id):
		return self.getMidLeftName(id) + "-eth2"

	def getMidR2LInterface(self, id):
		return self.getMidRightName(id) + "-eth" + str(id)

#this class inherits from mininet class Topo
class MininetBuilder(Topo):
    def __init__(self):
        Topo.__init__(self)
        self.net=None

    def commandTo(self,who,cmd):
        return who.cmd(cmd)

    def startNetwork(self):
        #relly? topo=self?
        self.net=Mininet(topo=self,link=TCLink)
        self.net.start()

    def getCLI(self):
        if self.net is None:
            print("can not get the CLI")
        else:
            CLI(self.net)

    def getHost(self,who):
        if self.net is None:
            print("network not available...")
            raise Exception("network not ready")
        else:
            return self.net.getNodeByName(who)

    def stopNetwork(self):
        if self.net is None:
            print("could not stop network... nothing to stop")
        else:
            self.net.stop()

class MpXpRunner:
    def __init__(self,topoParamFile):

        self.topoParamObj=MpParamTopo(topoParamFile)

        # so far so good

        self.topoBuilder=MininetBuilder()

        #should be no problem up to this point

        self.mpTopo=MpTopo(self.topoBuilder,self.topoParamObj)

        self.mpTopoConfig=MpConfig(self.mpTopo,self.topoParamObj)

        #start topo
        self.mpTopo.startNetwork()
        self.mpTopoConfig.configureNetwork()

        #strat experiment
        #MpExperienceQUIC()

        #stop topo
        self.mpTopo.stopNetwork()


if __name__=='__main__':
    parseArgs(sys.argv[1:])
    MpXpRunner(topoParamFile)
