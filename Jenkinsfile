node() {
  stage('Checkout') {
    checkoutInfo = checkout scm
  }
  stage('Run build script') {
    sh "python ./scripts/getrelease.py --copy ./Build"
  }
  stage('Commit/Push') {
    sh "echo foo"
  }
}
