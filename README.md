# etl-wizard

Script to replicate databases from Source to Origin\
Could be all the data or specific ones

## Usage

Run Docker Compose (without reload)

```bash
docker-compose up --build
```

With Auto Reload

```bash
uvicorn api.main:app --reload
```
