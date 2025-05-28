# MarkItDown Web

MarkItDown Web provides a web-based interface for the `markitdown` file conversion utility. It allows users to upload files through their browser and receive the converted Markdown output.

This application is built using Python and Flask, and is designed to be run with Docker using Gunicorn as the WSGI server for production.

## Features

*   Upload various file types supported by the core `markitdown` library.
*   View converted Markdown content directly in the browser.
*   Simple and clean user interface.
*   Containerized for easy deployment using Docker.
*   Uses Gunicorn for robust performance.

## Prerequisites

*   **For running with Docker:**
    *   Docker installed and running.
*   **For local development:**
    *   Python 3.10+
    *   `hatch` (for managing environments and running scripts as defined in `pyproject.toml`)
    *   Access to the `markitdown` local package (it's a dependency).

## How to Build and Run with Docker (Recommended for Production/Deployment)

1.  **Navigate to the root of the monorepo.**
    (This is the directory that contains the main `packages/` directory).

2.  **Build the Docker image:**
    ```bash
    docker build -t markitdown-web -f packages/markitdown-web/Dockerfile .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -d -p 5000:5000 markitdown-web
    ```
    *   `-d`: Runs the container in detached mode (in the background).
    *   `-p 5000:5000`: Maps port 5000 on your host to port 5000 in the container. You can change the host port if needed (e.g., `-p 8080:5000`).
    *   The application will be accessible at `http://localhost:5000` (or your server's IP/domain if deployed).

## How to Run Locally (For Development)

1.  **Navigate to the `markitdown-web` package directory:**
    ```bash
    cd packages/markitdown-web
    ```

2.  **Ensure the `markitdown` core package is installable.**
    Since `markitdown-web` depends on the local `markitdown` package, your Python environment needs to be able to find and install it. This is typically handled if both are part of the same monorepo and you're using a build system like Hatch that understands local path dependencies.
    *   One way using Hatch (from the monorepo root, assuming `markitdown` also uses Hatch):
        ```bash
        # From monorepo root
        hatch shell 
        # Then navigate to packages/markitdown-web
        cd packages/markitdown-web
        # Now install dependencies for markitdown-web which should find local markitdown
        hatch dep install 
        ```
    *   Alternatively, ensure `markitdown` is installed in your chosen Python environment.

3.  **Create a virtual environment and install dependencies (using Hatch from `packages/markitdown-web`):**
    *   To create/activate a dedicated environment for `markitdown-web` and install its dependencies:
        ```bash
        hatch shell
        ```
        This command (when run inside `packages/markitdown-web`) sets up an environment based on `markitdown-web/pyproject.toml`. If dependencies weren't installed in the previous step, this will also attempt to install them.

4.  **Run the Flask development server:**
    Once dependencies are installed and the environment is active:
    ```bash
    flask run --host=0.0.0.0 --port=5001
    ```
    *   This runs the app with Flask's built-in development server. It's recommended to use a different port (e.g., 5001) than the Docker default if you might run both.
    *   The application will be accessible at `http://localhost:5001`.

## How to Run Tests

1.  **Navigate to the `markitdown-web` package directory:**
    ```bash
    cd packages/markitdown-web
    ```

2.  **Run tests using Hatch:**
    ```bash
    hatch env run -e hatch-test test
    ```
    This will execute the tests defined in `packages/markitdown-web/tests/` using `pytest`.

## Key Dependencies

*   **Flask:** Micro web framework for Python.
*   **Gunicorn:** WSGI HTTP Server for UNIX.
*   **MarkItDown (local package):** The core library for file conversion.
*   Other dependencies are listed in `pyproject.toml`.

## Configuration

*   **Port:** The Docker container (using Gunicorn) listens on port `5000` by default.
*   **Workers (Gunicorn):** The Docker CMD is set to use 2 Gunicorn workers. This can be adjusted in the `Dockerfile`.
*   **Upload Folder:** Temporary files are stored in `tmp_uploads` within the application's source directory during processing.
*   **Secret Key:** A default `SECRET_KEY` is set in `app.py`. For actual production deployments beyond trusted local networks, this should be managed securely (e.g., via environment variables).

---

This README aims to provide a good starting point for users and contributors of the `markitdown-web` package.
