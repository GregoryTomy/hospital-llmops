"""
This script leverages FastAPI's asynchronous serving capabilities to handle multiple requests 
efficiently. By making use of asynchronous programming, the script can initiate multiple requests 
to an external server, such as OpenAI's models, in succession, reducing overall latency.

Additionally, the script implements retry logic for handling intermittent connection issues with
services like Neo4j. When encountering connection errors or timeouts, the script gracefully retries
failed operations without blocking the execution of other tasks. 
"""
import asyncio

def async_retry(max_retries: int=3, delay: int=1):
    """Decorator function for retrying asynchronous functions.

    Args:
        max_retries (int, optional): Maximum number of retries. Defaults to 3.
        delay (int, optional): Delay in seconds between retry attempts. Defaults to 1.
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Attempt {attempt} failed: {str(e)}")
                    await asyncio.sleep(delay)
            
            raise ValueError(f"Failed after {max_retries} attempts")

        return wrapper
    
    return decorator
