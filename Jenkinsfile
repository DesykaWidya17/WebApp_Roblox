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
                echo "🔍 Testing if Flask app is reachable..."
                bat '''
                REM Tunggu Flask siap dulu
                timeout /t 10 /nobreak >nul

                echo Testing connection to Flask app...
                curl -f http://localhost:5000/ || (echo App did not start correctly! && exit /b 1)
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
