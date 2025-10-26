pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
        APP_NAME = 'roblox_app'
        IMAGE_NAME = 'roblox-webapp'
        INTERNAL_PORT = '5000'
        EXTERNAL_PORT = '5050'
        DOCKER_HUB_USER = 'desykawidya'  // Ganti dengan username Docker Hub kamu
    }

    stages {

        /* === 1. CHECKOUT SOURCE CODE === */
        stage('Checkout SCM') {
            steps {
                echo "📥 Checking out source code from ${REPO_URL}..."
                git branch: 'main', url: "${REPO_URL}"
            }
        }

        /* === 2. BUILD APP SOURCE CODE === */
        stage('Build & Setup Environment') {
            steps {
                echo "🧱 Setting up Python environment..."
                bat '''
                python --version
                pip install --upgrade pip
                pip install -r requirements.txt
                echo Python dependencies installed successfully.
                '''
            }
        }

        /* === 3. UNIT TEST === */
        stage('Run Unit Tests') {
            steps {
                echo "🧪 Running unit tests..."
                bat '''
                if not exist tests (
                    echo No tests folder found. Skipping pytest.
                ) else (
                    pip install pytest requests
                    pytest -v --maxfail=1 --disable-warnings || exit /b 1
                )
                '''
            }
        }

        /* === 4. DOCKER BUILD === */
        stage('Docker Build') {
            steps {
                echo "🐳 Building Docker image: ${IMAGE_NAME}:latest"
                bat '''
                docker build -t %IMAGE_NAME%:latest .
                '''
            }
        }

        /* === 5. RUN & TEST CONTAINER === */
        stage('Docker Test Run') {
            steps {
                echo "🚀 Running container and performing health check..."
                bat '''
                docker rm -f %APP_NAME% 1>nul 2>&1
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest
                echo Waiting for Flask app to start...

                powershell -Command ^
                "$retries = 0; ^
                while ($retries -lt 6) { ^
                    try { ^
                        Invoke-WebRequest -Uri http://localhost:%EXTERNAL_PORT% -UseBasicParsing | Out-Null; ^
                        Write-Host 'Flask app is reachable!'; ^
                        exit 0; ^
                    } catch { ^
                        Write-Host 'Flask not ready yet... retry' ($retries+1) '/6'; ^
                        Start-Sleep -Seconds 5; ^
                        $retries++; ^
                    } ^
                } ^
                Write-Host 'App did not start correctly after retries!'; exit 1;"
                '''
            }
        }

        /* === 6. PUSH TO DOCKER HUB === */
        stage('Push to Docker Hub') {
            steps {
                echo "☁️ Pushing image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    echo Logging in to Docker Hub...
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker tag %IMAGE_NAME%:latest %DOCKER_USER%/%IMAGE_NAME%:latest
                    docker push %DOCKER_USER%/%IMAGE_NAME%:latest
                    docker logout
                    '''
                }
            }
        }
    }

    /* === 7. POST ACTIONS === */
    post {
        always {
            echo "🧹 Cleaning up containers..."
            bat '''
            docker stop %APP_NAME% 1>nul 2>&1
            docker rm %APP_NAME% 1>nul 2>&1
            '''
        }
        success {
            echo "✅ Pipeline completed successfully and pushed to Docker Hub."
        }
        failure {
            echo "❌ Pipeline failed! Check Jenkins logs for details."
        }
    }
}
