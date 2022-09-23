# Foptimum

[![Docker Pulls](https://badgen.net/docker/pulls/roseatoni/foptimum?icon=docker&label=pulls)](https://hub.docker.com/r/roseatoni/foptimum)
[![Image Size](https://badgen.net/docker/size/roseatoni/foptimum?icon=docker&label=size)](https://hub.docker.com/r/roseatoni/foptimum)

Foptimum is a lightweight, dockerized app to monitor your internet speed and uptime so you can keep your ISP accountable.

Foptimum exports its data to [Prometheus](https://prometheus.io/docs/introduction/overview/) so it can easily be visualized with a tool like [Grafana](https://grafana.com/).

# Deployment

## Docker

---

The Docker image is [available on Docker Hub](https://hub.docker.com/r/roseatoni/foptimum). Pull the container using the following command:

```
docker pull roseatoni/foptimum
```

All variables are passed to the program as environment variables. These variables are:

| Variable Name      | Description                                 | Recommended Value |
| ------------------ | ------------------------------------------- | ----------------- |
| SPEEDTEST_INTERVAL | How often (in seconds) to run the speedtest | 900 (15 min)      |
| PING_INTERVAL      | How often (in seconds) to ping all servers  | 15                |
| SERVER_LIST        | A comma delimited list of IPs to ping       | 1.1.1.1,8.8.8.8   |

The Prometheus server is exposed in the container on port 9191. When deploying this container, map port 9191 to your desired host port.

Putting it all together, here is an example Docker run command:

```
docker run -d -p 9191:9191 -e SPEEDTEST_INTERVAL=900 -e PING_INTERVAL=15 -e SERVER_LIST=1.1.1.1,8.8.8.8 roseatoni/foptimum:latest
```

## unRAID

---

This application has also been added to the unRAID community apps store.

# Grafana

A very basic Grafana dashboard has been added to this repository to get you started with visualizing the data. Download _Grafana_Dashboard.json_ and import it into your Grafana instance.

# Logs

If you do not have a means of visualizing the Prometheus data, you can also manually look at the logs to identify internet outages.

Logs are written to a file called _app.log_. So, you can read the logs by running a command such as:

```
docker exec dc5a365ad9a572863a3cdeb3f2a3c3c82034fe669c74e75df1730469286e335e tail -n 100 app.log
```

One thing that the logs can provide that Grafana can not is the IP address of failed pings. This allows you to determine if your internet is really down, or it is just one of the servers you chose to ping.
