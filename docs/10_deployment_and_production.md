# 10. Deployment & Production

When you move your code from your laptop to a real server (like AWS, Google Cloud, or a Docker container), you need to think about how logs are handled.

## Using TraceNest in Docker

If you are running your app inside a Docker container, saving files to `logs/app.log` might be a bad idea, because Docker containers are temporary! If the container restarts, your logs get deleted.

**The Solution: Use Docker Volumes**

You should mount a Volume to your Docker container so that the logs are saved to your actual host computer, not inside the temporary container.

```yaml
# docker-compose.yml example
version: '3'
services:
  my_api:
    image: my_api_image
    ports:
      - "8000:8000"
    volumes:
      # Map the /app/logs folder in the container to a permanent folder on your server
      - ./server_logs:/app/logs
```

Now, TraceNest will save the logs into `/app/logs` inside the container, but Docker will automatically save them permanently to `./server_logs` on your hard drive!

## Production Best Practices

1. **Keep Retention Low:** In production, do not set `backup_count` to 365 days. Keeping a year of logs on a small web server will fill up your hard drive. Set it to 7 or 14 days.
2. **Use the UI Securely:** The TraceNest Web Dashboard does not have a login screen built-in! If you mount the dashboard on a public server (`http://mywebsite.com/logs`), **anyone in the world can read your logs.**
   * *Fix:* Use a reverse proxy like NGINX, or FastAPI's built-in authentication, to put a password in front of the `/logs` URL.
3. **Enjoy the Speed:** Because TraceNest uses Asynchronous logging, it is perfectly safe to use in high-traffic production environments. It will not slow down your app!

## Under the Hood (Technical Context)
**Multiprocessing and Concurrency in Production:**
When deploying a FastAPI app using Gunicorn and Uvicorn workers (`gunicorn -k uvicorn.workers.UvicornWorker -w 4`), Gunicorn forks your application into 4 completely separate Python processes.
Each of those 4 processes will instantiate its own `AsyncFileHandler`, and thereby its own internal `queue.Queue` and daemon `threading.Thread`.

Because multiple processes are attempting to write to the exact same `app.log` file simultaneously, you might experience file interleaving or locking issues on Windows. However, on Linux/POSIX systems (which run most Docker containers), appending to a file (`mode='a'`) of size smaller than the OS block size (usually 4KB) is guaranteed to be atomic by the kernel. 
TraceNest relies on this POSIX guarantee in production to ensure high-throughput multiprocessing without using heavy inter-process locks.

---
**Next Step:** Want a dictionary of all the functions? Check out [11. API Reference](11_api_reference.md).
