node() {
  properties(
    [
       pipelineTriggers([
         cron( env.BRANCH_NAME.equals('master') ? 'H H * * *' : '')
       ])
    ]
  )
  stage('Checkout') {
    checkout scm
  }
  stage('Run build script') {
    sh "python ./scripts/getrelease.py --copy-build ./latest --base-dir releases --remove"
  }
  stage('Commit/Push') {
    when {
      branch master
    }
    sh "./scripts/commit.bash"
  }
}
