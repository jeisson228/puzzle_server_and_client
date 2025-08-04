from fastapi import FastAPI, HTTPException, Query
import uvicorn
import os
import random
import json
import logging
import sys
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduced logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ],
    force=True  # Force reconfiguration
)

logger = logging.getLogger(__name__)

# Add startup log
print("Starting Request Engine API server...")  # Direct print for immediate visibility
logger.info("Starting Request Engine API server...")

# Global cache for JSON data
_json_cache = {}
_cache_loaded = False
_keys_list = []  # Cache the keys list

app = FastAPI(
    title="Request Engine API",
    description="A simple FastAPI server with GET endpoint",
    version="1.0.0"
)

def read_json_file(file_name: str) -> dict:
    """
    Read a JSON file and return its content as a dictionary
    Uses caching to avoid re-reading the file on every request
    
    Args:
        file_name (str): Name of the JSON file to read
        
    Returns:
        dict: Content of the JSON file as a dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
        Exception: For other file reading errors
    """
    global _json_cache, _cache_loaded, _keys_list
    
    # Return cached data if already loaded
    if _cache_loaded and file_name in _json_cache:
        return _json_cache[file_name]
    
    # Check if file exists
    if not os.path.exists(file_name):
        logger.error(f"File not found: {file_name}")
        raise FileNotFoundError(f"File '{file_name}' not found")
    
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Cache the data and keys list
            _json_cache[file_name] = data
            _keys_list = list(data.keys())
            _cache_loaded = True
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_name}: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error reading file {file_name}: {str(e)}")
        raise

def get_cached_json_data(file_name: str) -> dict:
    """
    Get JSON data from cache or load it if not cached
    
    Args:
        file_name (str): Name of the JSON file to get
        
    Returns:
        dict: Content of the JSON file as a dictionary
    """
    return read_json_file(file_name)

async def wait_for_it():  # Commented out for performance
    """
    Sleep for a random time between 100 and 400 milliseconds
    """
    sleep_time = random.uniform(0.1, 0.4)  # Random time between 100-400ms
    await asyncio.sleep(sleep_time)
    logger.info(f"Waited for {sleep_time:.3f} seconds")



@app.get("/")
async def root():
    """Root endpoint that returns a welcome message"""
    print("Root endpoint accessed")  # Direct print for immediate visibility
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Request Engine API!", "status": "success"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    print("Health check endpoint accessed")  # Direct print for immediate visibility
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "service": "request_engine"}

@app.get("/fragment")
async def get_data(
    id: int = Query(..., description="Index of the key to retrieve (0-based)")
):
    """
    Main data endpoint that reads a JSON file and returns a specific key-value pair
    
    Args:
        file_name (str): Name of the JSON file to read
        key_index (int): Index of the key to retrieve (0-based)
        
    Returns:
        dict: JSON response with the requested key-value pair and metadata
    """
    file_name = 'lorem_ipsum.json'
    asked_id = str(id)
    
    try:
        json_data = get_cached_json_data(file_name)
        
        if asked_id not in json_data:
            # Use cached keys list for better performance
            asked_id = _keys_list[random.randint(0, len(_keys_list) - 1)]

        await wait_for_it()
        return json_data[asked_id]
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Execution failed at line {sys.exc_info()[2].tb_lineno}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server with uvicorn
    logger.info("Starting uvicorn server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")  # Removed reload for production

