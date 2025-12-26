pipeline {
  agent any

  environment {
    IMAGE_NAME = "kafka-python-client"
    NETWORK = "kafka-net"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build -t $IMAGE_NAME ./python-client
        '''
      }
    }

    stage('Deploy Producer') {
      steps {
        sh '''
          docker stop kafka-producer || true
          docker rm kafka-producer || true

          docker run -d \
            --name kafka-producer \
            --network $NETWORK \
            $IMAGE_NAME \
            python producer.py
        '''
      }
    }

    stage('Deploy Consumer UI') {
      steps {
        sh '''
          docker stop kafka-consumer || true
          docker rm kafka-consumer || true

          docker run -d \
            --name kafka-consumer \
            --network $NETWORK \
            -p 8501:8501 \
            $IMAGE_NAME
        '''
      }
    }
  }

  post {
    success {
      echo "CI/CD completed successfully"
    }
    failure {
      echo "CI/CD failed"
    }
  }
}
