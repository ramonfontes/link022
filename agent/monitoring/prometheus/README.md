# OpenConfig Telemetry Exporter (Prometheus)

This directory contains an exporter that periodically collects AP's info via gNMI and exposes converted metrics to a web page. Prometheus can monitor AP's status by scraping that web page.

## Get Started

Follow steps below to set up environment and start exposition server

### Prerequisites

Change directory in terminal to this folder, then run below command.

```
go get -t ./...
```

### Compile Exporter

```
go build exposition_server.go openconfig_ap_exporter.go
```

This command will generate binary file named exposition_server.  

Note: The default location of exporter log file is  `/tmp/exposition_server.INFO`

## Running Mininet-WiFi

Go to [/emulator](https://github.com/ramonfontes/link022/tree/master/emulator) and run `emulator_monitoring.py`:

```
sudo python emulator_monitoring.py
```

## Monitoring In Prometheus

Follow steps below to set up Prometheus and monitoring AP status.  

### Prometheus Getting Started

You can get and run prometheus with docker by running the command below: 

```
docker run \
    -p 9090:9090 \
    -v {link022_dir}/agent/monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

### Configuring Prometheus to monitor AP

Save the following basic Prometheus configuration as a file named prometheus.yml

```
global:
  scrape_interval:     15s # Exposition server sends gNMI request every 15 seconds.

scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'link022'
    static_configs:
      # 10.0.0.4 is the IP address of wan0 node in Mininet-WiFi
      - targets: ['10.0.0.4:8080'] 
```

### Start Prometheus

Start Prometheus according to its official tutorial.  
By default, Prometheus admin page is localhost:9090.
You can see all exported AP status metrics in that page.