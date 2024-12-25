# Personal AI Assistant Project

This project consists of multiple services to create a personal AI assistant capable of handling tasks such as voice-to-text, text-to-speech, and text processing. The services are containerized using Docker.

## Services

1. **Redis:** In-memory data structure store used as a database, cache, and message broker.

2. **Voice-to-Text:** Converts spoken language into text. Utilizes PulseAudio for audio communication and NVIDIA GPU for processing.

3. **VLLM Server:** Serves the VLLM model for language tasks. Uses NVIDIA GPU for optimized performance.

4. **Text Processing:** Handles various text processing tasks. Depends on Redis and VLLM Server.

5. **Text-to-Speech:** Converts text into spoken language. Utilizes PulseAudio for audio communication and NVIDIA GPU for processing.

## Features

- **Offline Capable:** The assistant can run in an offline environment as the models are hosted locally. This means you can have full functionality without needing an internet connection.
- **Local Deployment:** With most people owning gaming PCs equipped with powerful GPUs, this setup can leverage local hardware for high performance, making it an ideal personal assistant.

## Getting Started

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Ensure you have Docker and Docker Compose installed.

3. Create a `.env` file with the required environment variables. Example `.env` file:
    ```dotenv
    # Specifies which GPUs to use (all in this case)
    NVIDIA_VISIBLE_DEVICES=all

    # Redis server host IP address
    REDIS_HOST=<your_redis_host_ip>

    # Redis server port
    REDIS_PORT=6379

    # VLLM server host IP address
    VLLM_HOST=<your_vllm_host_ip>

    # VLLM server port
    VLLM_PORT=8000
    ```

4. Build and run the services:
    ```bash
    docker-compose up --build
    ```

## Contributions

Feel free to open issues or submit pull requests. Contributions to improve this project are welcome.

