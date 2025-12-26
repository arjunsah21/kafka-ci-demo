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
            $IMAGE_NAME
        '''
      }
    }

    stage('Deploy Consumer') {
      steps {
        sh '''
          docker stop kafka-consumer || true
          docker rm kafka-consumer || true

          docker run -d \
            --name kafka-consumer \
            --network $NETWORK \
            $IMAGE_NAME \
            python consumer.py
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
