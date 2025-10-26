pipeline {
    agent any

    environment {
        APP_NAME = "roblox-webapp"
        DOCKER_IMAGE = "roblox-webapp:latest"
        CONTAINER_NAME = "roblox_app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Checking out source code from Git..."
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                bat """
                docker build -t %DOCKER_IMAGE% .
                """
            }
        }

        stage('Run Container') {
            steps {
                echo "🚀 Running Flask app container..."
                bat """
                docker rm -f %CONTAINER_NAME% >nul 2>&1 || echo No old container
                docker run -d --name %CONTAINER_NAME% -p 5000:5000 %DOCKER_IMAGE%
                """
            }
        }

        stage('Test App Startup') {
            steps {
                echo "🔍 Waiting for Flask app to start..."
                bat '''
                setlocal enabledelayedexpansion
                set /a retries=0
                :retry
                curl -f http://localhost:5000/ >nul 2>&1
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

        stage('Run Python Tests') {
            steps {
                echo "🧪 Running pytest on Flask app endpoints..."
                bat '''
                docker exec %CONTAINER_NAME% pip install pytest requests >nul
                docker exec %CONTAINER_NAME% pytest -v --maxfail=1 --disable-warnings
                '''
            }
        }
    }

    post {
        always {
            echo "🧹 Cleaning up containers..."
            bat """
            docker stop %CONTAINER_NAME% >nul 2>&1 || echo No container to stop
            docker rm %CONTAINER_NAME% >nul 2>&1 || echo No container to remove
            """
        }
        success {
            echo "✅ Build & Test completed successfully!"
        }
        failure {
            echo "❌ Build or Test failed!"
        }
    }
}
