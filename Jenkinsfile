node() {
  agent any
  triggers {
    cron('H H * * *')
  }
  stage('Checkout') {
    checkout scm
  }
  stage('Run build script') {
    steps {
      sh "python ./scripts/getrelease.py --copy-build ./latest --base-dir releases --remove"
    }
  }
  stage('Commit/Push') {
     when {
       branch master
     }
     steps {
       sh "./scripts/commit.bash"
     }
  }
}
