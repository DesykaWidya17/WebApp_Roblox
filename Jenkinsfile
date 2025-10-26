pipeline {
    agent any

    environment {
        IMAGE_NAME = "roblox-webapp"
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
                echo "🔍 Testing if Flask app is reachable..."
                bat '''
                    timeout /t 5 >nul
                    curl -f http://localhost:5000/ || (echo App did not start correctly! && exit /b 1)
                '''
            }
        }

        stage('Cleanup') {
            when {
                expression { return env.BRANCH_NAME == 'main' }
            }
            steps {
                echo "🧹 Cleaning up old images..."
                bat 'docker image prune -f'
            }
        }
    }

    post {
        success {
            echo "✅ Build and deployment successful!"
        }
        failure {
            echo "❌ Build failed. Check logs for details."
        }
    }
}
