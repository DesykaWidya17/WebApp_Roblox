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
                checkout scm
            }
        }

        /* === 2. BUILD APP SOURCE CODE === */
        stage('Build & Setup Environment') {
            steps {
                echo "🧱 Setting up Python environment and dependencies..."
                bat '''
                python --version
                pip install -r requirements.txt
                echo ✅ Python dependencies installed successfully!
                '''
            }
        }

        /* === 3. UNIT TEST === */
        stage('Test App') {
            steps {
                echo "🧪 Running unit tests for Flask app..."
                bat '''
                timeout /t 5 /nobreak >nul
                if not exist tests echo ⚠️ No tests folder found. Skipping pytest.
                if exist tests (
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

        /* === 5. DOCKER TEST (RUN CONTAINER + HEALTH CHECK) === */
        stage('Docker Test Run') {
            steps {
                echo "🚀 Running Flask container for health check..."
                bat '''
                docker rm -f %APP_NAME% 1>nul 2>&1
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest

                echo 🔍 Waiting for Flask app to start...
                setlocal enabledelayedexpansion
                set /a retries=0
                :retry
                curl -f http://localhost:%EXTERNAL_PORT% >nul 2>&1
                if !errorlevel! neq 0 (
                    if !retries! lss 6 (
                        set /a retries+=1
                        echo Flask not ready yet... retry !retries!/6
                        timeout /t 5 /nobreak >nul
                        goto retry
                    ) else (
                        echo ❌ App did not start correctly after 6 retries!
                        exit /b 1
                    )
                )
                echo ✅ Flask app is reachable!
                endlocal
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
            echo "🧹 Cleaning up local Docker containers..."
            bat '''
            docker stop %APP_NAME% 1>nul 2>&1
            docker rm %APP_NAME% 1>nul 2>&1
            '''
        }
        success {
            echo "✅ Pipeline completed successfully! Image pushed to Docker Hub."
        }
        failure {
            echo "❌ Pipeline failed! Please check logs for errors."
        }
    }
}
