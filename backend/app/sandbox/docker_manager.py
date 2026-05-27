import docker
import logging
from typing import Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class SandboxManager:
    def __init__(self):
        try:
            self.client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
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
            except docker.errors.NotFound:
                pass

            container = self.client.containers.run(
                settings.SANDBOX_DOCKER_IMAGE,
                detach=True,
                name=container_name,
                network_mode="none",  # Isolate from network by default
                mem_limit="512m",
                cpu_quota=50000,      # 50% of one CPU
                user="devuser",       # Run as non-root
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
