node() {
  stage('Checkout') {
    checkoutInfo = checkout scm
  }
  stage('Run build script') {
    sh "./scripts/fake_build.sh"
  }
  stage('Commit/Push') {
    sh "echo foo"
  }
}
