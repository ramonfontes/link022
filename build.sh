#!/bin/bash

# Build Link022 agent.

export GOROOT=/usr/local/go
export GOPATH=$HOME/go

go build -o binary/link022_agent agent/agent.go
