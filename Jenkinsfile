node() {
  stage('Checkout') {
    checkoutInfo = checkout scm
  }
  stage('Run build script') {
    sh "python ./scripts/getrelease.py --copy-build ./latest --base-dir releases --remove"
  }
  stage('Commit/Push') {
    sh "./scripts/commit.bash"
  }
}
