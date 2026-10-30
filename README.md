# TP04 — Containerization and Big Data Environment Deployment Using Docker

**University:** University of El Oued  
**Faculty:** Faculty of Exact Sciences  
**Department:** Computer Science  
**Level:** Master 2 — Artificial Intelligence & Data Science  
**Module:** Big Data Analytics  
**Academic Year:** 2026/2027

---

## 1. Introduction

The objective of this practical work is to understand containerization using Docker and deploy a Python data-analysis application in containers.

The application uses a CSV dataset previously used in TP03. The dataset contains sales records, allowing us to analyze total sales, regional sales, product categories, missing values, and duplicate records.

This practical work demonstrates Docker images, containers, networks, port mapping, Docker Hub, and Docker Compose.

## 2. Tools and Environment

- Operating System: Windows 11
- Docker Desktop: 4.96.3
- Docker Engine: 29.9.2
- Docker Compose: 5.6.1
- Backend: WSL2
- Programming Language: Python 3.11
- Library: Pandas
- Dataset: train.csv
- Code Editor: Visual Studio Code

## 3. Task 1 — Docker Installation

Docker Desktop was installed and configured on Windows 11 using the WSL2 backend.

The installation was verified using:

```bash
docker version
docker info
```

Both commands executed successfully and confirmed that the Docker client and server were available.

A Docker Hub account was also configured.

**Docker Hub username:** `alyatoumi`

## 4. Task 2 — Docker Image

### 4.1 Python Application

A Python script named `analysis.py` was developed to analyze the sales dataset.

The script performs the following operations:

1. Loads the CSV dataset using Pandas.
2. Displays the number of rows and columns.
3. Identifies missing values and duplicate rows.
4. Calculates total sales.
5. Calculates sales by region and category.
6. Displays the top ten sub-categories by sales.

### 4.2 Dockerfile

The application was containerized using a Dockerfile containing the instructions `FROM`, `WORKDIR`, `COPY`, `RUN`, and `CMD`.

The base image was `python:3.11-slim`.

### 4.3 Building the Image

The following command was executed:

```bash
docker build -t tp04-analysis:1.0 .
```

The image was built successfully.

### 4.4 Running the Application

The application was tested using:

```bash
docker run --rm tp04-analysis:1.0
```

The analysis completed successfully.

### 4.5 Dataset Results

| Metric | Result |
|---|---:|
| Number of rows | 9,800 |
| Number of columns | 18 |
| Missing values | 11 |
| Duplicate rows | 0 |
| Total sales | 2,261,536.78 |

**Sales by region:**

| Region | Total Sales |
|---|---:|
| West | 710,219.6845 |
| East | 669,518.7260 |
| Central | 492,646.9132 |
| South | 389,151.4590 |

**Sales by category:**

| Category | Total Sales |
|---|---:|
| Technology | 827,455.8730 |
| Furniture | 728,658.5757 |
| Office Supplies | 705,422.3340 |

### 4.6 Docker Hub

The image was tagged, pushed to Docker Hub, and pulled using the following commands:

```bash
docker tag tp04-analysis:1.0 alyatoumi/tp04-analysis:1.0
docker push alyatoumi/tp04-analysis:1.0
docker pull alyatoumi/tp04-analysis:1.0
```

The push completed successfully, and Docker confirmed that the local image was up to date when pulling.

**Repository:** https://hub.docker.com/r/alyatoumi/tp04-analysis

## 5. Task 3 — Containers and Networks

### 5.1 Creating the Docker Network

A bridge network was created:

```bash
docker network create tp04-network
```

### 5.2 Creating Three Containers

Three containers were created from the published image using `docker create`, with the names:

- `tp04-c1`
- `tp04-c2`
- `tp04-c3`

All three containers were configured to use `tp04-network`.

### 5.3 Executing the Data Analysis

The containers were started, and their logs were inspected:

```bash
docker start tp04-c1 tp04-c2 tp04-c3
docker logs tp04-c1
docker logs tp04-c2
docker logs tp04-c3
```

Each container completed the analysis successfully and exited with code 0.

### 5.4 Testing Simultaneous Container Execution

After successfully executing the data analysis, the three original containers (`tp04-c1`, `tp04-c2`, and `tp04-c3`) were removed and recreated from the same Docker image to run simple Python HTTP servers.

All three containers were connected to the Docker network named `tp04-network`.

The container status was verified using:

```powershell
docker ps --filter "name=tp04-c"
```

The output confirmed that all three containers were running with the status `Up`.

Next, the Python data-analysis application was executed inside each running container using the following commands:

