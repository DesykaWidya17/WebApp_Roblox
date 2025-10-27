pipeline {
    agent any

    environment {
        IMAGE_NAME = "roblox-webapp"
        CONTAINER_NAME = "roblox-webapp-container"
        // optional jika push ke Docker Hub
        // DOCKER_USER = credentials('DOCKER_USER')
        // DOCKER_PASS = credentials('DOCKER_PASS')
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
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Container') {
            steps {
                echo "🚀 Starting container..."
                bat '''
                    docker rm -f %CONTAINER_NAME% || echo No container to remove
                    docker run -d -p 5000:5000 --name %CONTAINER_NAME% %IMAGE_NAME%
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🔍 Testing Flask app availability..."
                bat '''
                    echo === Docker Containers ===
                    docker ps

                    echo === Container Logs ===
                    docker logs %CONTAINER_NAME%

                    echo === Waiting for app to start ===
                    powershell -Command "Start-Sleep -Seconds 5"

                    echo === Testing connection ===
                    curl -v http://localhost:5000/ || (echo App did not start correctly! && exit /b 1)
                '''
            }
        }

        stage('Cleanup') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                echo "🧹 Cleaning up old containers and images..."
                bat '''
                    docker rm -f %CONTAINER_NAME% || echo No container to remove
                    docker image prune -f
                '''
            }
        }
    }

    post {
        success {
            node { echo "✅ Build and deployment successful!" }
        }
        failure {
            node { echo "❌ Build failed. Check logs for details." }
        }
    }
}
