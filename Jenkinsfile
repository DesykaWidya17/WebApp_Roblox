pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
        APP_NAME = 'roblox_app'
        IMAGE_NAME = 'roblox-webapp'
        INTERNAL_PORT = '5000'
        EXTERNAL_PORT = '5050'
        DOCKER_HUB_USER = 'desykawidya'
    }

    stages {
        /* === 1. CHECKOUT SOURCE CODE === */
        stage('Checkout SCM') {
            steps {
                echo "📥 Checking out source code from ${REPO_URL}..."
                deleteDir()
                git branch: 'main', url: "${REPO_URL}"
                echo "✅ Source code checkout complete!"
            }
        }

        /* === 2. BUILD PYTHON ENVIRONMENT === */
        stage('Build & Setup Environment') {
            steps {
                echo "🧱 Setting up Python environment and dependencies..."
                bat '''
                echo Checking Python version...
                python --version || exit /b 1
                echo Installing dependencies...
                if exist requirements.txt (
                    pip install -r requirements.txt
                ) else (
                    echo ⚠️ No requirements.txt found, skipping install.
                )
                echo ✅ Environment ready!
                '''
            }
        }

        /* === 3. UNIT TESTS (Optional) === */
        stage('Run Unit Tests') {
            steps {
                echo "🧪 Running Flask unit tests..."
                bat '''
                if exist tests (
                    pip install pytest requests
                    pytest -v --maxfail=1 --disable-warnings || exit /b 1
                ) else (
                    echo ⚠️ No tests folder found. Skipping tests.
                )
                '''
            }
        }

        /* === 4. DOCKER BUILD === */
        stage('Docker Build') {
            steps {
                echo "🐳 Building Docker image..."
                bat '''
                docker build -t %IMAGE_NAME%:latest . || exit /b 1
                docker images %IMAGE_NAME%
                echo ✅ Docker image build complete!
                '''
            }
        }

        /* === 5. DOCKER TEST RUN === */
        stage('Docker Test Run') {
            steps {
                echo "🚀 Running container for health check..."
                bat '''
                docker rm -f %APP_NAME% 1>nul 2>&1
                docker run -d --name %APP_NAME% -p %EXTERNAL_PORT%:%INTERNAL_PORT% %IMAGE_NAME%:latest
                echo 🔍 Waiting for app to respond on port %EXTERNAL_PORT%...

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
                echo ✅ App responded successfully!
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
            echo "🧹 Cleaning up containers..."
            bat '''
            docker stop %APP_NAME% 1>nul 2>&1
            docker rm %APP_NAME% 1>nul 2>&1
            echo 🧽 Cleanup complete.
            '''
        }
        success {
            echo "🎉 ALL STAGES SUCCESSFUL — your pipeline ran perfectly!"
        }
        failure {
            echo "💥 PIPELINE FAILED — check the stage logs above for details."
        }
    }
}
