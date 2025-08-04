import asyncio
import aiohttp
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def make_async_request(session, arg):
    """Async request for maximum throughput"""
    url = f"http://localhost:8000/fragment?id={arg}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=1)) as response:
            if response.status == 200:
                data = await response.json()
                return {'status': 'success', 'arg': arg, 'data': data}
            else:
                return {'status': 'failed', 'error': f'Status {response.status}', 'arg': arg}
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'arg': arg}

async def collect_unique_data_async():
    """Async version for maximum speed - 69+ requests per second"""
    seen_ids = set()
    all_results = []
    unique_count = 0
    found_first_duplicate = False
    
    # Configure async session for maximum performance
    connector = aiohttp.TCPConnector(
        limit=200,  # High connection limit
        limit_per_host=100,  # High per-host limit
        ttl_dns_cache=300,  # DNS caching
        use_dns_cache=True,
        keepalive_timeout=30,
        enable_cleanup_closed=True
    )
    
    timeout = aiohttp.ClientTimeout(total=1)
    
    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={'Connection': 'keep-alive'}
    ) as session:
        
        tasks = set()
        request_id = 0
        
        while not found_first_duplicate or tasks:
            
            # Submit new requests only if we haven't found a duplicate yet
            while len(tasks) < 100 and not found_first_duplicate:
                request_id += 1
                task = asyncio.create_task(make_async_request(session, request_id))
                tasks.add(task)
            
            # Process completed tasks
            if tasks:
                done, pending = await asyncio.wait(tasks, timeout=0.01)
                tasks = pending
                
                for task in done:
                    result = await task
                    
                    if result['status'] == 'success':
                        data_key = result['data']['id']
                        
                        if data_key not in seen_ids:
                            seen_ids.add(data_key)
                            all_results.append(result['data'])
                            unique_count += 1
                            if unique_count % 5 == 0:
                                logger.info(f"🚀 Async: New data #{unique_count}")
                        else:
                            # Found first duplicate - stop submitting new requests
                            found_first_duplicate = True
                            logger.info(f"Found first duplicate (ID: {data_key}), stopping new requests")
    
    return all_results

def process_api_results(all_api_results):
    sorted_records = sorted(all_api_results, key=lambda item:item['index'])
    message = ' '.join([record['text'] for record in sorted_records])
    logger.warning(f'Puzzle resuelto\n{message}')


def run():
    start_time = datetime.now()
    all_api_results = asyncio.run(collect_unique_data_async())
    process_api_results(all_api_results)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f'Puzzle resolved in {duration} seconds')
    input('To exit, press any key: ')

if __name__ == "__main__":
    run()