pipeline {
    agent any

    environment {
        IMAGE_NAME = "roblox-webapp"
        CONTAINER_NAME = "roblox-webapp-container"
        // Docker Hub credentials
        DOCKER_USER = credentials('DOCKER_USER')
        DOCKER_PASS = credentials('DOCKER_PASS')
    }

    stages {
        stage('Checkout') {
            steps {
                echo "📥 Checking out source code..."
                deleteDir()
                // Jika repo private, masukkan credentialsId
                git branch: 'main', url: 'https://github.com/DesykaWidya17/WebApp_Roblox.git'
                echo "✅ Source code checkout complete!"
            }
        }

        stage('Build & Test (Python)') {
            steps {
<<<<<<< HEAD
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
=======
                echo "🧱 Checking Python setup..."
                bat '''
                echo Checking Python version...
                where python
                python --version

                echo Installing dependencies...
                if exist requirements.txt (
                    pip install -r requirements.txt
                ) else (
                    echo No requirements.txt found, skipping...
                )

                echo Running Python syntax check...
                if exist main.py (
                    python -m py_compile main.py
                ) else (
                    echo main.py not found, skipping test...
                )
>>>>>>> dfb18520c74b69827699c5fa3d5e5de2a8910de4
                '''
            }
        }

        stage('Docker Build & Test') {
            steps {
<<<<<<< HEAD
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
=======
                echo "🐳 Building and testing Docker image..."
                bat '''
                REM Remove existing container if exists
                docker rm -f roblox_app 1>nul 2>&1

                REM Build Docker image
                docker build -t roblox_app:latest .

                REM Run Docker container
                docker run -d --name roblox_app -p 5000:5000 roblox_app:latest

                docker ps
>>>>>>> dfb18520c74b69827699c5fa3d5e5de2a8910de4
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
<<<<<<< HEAD
                echo "🧹 Cleaning up old containers and images..."
                bat '''
                    docker rm -f %CONTAINER_NAME% || echo No container to remove
                    docker image prune -f
                '''
=======
                echo "📦 Pushing image to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'DOCKER_USER', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat '''
                    docker login -u %DOCKER_USER% -p %DOCKER_PASS%
                    docker tag roblox_app:latest %DOCKER_USER%/roblox_app:latest
                    docker push %DOCKER_USER%/roblox_app:latest
                    '''
                }
>>>>>>> dfb18520c74b69827699c5fa3d5e5de2a8910de4
            }
        }
    }

    post {
<<<<<<< HEAD
        success {
            node { echo "✅ Build and deployment successful!" }
=======
        always {
            echo "🧹 Cleaning up containers..."
            bat '''
            docker stop roblox_app 1>nul 2>&1
            docker rm roblox_app 1>nul 2>&1
            echo 🧽 Cleanup complete.
            '''
>>>>>>> dfb18520c74b69827699c5fa3d5e5de2a8910de4
        }

        success {
            echo "✅ PIPELINE SUCCESS — all stages completed."
        }

        failure {
<<<<<<< HEAD
            node { echo "❌ Build failed. Check logs for details." }
=======
            echo "💥 PIPELINE FAILED — check the stage logs above for details."
>>>>>>> dfb18520c74b69827699c5fa3d5e5de2a8910de4
        }
    }
}
