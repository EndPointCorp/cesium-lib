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
    if (env.BRANCH_NAME == 'master') {
      sh './scripts/commit.bash'
    }
    else {
      sh "echo Don't commit/push for non-master branch"
    }
  }
}
