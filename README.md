# LiteLLM Proxy for Google Vertex AI

This project provides a simple way to set up a LiteLLM proxy for Google Vertex AI, allowing you to use OpenAI-style endpoints for models like Gemini 2.5 Pro and Claude Sonnet 4.

## Features

*   **OpenAI-Compatible Endpoints:** Use the familiar OpenAI API format to interact with Google Vertex AI models.
*   **Model Support:** Pre-configured for `gemini-2.5-pro` and `claude-sonnet-4`.
*   **"Thinking" Parameter:** Supports the `thinking` parameter for Gemini models.
*   **Easy to Run:** Includes simple command scripts to start the proxy for different models.

## Installation

1.  Install the required Python packages:

    ```bash
    pip install "litellm[proxy]" uvicorn
    ```

## Configuration

The proxy is configured using a `proxy_config.yaml` file. This file specifies the model(s) to be served and the connection details for Google Vertex AI.

### Google Cloud Authentication

To use this proxy, you need to authenticate with Google Cloud. The recommended way is to use Application Default Credentials (ADC).

1.  **Install the Google Cloud CLI:** If you don't have it already, [install the Google Cloud CLI](https://cloud.google.com/sdk/docs/install).

2.  **Log in and create credentials:** Run the following command and follow the instructions to log in to your Google account:

    ```bash
    gcloud auth application-default login
    ```

    This command will create a `application_default_credentials.json` file in your user's configuration directory.

3.  **Find the credentials file path:** To get the absolute path to the `application_default_credentials.json` file, run the following command:

    *   **Windows (Command Prompt):**
        ```cmd
        echo %APPDATA%\gcloud\application_default_credentials.json
        ```
    *   **Windows (PowerShell):**
        ```powershell
        Join-Path $env:APPDATA "gcloud\application_default_credentials.json"
        ```
    *   **Linux/macOS:**
        ```bash
        echo $HOME/.config/gcloud/application_default_credentials.json
        ```

    Copy the output of this command, as you will need it for the `vertex_credentials` field in your configuration file.

### Configuration Files

This project includes two pre-configured YAML files:

*   `proxy_config.yaml`: For `gemini-2.5-pro`
*   `proxy_config.sonnet.yaml`: For `claude-sonnet-4`

You will need to edit these files to add your Google Cloud project ID and the path to your credentials file.

**`proxy_config.yaml` (for Gemini 2.5 Pro)**

```yaml
model_list:
  - model_name: gemini-2.5-pro
    litellm_params:
      model: vertex_ai/gemini-2.5-pro
      vertex_project: "YOUR_GCP_PROJECT_ID"
      vertex_location: "global"
      vertex_credentials: "PATH_TO_YOUR_CREDENTIALS_FILE"
router_settings:
  default_model: gemini-2.5-pro
```

**`proxy_config.sonnet.yaml` (for Claude Sonnet 4)**

```yaml
model_list:
  - model_name: claude-sonnet-4
    litellm_params:
      model: vertex_ai/claude-sonnet-4@20250514
      vertex_project: "YOUR_GCP_PROJECT_ID"
      vertex_location: "us-east5"
      vertex_credentials: "PATH_TO_YOUR_CREDENTIALS_FILE"
router_settings:
  default_model: claude-sonnet-4
```

**Replace the following placeholders:**

*   `YOUR_GCP_PROJECT_ID`: Your Google Cloud project ID.
*   `PATH_TO_YOUR_CREDENTIALS_FILE`: The absolute path to your `application_default_credentials.json` file that you obtained in the previous step. **Important:** Use forward slashes (`/`) in the path, even on Windows.

## Running the Proxy

This project includes scripts to easily start the proxy for each model:

*   **For Gemini 2.5 Pro:**
    ```bash
    start_gemini_proxy.cmd
    ```

*   **For Claude Sonnet 4:**
    ```bash
    start_sonnet_proxy.cmd
    ```

You can also run the proxy directly with `litellm`:

```bash
litellm --config proxy_config.yaml
```

The proxy will start on `http://localhost:8000`.

## Usage

Once the proxy is running, you can send requests to it using the OpenAI API format.

### cURL Example

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-pro",
    "messages": [{"role": "user", "content": "Explain the theory of relativity."}],
    "thinking": {"type": "enabled", "budget_tokens": 1024}
  }'
```