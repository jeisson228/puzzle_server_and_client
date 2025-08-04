# Request Engine API - Technical Test

This project consists of a FastAPI server that serves JSON fragments with random delays, and a multi-threaded client that collects unique data.

## Project Structure

```
puzzle_server_and_client/
├── server/
│   ├── request_engine.py      # FastAPI server
│   ├── requirements.txt       # Server dependencies
│   ├── lorem_ipsum.json      # Data source
│   └── testing/              # HTTP test files
└── client/
    ├── async_ultra_fast.py   # Async client
    └── requirements.txt       # Client dependencies
```

### Server Analysis

The server (`server/request_engine.py`) was working correctly:
- Adds random delays of 100-400ms via `wait_for_it()` function
- Returns JSON objects with `id`, `index`, and `text` fields
- Handles out-of-range requests by randomizing the response

## How to Run

### 1. Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

For Windows/macOS: Install Docker Desktop
For Linux: Install Docker Engine and Docker Compose

### 2. Run the FastAPI Server with Docker Compose

```bash
# From the server directory
cd server
docker-compose up --build
```

Or to run in detached mode:

```bash
# From the server directory
cd server
docker-compose up --build -d
```

The server will start on `http://localhost:8000`

To stop the server:

```bash
# From the server directory
docker-compose down
```

### 3. Install Client Dependencies

```bash
# Open a new terminal
cd client
pip install -r requirements.txt
```

### 4. Run the Async Ultra Fast Client

```bash
# From the client directory
cd client
python async_ultra_fast.py
```

## Expected Behavior

With the fixes, you should now see:

- The server running on `http://localhost:8000`
- The client making async requests to collect unique data
- Real-time logging showing progress
- Final puzzle solution displayed
- Performance metrics showing completion time

## API Endpoints

- `GET /fragment?id={index}` - Get JSON fragment by index
- `GET /health` - Health check endpoint
- `GET /` - Root endpoint

## Performance

The async client is optimized for maximum throughput:
- 69+ requests per second
- Connection pooling and keep-alive
- DNS caching
- High connection limits

## Disclaimer

I inicially thought the task was to only create the client to solve the puzzle, as there was no url pinpointed to do that, got to understand i had to create the serve too. As there wasn't a "testing puzzle" i used the lorem ipsum with its 69 words

I attacked the problem from diferent standpoints until got it working in less than a second. 

important points:
It wasn't a specified requriment, so to avoid unnecesary IO operations, the server "reads" the puzzle information once, and keeps it cached. i am not sure if that is cheating but it was a blank rule so i took advantage

I am no expert in requesting frameworks so started using multithreading and was getting times over 30 seconds, the IA helped me to add and clean the usage of aiohttp and asyncio; but off course there was more debugging than developing so i had to clean it, like a lot

as the rules implies, the client, nor the server, 'can't' know how much puzzle pieces there is, so when url query goes over the length of the data, the server will return a random puzzle piece. I used that behaviour into the cliend script: the client will call the server (like 100 times), when there comes a repeated puzzle piece (because the lorem ipsum is 69 words) it will stop creating requests and wait for the now created requests to finish.

After all the requests are over, the received (and unrepeated) data is sorted by "index" and printed.

You will see some "create_json_from_text,py" file in the server folder, i was thinking it is possible to create a fully articulated api with different puzzles. As that was no the task, i didn't continue to pursue those endpoints.