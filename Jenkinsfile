pipeline {
    agent any

    environment {
        // Tambahkan path Node.js supaya Jenkins bisa detect node & npm
        PATH = "C:\\Program Files\\nodejs\\;${env.PATH}"
        IMAGE_NAME = "roblox-webapp"
        CONTAINER_NAME = "roblox-webapp-container"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📦 Checking out source code..."
                checkout scm
            }
        }

        stage('Check Node & NPM') {
            steps {
                echo "🔍 Checking Node.js and NPM versions..."
                bat 'node -v'
                bat 'npm -v'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "📥 Installing dependencies..."
                bat 'npm install'
            }
        }

        stage('Run Tests') {
            steps {
                echo "🧪 Running tests..."
                bat 'npm test'
            }
        }

        stage('Build Application') {
            steps {
                echo "🏗️ Building application..."
                bat 'npm run build'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image..."
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "🚀 Deploying with Docker Compose..."
                bat 'docker-compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                echo "💓 Performing health check..."
                bat 'curl http://localhost:3000'
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed! Check logs for details."
        }
    }
}
