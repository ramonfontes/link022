"""
Emulation with support for OpenConfig/WiFi. Refer to the README.md file for instructions.

@author: Ramon Fontes
@Github: https://github.com/ramonfontes/link022

"""

import os
import logging

from mininet.log import setLogLevel, info
from mininet.term import makeTerm

from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

logging.basicConfig(filename='/tmp/link022_emulator.log', level=logging.INFO)
logger = logging.getLogger()


def topology():

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    # Creating our AP - This can be replaced by addAccessPoint() running at a particular NS
    # IP address is required!
    ap1 = net.addStation('ap1', ip='192.168.0.1/24')
    # This station is not mandatory but we can use it to validate ou AP
    net.addStation('sta1', ip='192.168.0.2/24')
    # Creating our controller that will be used with gnmi
    c1 = net.addHost('c1', ip='10.0.0.2/8')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    ap1.setMasterMode(intf='ap1-wlan0', ssid='ap1-ssid', channel='1', mode='n')
    net.addLink(ap1, c1)

    info("*** Starting network\n")
    net.build()

    # Configuring IP address for the interface attached to c1
    ap1.cmd('ifconfig ap1-eth1 10.0.0.1')
    makeTerm(ap1, title='agent', cmd="bash -c 'echo \"running agent...\" "
                                     "&& ../binary/link022_agent -ca=../demo/cert/tls_cert_key/server/ca.crt "
                                     "-cert=../demo/cert/tls_cert_key/server/server.crt -key=../demo/cert/"
                                     "tls_cert_key/server/server.key -eth_intf_name=ap1-eth1 "
                                     "-wlan_intf_name=ap1-wlan0;'")
    makeTerm(c1, title='ctrl')

    info("*** Running CLI\n")
    CLI(net)

    os.system('pkill -9 -f \"xterm -title\"')

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