```powershell
docker exec tp04-c1 python /app/analysis.py
docker exec tp04-c2 python /app/analysis.py
docker exec tp04-c3 python /app/analysis.py
```

All three containers successfully processed the CSV dataset and produced identical results:

| Metric | Result |
|---|---:|
| Number of rows | 9,800 |
| Number of columns | 18 |
| Missing values | 11 |
| Duplicate rows | 0 |
| Total sales | 2,261,536.78 |

Each execution ended with the message:

```text
Analysis completed successfully!
```

After completing the data analysis, the containers remained in the `Up` state because their HTTP servers continued running.

**Result:** The three containers successfully executed the data-analysis application while remaining operational.

### 5.5 Testing Network Communication Between Containers

The Docker bridge network `tp04-network` was used to connect the three containers.

To verify network communication, an HTTP request was sent from `tp04-c1` to the HTTP server running inside `tp04-c2`.

The following command was executed:

```powershell
docker exec tp04-c1 python -c "import urllib.request; r=urllib.request.urlopen('http://tp04-c2:8000', timeout=5); print('HTTP Status:', r.status)"
```

The output was:

```text
HTTP Status: 200
```

The HTTP status code `200` confirms that `tp04-c1` successfully communicated with `tp04-c2` using Docker's internal container-name resolution.

**Result:** The network communication test was successful, demonstrating connectivity between containers on the same Docker network.

### 5.6 Port Mapping

A separate test container was launched with the port mapping:

```bash
-p 8080:8000
```

The HTTP server was accessible from Windows through:

`http://localhost:8080/`

The browser displayed the directory listing, confirming successful port forwarding from the host to the container.

This HTTP server was used only to test Docker networking and port mapping, not as the main data-analysis application.

## 6. Task 4 — Docker Compose

A `compose.yaml` file was created to define the data-analysis service.

```yaml
services:
  data-analysis:
    build: .
    container_name: tp04-analysis
    volumes:
      - ./data:/app/data:ro
    restart: "no"
```

The following commands were executed:

```bash
docker compose up --build
docker compose ps -a
docker compose down
```

**Results:**

- Docker Compose successfully built the image.
- The application processed the dataset successfully.
- The container exited with code 0.
- Docker Compose successfully removed the created container and default network.

### Question 1: What problem does Docker Compose solve?

Docker Compose simplifies the configuration and management of applications containing one or more services. It allows developers to define services, networks, and volumes in a single YAML file instead of manually executing multiple commands.

### Question 2: Compare `docker run` with `docker compose up`.

`docker run` creates and starts a container directly using command-line arguments.

`docker compose up` creates and starts services based on the definitions in a Compose configuration file. It is more convenient for applications with multiple services, networks, and volumes.

### Question 3: How could you extend the Compose project to include a database service?

A PostgreSQL database service could be added to `compose.yaml`.

The database would use environment variables for configuration and a named volume for persistent data storage.

The Python application could communicate with PostgreSQL through the service name on the Docker Compose network. The application code would also need to be updated to use the database.

## 7. Task 5 — Report Questions

### Question 1: What is Docker, and why is it useful in data-science projects?

Docker is a containerization platform that packages an application together with its dependencies into a portable image.

In data-science projects, Docker helps create reproducible environments, improves portability, simplifies deployment, and reduces dependency conflicts between different machines.

### Question 2: Explain the difference between a Docker image and a container.

A Docker image is a reusable, read-only template containing an application, its dependencies, and its configuration.

A Docker container is a runnable instance of an image.

The same image can be used to create multiple independent containers.

### Question 3: Explain the purpose of `FROM`, `WORKDIR`, `COPY`, `RUN`, and `CMD` in the Dockerfile.

| Instruction | Purpose |
|---|---|
| FROM | Specifies the base image used to build the application image. |
| WORKDIR | Sets the working directory inside the image. |
| COPY | Copies local files into the image. |
| RUN | Executes commands during the image-building process. |
| CMD | Specifies the default command executed when a container starts. |

## 8. Conclusion

This practical work successfully demonstrated the main concepts of Docker containerization.

A Python data-analysis application was packaged into a Docker image, tested locally, published to Docker Hub, and retrieved using Docker Pull.

Three containers executed the application successfully. Additional experiments demonstrated simultaneous container execution, Docker bridge networking, communication between containers, and host-to-container port mapping.

Docker Compose was used to automate the application deployment through a YAML configuration file.

The experiment illustrates how Docker can improve the reproducibility, portability, and deployment of Python data-analysis applications.



