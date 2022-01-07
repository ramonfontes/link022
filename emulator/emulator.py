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
import mininet.net
import mininet.node
import mininet.cli


logging.basicConfig(filename='/tmp/link022_emulator.log', level=logging.INFO)
logger = logging.getLogger()

TARGET_NAME = 'target'
CONTROLLER_NAME = 'ctrlr'
DUMMY_NAME = 'dummy'


class Emulator(object):
  """Link022 emulator."""

  def __init__(self):
    self._net = None
    self._ctrlr = None
    self._target = None

  def start(self):
    self._start_topo()
    logger.info('Emulator started.')
    mininet.cli.CLI(self._net)

  def _start_topo(self):
    """Create an empty network and add nodes to it.
    """

    self._net = mininet.net.Mininet(controller=None)

    self._net.addHost(TARGET_NAME, ip='10.0.0.1/8')
    self._net.addHost(CONTROLLER_NAME, ip='10.0.0.2/8')
    # We add a dummy host to create the eth and wlan interfaces for the
    # Target
    self._net.addHost(DUMMY_NAME)
    self._net.addLink(TARGET_NAME, CONTROLLER_NAME)
    self._net.addLink(TARGET_NAME, DUMMY_NAME)
    self._net.addLink(TARGET_NAME, DUMMY_NAME)

    self._target = self._net[TARGET_NAME]
    self._ctrlr = self._net[CONTROLLER_NAME]

    self._net.start()

    #"../binary/link022_agent -ca=../demo/cert/server/ca.crt -cert=../demo/cert/server/server.crt -key=../demo/cert/server/server.key -eth_intf_name=target-eth1 -wlan_intf_name=target-eth2"
    makeTerm(self._target, title='agent', cmd="bash -c 'echo \"running agent...\" && ../binary/link022_agent -ca=../demo/cert/tls_cert_key/server/ca.crt -cert=../demo/cert/tls_cert_key/server/server.crt -key=../demo/cert/tls_cert_key/server/server.key -eth_intf_name=target-eth1 -wlan_intf_name=target-eth2;'")

    #makeTerm(self._ctrlr, title='set_config',
     #        cmd="bash -c '/home/alpha/go/bin/gnmi_set -ca ../demo/cert/tls_cert_key/client/ca.crt -cert ../demo/cert/tls_cert_key/client/client.crt -key ../demo/cert/tls_cert_key/client/client.key -target_name www.example.com -target_addr 10.0.0.1:10162 -replace=/:@../tests/ap_config1.json;'")

    #"/home/alpha/go/bin/gnmi_set -ca ../demo/cert/tls_cert_key/client/ca.crt -cert ../demo/cert/tls_cert_key/client/client.crt -key ../demo/cert/tls_cert_key/client/client.key -target_name www.example.com -target_addr 10.0.0.1:10162 -replace=/:@../tests/ap_config1.json"

  def cleanup(self):
    """Clean up emulator."""
    if self._net:
      self._net.stop()
      os.system('pkill -9 -f \"xterm -title\"')
      logger.info('Emulator cleaned up.')

if __name__ == '__main__':
  setLogLevel('info')
  emulator = Emulator()
  try:
    emulator.start()
  finally:
    emulator.cleanup()
