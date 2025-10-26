pipeline {
    agent any

    environment {
        REPO_URL      = 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
        APP_NAME      = 'roblox_app'
        IMAGE_NAME    = 'roblox-webapp'
        INTERNAL_PORT = '5000'
        EXTERNAL_PORT = '5050'
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo "Checking out source..."
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        stage('Build & Setup (Containerized)') {
            steps {
                echo "Installing dependencies inside Python container..."
                bat """
                docker run --rm -v "%cd%:/app" -w /app python:3.11-slim ^
                  sh -c "pip install --upgrade pip && pip install -r requirements.txt"
                """
            }
        }

        stage('Run Unit Tests (in container)') {
            steps {
                echo "Running unit tests inside Python container..."
                bat """
                if not exist tests (
                    echo No tests folder found. Skipping tests.
                ) else (
                    docker run --rm -v "%cd%:/app" -w /app python:3.11-slim ^
                      sh -c "pip install -r requirements.txt pytest requests && pytest -q --maxfail=1 --disable-warnings"
                )
                """
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image..."
                bat """
                docker build -t %IMAGE_NAME%:latest .
                """
            }
        }

        stage('Docker Test Run') {
            steps {
                echo "Running Docker container and health check..."
                bat """
                docker rm -f %APP_NAME% 1>nul 2>&1 || echo No previous container found.
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest

                echo Checking if app is reachable on port %EXTERNAL_PORT% ...
                powershell -Command ^
                  "$max=12; for ($i=0; $i -lt $max; $i++) { try { Invoke-WebRequest -UseBasicParsing -Uri http://localhost:%EXTERNAL_PORT% -TimeoutSec 5 | Out-Null; Write-Host 'App OK!'; exit 0 } catch { Write-Host 'Waiting for app... ' ($i+1); Start-Sleep -Seconds 5 } } ; Write-Error 'App did not start'; exit 1"
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo Logging in to Docker Hub...
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker tag %IMAGE_NAME%:latest %DOCKER_USER%/%IMAGE_NAME%:latest
                    docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                    docker logout
                    """
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up containers..."
            bat """
            docker stop %APP_NAME% 1>nul 2>&1 || echo No container to stop
            docker rm %APP_NAME% 1>nul 2>&1 || echo No container to remove
            exit /b 0
            """
        }
        success {
            echo "✅ Pipeline success! Image built and pushed successfully."
        }
        failure {
            echo "❌ Pipeline failed. Check console output for details."
        }
    }
}
