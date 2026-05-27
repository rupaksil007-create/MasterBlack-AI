import docker
import logging
import os
from typing import Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class SandboxManager:
    def __init__(self):
        self.client = None
        
        # 🛡️ THE FIX: Hardcode the unix socket and bypass environment detection
        # This prevents the "http+docker" scheme error caused by mangled DOCKER_HOST values.
        try:
            # Clear any problematic vars that cause scheme resolution issues
            for key in ["DOCKER_HOST", "DOCKER_TLS_VERIFY", "DOCKER_CERT_PATH", "DOCKER_URL"]:
                os.environ.pop(key, None)

            # Use the absolute most direct path for Linux sockets in Docker-in-Docker
            socket_path = "unix:///var/run/docker.sock"
            print(f"DEBUG: Initializing Docker client with {socket_path}")
            self.client = docker.DockerClient(base_url=socket_path)
            
            # Immediate check
            self.client.ping()
            print(f"DEBUG: Docker client initialized successfully via {socket_path}")
            logger.info(f"Docker client initialized successfully via {socket_path}")
            
        except Exception as e:
            print(f"DEBUG: FATAL Docker initialization failed: {e}")
            logger.error(f"FATAL: Docker initialization failed: {e}")
            self.client = None

    def create_sandbox(self, session_id: str) -> Optional[str]:
        """Creates a new isolated Docker container for a session."""
        if not self.client:
            logger.error("Docker client not initialized")
            return None
        
        container_name = f"masterblack-sandbox-{session_id}"
        
        try:
            # Check if container already exists
            try:
                container = self.client.containers.get(container_name)
                return container.id
            except Exception:
                pass

            container = self.client.containers.run(
                settings.SANDBOX_DOCKER_IMAGE,
                detach=True,
                name=container_name,
                network_mode="none",
                mem_limit="512m",
                cpu_quota=50000,
                user="devuser",
                volumes={
                    f"{settings.WORKSPACE_ROOT}/{session_id}": {
                        "bind": "/home/devuser/workspace",
                        "mode": "rw"
                    }
                },
                tty=True,
                stdin_open=True,
                command="/bin/bash"
            )
            return container.id
        except Exception as e:
            logger.error(f"Failed to create sandbox: {e}")
            return None

    def execute_command(self, container_id: str, command: str) -> Dict[str, Any]:
        """Executes a command inside the specified container."""
        if not self.client:
            return {"error": "Docker client not initialized"}
        
        try:
            container = self.client.containers.get(container_id)
            exec_result = container.exec_run(
                command,
                user="devuser",
                workdir="/home/devuser/workspace"
            )
            return {
                "exit_code": exec_result.exit_code,
                "output": exec_result.output.decode("utf-8")
            }
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            return {"error": str(e)}

    def stop_sandbox(self, container_id: str):
        """Stops and removes the sandbox container."""
        if not self.client:
            return
        
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
        except Exception as e:
            logger.error(f"Failed to stop sandbox: {e}")

sandbox_manager = SandboxManager()
