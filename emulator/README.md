# Link022 emulator
This doc contains steps to run a Link022 emulator.

The emulator builds a local testing environment with Link022 agent running inside a mininet node.

### Prerequisites
* Mininet-WiFi: (https://github.com/intrig-unicamp/mininet-wifi)[https://github.com/intrig-unicamp/mininet-wifi]

### 1. Setup environment
The setup needs some additional packages.
```
go get github.com/openconfig/goyang/pkg/yang
go get github.com/openconfig/ygot/experimental/ygotutils
```

### 2. Compile Link022 agent
Run the [build script](../build.sh) to compile the Link022 agent.
It stores output binary file in the "binary" folder.
```
./build.sh
```

### 3. Start emulator
Run the following command to start the network topology (two xterms terminals will open up automatically):
```
cd emulator

sudo python emulator.py
```

The mininet-wifi CLI should appear after emulator started.
```
mininet-wifi>
```

### 4. Verify the setup

### Check mininet nodes
```
mininet> nodes
available nodes are: 
ap1 c1 sta1
```

There are three nodes in mininet-wifi.
* `c1`: where gNMI client runs on.
* `ap1`: where Link022 agent runs on.
* `sta1`: a dummy station that can be used for tests.

### Check Link022 agent

The `ap1` node contains the following interfaces:
```
mininet> ap1 ifconfig
ap1-eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.0.1  netmask 255.0.0.0  broadcast 10.255.255.255
        inet6 fe80::8c24:3eff:fe73:dca2  prefixlen 64  scopeid 0x20<link>
        ether 8e:24:3e:73:dc:a2  txqueuelen 1000  (Ethernet)
        RX packets 15  bytes 1186 (1.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13  bytes 1006 (1006.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

ap1-wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.1  netmask 255.255.255.0  broadcast 192.168.0.255
        inet6 fe80::3490:9eff:fe21:bf96  prefixlen 64  scopeid 0x20<link>
        ether 36:90:9e:21:bf:96  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13  bytes 1280 (1.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
`ap1-eth1` is the management interface of the emulated AP, where gNMI target listens on (default port 10162).

The link022 agent process runs inside `ap1` node:
```
mininet-wifi> ap1 ps aux | grep ../binary/link022_agent
root       17193  0.0  0.1 1529392 17156 pts/4   Ssl+ 09:20   0:00 ../binary/link022_agent -ca=../demo/cert/tls_cert_key/server/ca.crt -cert=../demo/cert/tls_cert_key/server/server.crt -key=../demo/cert/tls_cert_key/server/server.key -eth_intf_name=ap1-eth1 -wlan_intf_name=ap1-wlan0
```

The link022 log is "/tmp/link022_agent.INFO" by default.

### 5. Config Link022 AP
All gNMI requests working on a physical Link022 AP should also work on the emulated one.
Run gNMI client in `c1` node.

Here are some examples to start with:

1. Download GNMI clients.
* Download and compile [gNXI "SET" client](https://github.com/google/gnxi/tree/master/gnmi_set).
* Download and compile [gNXI "GET" client](https://github.com/google/gnxi/tree/master/gnmi_get).

2. Pushing the entire configuration to AP. It wipes out the existing configuration and applies the incoming one. **Note**: Please replace the hostname fields in `../tests/ap_config.json` with your host information.
```
mininet-wifi> xterm c1
{path to gnmi_set binary} \ 
-ca ../demo/cert/tls_cert_key/client/ca.crt 
-cert ../demo/cert/tls_cert_key/client/client.crt 
-key ../demo/cert/tls_cert_key/client/client.key 
-target_name www.example.com 
-target_addr 10.0.0.1:10162 
-replace=/:@../tests/ap_config.json
```

3. Fetch AP configuration (please replace the hostname field below with your host information)
```
mininet-wifi> xterm c1
{path to gnmi_get binary} \ 
-ca ../demo/cert/tls_cert_key/client/ca.crt 
-cert ../demo/cert/tls_cert_key/client/client.crt 
-key ../demo/cert/tls_cert_key/client/client.key 
-target_name www.example.com 
-target_addr 10.0.0.1:10162 
-xpath "/access-points/access-point[hostname=alpha-Inspiron-5480]/radios/"
```

You can also try `xpath` with:
```
-xpath "/access-points/access-point[hostname=alpha-Inspiron-5480]/radios/radio[id=1]/config/channel"
```

The output should be similar to:
```
== getResponse:
notification: <
  timestamp: 1521145574058185274
  update: <
    path: <
      elem: <
        name: "access-points"
      >
      elem: <
        name: "access-point"
        key: <
          key: "hostname"
          value: "alpha-Inspiron-5480"
        >
      >
      elem: <
        name: "radios"
      >
      elem: <
        name: "radio"
        key: <
          key: "id"
          value: "1"
        >
      >
      elem: <
        name: "config"
      >
      elem: <
        name: "channel"
      >
    >
    val: <
      uint_val: 8
    >
  >
>
```
