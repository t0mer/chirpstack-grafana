# chirpstack-grafana

A minimal webhook receiver for [ChirpStack](https://www.chirpstack.io/) HTTP integration events. It accepts `up`, `status` and `join` events and appends each one to a local file (`up.json`, `status.json`, `join.json`).

> **Status:** early work in progress. The project name refers to a planned Grafana dashboard, but the repository currently contains only the webhook receiver in [`app/app.py`](app/app.py). There is no metrics exporter, Grafana dashboard, Dockerfile or `requirements.txt` yet.

## How it works

1. ChirpStack's HTTP integration sends each event as a `POST` to the configured URL, with the event type in the `event` query parameter (for example `/?event=up`).
2. The app reads the JSON body and appends it, one line per event, to a file named after the event type in the current working directory:

   | `event` | File |
   |---------|------|
   | `up` | `up.json` |
   | `status` | `status.json` |
   | `join` | `join.json` |

3. Any other event type is accepted but not stored.

## Requirements

* Python 3 with `fastapi`, `uvicorn`, `loguru` and `requests` (`requests` is imported but not used)
* A ChirpStack instance that can reach this app over HTTP

## Running

```bash
pip install fastapi uvicorn loguru requests
python app/app.py
```

The app listens on `0.0.0.0:8213`. The port and bind address are hard-coded. Swagger UI and ReDoc are disabled.

## ChirpStack setup

In ChirpStack, open your application, go to **Integrations → HTTP**, and set the event endpoint URL to:

```
http://<host>:8213/
```

ChirpStack appends `?event=<type>` to each request. Set **Payload encoding** to **JSON**: the app parses every body as JSON, so a Protobuf payload fails with an HTTP 500.

## Known limitations

* **The output files are not valid JSON.** Each line is Python's string form of the payload with single quotes replaced by double quotes, so values such as `True`, `False` and `None` (and strings that contain quotes) are not valid JSON.
* **Files grow without limit** and are written to the directory the app is started from.
* **No authentication.** Anyone who can reach port 8213 can append data to the files. Keep it on a trusted network.
* The startup log message says "Whatsapp Webhook is up and running", which is left over from another project.

## License

[Apache License 2.0](LICENSE)
