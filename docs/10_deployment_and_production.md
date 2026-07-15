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

---
**Next Step:** Want a dictionary of all the functions? Check out [11. API Reference](11_api_reference.md).
