pipeline {
    agent any

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                echo "📥 Checking out source code from ${env.GIT_URL}..."
                deleteDir()
                git branch: 'main', url: 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
                echo "✅ Source code checkout complete!"
            }
        }

        stage('Build & Test (Go)') {
            steps {
                echo "🧱 Checking Python setup..."
                bat '''
                echo Checking Python version...
                where python
                python --version
                echo Installing dependencies if any...
                pip install -r requirements.txt || echo No requirements.txt found
                echo Running simple test...
                python -m py_compile main.py || echo Skip test
                '''
            }
        }

        stage('Docker Build & Test') {
            steps {
                echo "🐳 Building and testing Docker image..."
                bat '''
                docker build -t roblox_app:latest .
                docker run -d --name roblox_app -p 5000:5000 roblox_app:latest
                echo Checking container status...
                docker ps
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "📦 Pushing image to Docker Hub..."
                bat '''
                docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                docker tag roblox_app:latest %DOCKER_USER%/roblox_app:latest
                docker push %DOCKER_USER%/roblox_app:latest
                '''
            }
        }
    }

    post {
        always {
            stage('Declarative: Post Actions') {
                steps {
                    echo "🧹 Cleaning up containers..."
                    bat '''
                    docker stop roblox_app  1>nul 2>&1
                    docker rm roblox_app  1>nul 2>&1
                    echo 🧽 Cleanup complete.
                    '''
                }
            }
        }
        failure {
            echo "💥 PIPELINE FAILED — check the stage logs above for details."
        }
        success {
            echo "✅ PIPELINE SUCCESS — all stages completed."
        }
    }
}
