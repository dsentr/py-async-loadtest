import aiohttp
import asyncio
from async_timeout import timeout
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('url', help='The URL of the website to load test')
parser.add_argument('-n', '--num-requests', type=int, default=10, help='The number of requests to send')
args = parser.parse_args()

class LoadTester:
    def __init__(self, url, num_requests):
        self.url = url
        self.num_requests = num_requests

    def run(self):
        # Create an asyncio session
        session = aiohttp.ClientSession()

        def close_session():
            session.close()

        tasks = []
        for i in range(self.num_requests):
            # Create a task to send a request to the website with a timeout of 5 seconds
            task = asyncio.ensure_future(self.load_test(session))
            tasks.append(task)

        # Run the tasks and close the session when they are complete
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        finally:
            loop.run_until_complete(session.close())
            loop.close()

    async def load_test(self, session):
        with timeout(5):
            async with session.get(self.url) as response:
                print(f'Request {i+1}: {response.status}')

# Create a LoadTester object and run the load test
tester = LoadTester(args.url, args.num_requests)
tester.run()
