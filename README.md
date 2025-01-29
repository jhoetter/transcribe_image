# adalace-template-01

First template code for adalace

To run as part of a docker compose stack:

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

To run as a standalone server:

1. activate the venv
2. run the server with

```bash
cd backend
python app.py
```

3. run the worker with

```bash
cd backend
python app.py worker
```

4. run the frontend with

```bash
cd frontend
npm run dev
```
