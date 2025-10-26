pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "roblox-webapp"
        CONTAINER_NAME = "roblox-webapp-container"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Cloning repository..."
                checkout scm
            }
        }

        stage('Build Docker image') {
            steps {
                echo "🐳 Building Docker image..."
                bat '''
                docker build -t %DOCKER_IMAGE% .
                '''
            }
        }

        stage('Run Container') {
            steps {
                echo "🚀 Starting container..."
                bat '''
                docker rm -f %CONTAINER_NAME% || echo No container to remove
                docker run -d -p 5000:5000 --name %CONTAINER_NAME% %DOCKER_IMAGE%
                '''
            }
        }

        stage('Test') {
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
                echo App did not start correctly after 6 retries!
                exit /b 1
            )
        )
        echo ✅ Flask app is reachable!
        endlocal
        '''
    }
}

        stage('Cleanup') {
            steps {
                echo "🧹 Cleaning up container..."
                bat '''
                docker rm -f %CONTAINER_NAME% || echo No container to remove
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build and test succeeded!"
        }
        failure {
            echo "❌ Build failed. Check logs for details."
        }
    }
}
