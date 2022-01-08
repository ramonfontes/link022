""" Copyright 2018 Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""Emulator for link022. Refer to the README.md file for instructions.
"""

import os
import argparse
import netaddr
import logging

from mininet.log import setLogLevel, info
from mininet.term import makeTerm
import mininet.node

from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

logging.basicConfig(filename='/tmp/link022_emulator.log', level=logging.INFO)
logger = logging.getLogger()


def start_topo():
    """Create an empty network and add nodes to it.
    """

    net = Mininet_wifi(controller=None)

    target = net.addStation('target', ip='192.168.0.1/24')
    ctrlr = net.addHost('ctrlr', ip='10.0.0.2/8')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding Link\n")
    target.setMasterMode(intf='target-wlan0', ssid='ap1-ssid', channel='1', mode='n')
    net.addLink(target, ctrlr)

    info("*** Starting network\n")
    net.build()

    target.cmd('ifconfig target-eth1 10.0.0.1')
    #"../binary/link022_agent -ca=../demo/cert/server/ca.crt -cert=../demo/cert/server/server.crt -key=../demo/cert/server/server.key -eth_intf_name=target-eth1 -wlan_intf_name=target-eth2"
    makeTerm(target, title='agent', cmd="bash -c 'echo \"running agent...\" && ../binary/link022_agent -ca=../demo/cert/tls_cert_key/server/ca.crt -cert=../demo/cert/tls_cert_key/server/server.crt -key=../demo/cert/tls_cert_key/server/server.key -eth_intf_name=target-eth1 -wlan_intf_name=target-wlan0;'")

    #makeTerm(self._ctrlr, title='set_config',
     #        cmd="bash -c '/home/alpha/go/bin/gnmi_set -ca ../demo/cert/tls_cert_key/client/ca.crt -cert ../demo/cert/tls_cert_key/client/client.crt -key ../demo/cert/tls_cert_key/client/client.key -target_name www.example.com -target_addr 10.0.0.1:10162 -replace=/:@../tests/ap_config1.json;'")

    #"/home/alpha/go/bin/gnmi_set -ca ../demo/cert/tls_cert_key/client/ca.crt -cert ../demo/cert/tls_cert_key/client/client.crt -key ../demo/cert/tls_cert_key/client/client.key -target_name www.example.com -target_addr 10.0.0.1:10162 -replace=/:@../tests/ap_config1.json"

    info("*** Running CLI\n")
    CLI(net)

    os.system('pkill -9 -f \"xterm -title\"')

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    start_topo()
