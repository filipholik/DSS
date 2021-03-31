#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def DssTopo():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='1.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=OVSController,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    GATEWAY = net.addSwitch('GATEWAY', cls=OVSKernelSwitch, dpid='1',failMode='standalone')
    RTU = net.addSwitch('RTU', cls=OVSKernelSwitch, dpid='2',failMode='standalone')    

    info( '*** Add hosts\n')
    TTS1 = net.addHost('TTS1', cls=Host, ip='1.1.1.1', defaultRoute=None)
    TTS2 = net.addHost('TTS2', cls=Host, ip='1.1.1.2', defaultRoute=None)
    TTS3 = net.addHost('TTS3', cls=Host, ip='1.1.1.3', defaultRoute=None)
    MM1 = net.addHost('MM1', cls=Host, ip='1.1.2.1', defaultRoute=None)
    MM2 = net.addHost('MM2', cls=Host, ip='1.1.2.2', defaultRoute=None)
    MM3 = net.addHost('MM3', cls=Host, ip='1.1.2.3', defaultRoute=None)   
    CONTROL = net.addHost('CONTROL', cls=Host, ip='1.10.10.10', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(GATEWAY, RTU)
    net.addLink(GATEWAY, CONTROL)
    net.addLink(TTS1, RTU)
    net.addLink(TTS2, RTU)
    net.addLink(TTS3, RTU)
    net.addLink(MM1, RTU)
    net.addLink(MM2, RTU)
    net.addLink(MM3, RTU)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('GATEWAY').start([])
    net.get('RTU').start([])

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    DssTopo()

