# Agent

This directory contains the WiFi management component that runs on Hostapd AP.

## Get Started
For documentation on installing a full demo system (with both a gNMI client and link022 access point)
please see the [full demo documentation](../demo/README.md) which explains a fully complete system.

The following instructions will get you a Link022 AP on a Linux-based device.

### Prerequisites

Install Golang:
```
For other systems:
Install golang 1.7+ (get it from: https://golang.org/doc/install#install)
```

Set up Path:
```
export PATH=$PATH:/usr/local/go/bin
```

### Download Link022 agent
```
export GOPATH=$HOME/go
go get github.com/ramonfontes/link022/agent
```