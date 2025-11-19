# simple-notes-app-203852-203862

## Notes Backend API

A simple Flask API for notes with CRUD operations, using SQLite and SQLAlchemy.

### Setup

1. Install dependencies (in the `notes_backend` folder):

```bash
pip install -r requirements.txt
```

2. Run the backend server (by default runs on port 3001):

```bash
export FLASK_RUN_PORT=3001
python run.py
```

The API docs will be available at: [http://localhost:3001/docs/](http://localhost:3001/docs/)

### API Example Requests

**Create a note:**

```bash
curl -X POST http://localhost:3001/notes/ -H "Content-Type: application/json" -d '{"title": "First Note", "content": "Hello world!"}'
```

**List notes:**
```bash
curl http://localhost:3001/notes/
```

**Get one note:**
```bash
curl http://localhost:3001/notes/1
```

**Update a note:**
```bash
curl -X PUT http://localhost:3001/notes/1 -H "Content-Type: application/json" -d '{"content": "Updated content"}'
```

**Delete a note:**
```bash
curl -X DELETE http://localhost:3001/notes/1
```

**Health check:**
```bash
curl http://localhost:3001/
```