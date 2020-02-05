pipeline {
  environment {
    registry = 'https://registry'
    dockerImage = ''
    app = ''
    imageName = 'middlewareintegration'
  }
  agent any
  stages {
    stage('Generate docker name for Production') {
      when {
        branch 'master'
      }
      steps{
        script {
          dockerImage = 'integrador_redmine/' + imageName
        }
      }
    }

    stage('Generate docker name for Development') {
      when {
        branch 'develop'
      }
      steps{
        script {
          dockerImage = 'integrador_redmine/' + imageName + "dev"
        }
      }
    }

    stage('Building docker image') {
      steps{
        script {
          app = docker.build(dockerImage)
        }
      }
    }

    stage('Deploy docker Image') {
      steps{
        script {
          docker.withRegistry(registry, '' ) {
            app.push("$BUILD_NUMBER")
            app.push()
          }
        }
      }
    }

    stage('Remove Unused docker image') {
      steps{
        sh 'docker rmi ' + dockerImage
      }
    }
  }
}