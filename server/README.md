# Request Engine API Server

A FastAPI server that serves JSON fragments from a lorem ipsum dataset.

## Features

- **FastAPI** server with async endpoints
- **Caching** for JSON data to improve performance
- **Health check** endpoint for monitoring
- **Random delay simulation** (100-400ms) for realistic testing
- **Docker** support for easy deployment

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /fragment?id={index}` - Get a specific fragment by ID

## Docker Setup

### Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

### Building and Running

#### Option 1: Using Docker directly

```bash
# Build the Docker image
docker build -t request-engine .

# Run the container
docker run -p 8000:8000 request-engine
```

#### Option 2: Using Docker Compose (recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### Testing the API

Once the server is running, you can test it using the provided HTTP files:

```bash
# Test the health endpoint
curl http://localhost:8000/health

# Test the fragment endpoint
curl http://localhost:8000/fragment?id=1

# Or use the provided HTTP files in the testing/ directory
```

### Development Mode

For development with live code changes, uncomment the volume mounts in `docker-compose.yml`:

```yaml
volumes:
  - ./request_engine.py:/app/request_engine.py
  - ./create_json_from_text.py:/app/create_json_from_text.py
  - ./lorem_ipsum.json:/app/lorem_ipsum.json
  - ./raw_lorem_ipsum.txt:/app/raw_lorem_ipsum.txt
```

## Project Structure

```
server/
├── request_engine.py          # Main FastAPI application
├── create_json_from_text.py   # Utility for creating JSON from text
├── lorem_ipsum.json          # Data file
├── raw_lorem_ipsum.txt       # Raw text data
├── requirements.txt           # Python dependencies
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── .dockerignore             # Docker ignore file
├── testing/                  # HTTP test files
│   ├── lorem_ipsum-1.http
│   ├── lorem_ipsum--1.http
│   └── lorem_ipsum-10000.http
└── README.md                 # This file
```

## Dependencies

- FastAPI 0.104.1
- Uvicorn 0.24.0 (with standard extras)
- Pydantic 2.5.0

## Performance Features

- **JSON Caching**: Data is cached in memory after first load
- **Random Delays**: Simulates realistic response times (100-400ms)
- **Error Handling**: Comprehensive error handling with proper HTTP status codes
- **Logging**: Configurable logging with reduced verbosity for production

## Health Monitoring

The container includes a health check that monitors the `/health` endpoint every 30 seconds. 