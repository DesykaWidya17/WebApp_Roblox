pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
        APP_NAME = 'roblox_app'
        IMAGE_NAME = 'roblox-webapp'
        INTERNAL_PORT = '5000'
        EXTERNAL_PORT = '5050'
        DOCKER_HUB_USER = 'desykawidya'

        // Tambahkan path Python agar dikenali Jenkins service
        PATH = "C:\\Users\\DESYKA\\AppData\\Local\\Programs\\Python\\Python312;C:\\Users\\DESYKA\\AppData\\Local\\Programs\\Python\\Python312\\Scripts;${env.PATH}"
    }

    stages {
        /* === 1. CHECKOUT === */
        stage('Checkout') {
            steps {
                echo "📥 Checking out source code..."
                deleteDir()
                git branch: 'main', url: "${REPO_URL}"
                echo "✅ Source code checkout complete!"
            }
        }

        /* === 2. BUILD & TEST (GO) — tapi Python === */
        stage('Build & Test (Go)') {
            steps {
                echo "🧱 Building and testing Python web app..."
                bat '''
                echo Checking Python version...
                "C:\\Users\\DESYKA\\AppData\\Local\\Programs\\Python\\Python312\\python.exe" --version || exit /b 1

                echo Installing dependencies...
                if exist requirements.txt (
                    pip install -r requirements.txt
                ) else (
                    echo ⚠️ No requirements.txt found. Skipping install.
                )

                echo Running tests...
                if exist tests (
                    pip install pytest requests
                    pytest -v --maxfail=1 --disable-warnings || exit /b 1
                ) else (
                    echo ⚠️ No test folder found. Skipping tests.
                )

                echo ✅ Python build & test complete!
                '''
            }
        }

        /* === 3. DOCKER BUILD & TEST === */
        stage('Docker Build & Test') {
            steps {
                echo "🐳 Building Docker image and running container..."
                bat '''
                docker build -t %IMAGE_NAME%:latest . || exit /b 1
                docker rm -f %APP_NAME% 1>nul 2>&1
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest

                echo 🔍 Checking app health on port %EXTERNAL_PORT%...
                setlocal enabledelayedexpansion
                set /a retries=0
                :retry
                curl -f http://localhost:%EXTERNAL_PORT% >nul 2>&1
                if !errorlevel! neq 0 (
                    if !retries! lss 8 (
                        set /a retries+=1
                        echo App not ready... retry !retries!/8
                        timeout /t 5 /nobreak >nul
                        goto retry
                    ) else (
                        echo ❌ App failed to start after 8 retries.
                        docker logs %APP_NAME%
                        exit /b 1
                    )
                )
                echo ✅ Container is healthy!
                endlocal
                '''
            }
        }

        /* === 4. PUSH TO DOCKER HUB === */
        stage('Push to Docker Hub') {
            steps {
                echo "☁️ Pushing image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'docker-hub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS% || exit /b 1
                    docker tag %IMAGE_NAME%:latest %DOCKER_USER%/%IMAGE_NAME%:latest
                    docker push %DOCKER_USER%/%IMAGE_NAME%:latest || exit /b 1
                    docker logout
                    echo ✅ Image successfully pushed to Docker Hub!
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning up environment..."
            bat '''
            docker stop %APP_NAME% 1>nul 2>&1
            docker rm %APP_NAME% 1>nul 2>&1
            docker system prune -f
            echo 🧽 Cleanup complete.
            '''
        }
        success {
            echo "🎉 PIPELINE SUCCESS — All stages completed perfectly!"
        }
        failure {
            echo "💥 PIPELINE FAILED — Check the logs above for details."
        }
    }
}
