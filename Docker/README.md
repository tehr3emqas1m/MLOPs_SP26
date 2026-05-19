<img width="360" height="294" alt="what-is-docker" src="https://github.com/user-attachments/assets/be5b57b9-2e97-4fe6-99a3-5fbeef70db9e" />



# Docker 

Docker is a containerization platform that packages applications with their dependencies into portable containers that run consistently across different environments.



---

## Core Concepts

### Docker Engine
The beating heart. A runtime that builds, runs, and manages containers on a host system.

### Docker Daemon
The quiet worker in the background. It listens, builds, runs, and distributes containers.

```bash
systemctl status docker      # check if it's alive
sudo systemctl start docker  # wake it up
sudo systemctl stop docker   # gentle shutdown
sudo systemctl enable docker # autostart on boot
systemctl is-enabled docker  # verify
```

### Docker Image
A **read‑only blueprint**. An image goes through a lifecycle:

**Build → Tag → Push → Pull → Run**

### Dockerfile
The recipe. A script that tells Docker how to bake your image, step by step.

### Docker Container
A **running instance** of an image. Isolated filesystem. Private process space. Its own little universe.

### Registry (Docker Hub / Private / 3rd Party)
The library. A place to store and share images.

- **Repositories** – collections of related images
- **Tags** – versions (e.g., `python:3.11-slim`)
- **Manifests** – image metadata
- **Layers** – cached, reusable building blocks

---

## The Docker Workflow (One‑Liner)

```
Write Dockerfile → Build image → Push to registry → Pull image → Run container → Manage lifecycle
```

---

## Docker Desktop + Docker Hub

| Tool | Purpose |
|------|---------|
| **Docker Desktop** | Local GUI + engine to manage containers on your machine |
| **Docker Hub** | Public cloud registry to share and download images |

🔗 [hub.docker.com](https://hub.docker.com/)

---

##  Mini Example 1: `hello-world`

```bash
docker pull hello-world   # pull from registry
docker run hello-world    # run it
```

---

## Mini Example 2: A Real Python Hello World

### 1. Create project directory

```bash
mkdir docker-hello-demo
cd docker-hello-demo
```

### 2. Virtual environment (just for education — we'll containerize anyway)

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install numpy pandas requests   # heavy, but we're learning
pip freeze > requirements.txt
```

### 3. Write a simple app

```bash
echo 'print("Hello from Docker!")' > app.py
```

### 4. Create a `Dockerfile`

```dockerfile
# Use a slim Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (leverage Docker layer caching)
COPY requirements.txt .

# Install dependencies (no cache = smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application
COPY app.py .

# Default command when container starts
CMD ["python", "app.py"]
```

### 5. Build & Run

```bash
docker build -t hello-demo .
docker run hello-demo
```

**Output:**  
```
Hello from Docker!
```

---

## Save & Load an Image (No Registry Needed)

```bash
docker save -o hello-demo.tar hello-demo   # save to file
docker load -i hello-demo.tar              # load back
docker run hello-demo                      # still works
```

---

## Clean Up

```bash
docker rmi -f hello-demo                   # remove image
docker images | grep hello-demo            # gone 
```

---

## Common Base Images

| Image | Purpose |
|-------|---------|
| `ubuntu` | General Linux environment |
| `alpine` | Extremely small, lightweight |
| `python` | Python preinstalled |
| `node` | Node.js ready |
| `nginx` | Web server |
| `openjdk` | Java environment |
| `scratch` | Completely empty (for the truly hardcore) |

> `python:3.11-slim` (used above) is a **Debian-based** Linux with Python on top — includes `/bin`, `/usr`, shell utils, package manager, and a minimal userspace. Not a full OS, but enough to feel like home.

---

## You Made It.

---
```

---

