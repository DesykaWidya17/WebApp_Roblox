pipeline {
    agent any

    environment {
        REPO_URL      = 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
        APP_NAME      = 'roblox_app'
        IMAGE_NAME    = 'roblox-webapp'
        INTERNAL_PORT = '5000'
        EXTERNAL_PORT = '5050'
        DOCKER_USER   = ''   // optional: replace or use credential below
    }

    stages {

        stage('Checkout SCM') {
            steps {
                echo "Checking out source..."
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        /*
         * Build & tests run inside containers so we don't require python/pip on agent
         */
        stage('Build & Setup (Containerized)') {
            steps {
                echo "Preparing build/test environment inside Python Docker image..."
                // Use Docker to install dependencies inside a throwaway container
                bat """
                docker run --rm -v "%cd%:/app" -w /app python:3.11-slim ^
                  sh -c "pip install --upgrade pip && pip install -r requirements.txt"
                """
            }
        }

        stage('Run Unit Tests (in container)') {
            steps {
                echo "Running unit tests inside Python container (if tests exist)..."
                bat """
                if not exist tests (
                    echo No tests folder found. Skipping tests.
                ) else (
                    docker run --rm -v "%cd%:/app" -w /app python:3.11-slim ^
                      sh -c "pip install --upgrade pip && pip install -r requirements.txt pytest requests && pytest -q --maxfail=1 --disable-warnings"
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
                echo "Docker run + health check (uses external port %EXTERNAL_PORT%)..."
                bat """
                rem Remove any previous container with same name (ignore errors)
                docker rm -f %APP_NAME% 1>nul 2>&1 || echo No previous container

                rem Start container mapping EXTERNAL_PORT -> INTERNAL_PORT
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest

                rem Wait for app to be ready using PowerShell (retries)
                powershell -Command ^
                  "$retries=0; while ($retries -lt 12) { try { Invoke-WebRequest -UseBasicParsing -Uri http://localhost:%EXTERNAL_PORT% -TimeoutSec 5 | Out-Null; Write-Host 'OK'; exit 0 } catch { Write-Host 'Not ready... ' ($retries+1); Start-Sleep -Seconds 5; $retries++ } } ; Write-Host 'App not ready after retries'; exit 1"
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub (if credentials provided)..."
                // Make sure you added a Jenkins credential with ID 'docker-hub-cred'
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat """
                    echo Logging in...
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
            echo "Post: cleaning local containers (ignore errors)..."
            // Ensure the post cleanup never fails the pipeline itself
            bat """
            docker stop %APP_NAME% 1>nul 2>&1 || echo No container to stop
            docker rm %APP_NAME% 1>nul 2>&1 || echo No container to remove
            exit /b 0
            """
        }
        success {
            echo "Pipeline finished SUCCESS — image built (and pushed if credentials present)."
        }
        failure {
            echo "Pipeline FAILED — check console logs for details."
        }
    }
}
