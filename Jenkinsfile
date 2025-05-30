properties([
    disableConcurrentBuilds(),
])

commitSha = ''
commitMessage = ''
pipelineId = env.BUILD_ID
skipCI = false
dockerImage = ''
dockerRegistry = 'ghcr.io/mazhora'
appName = 'it-breakfast-tg-bot'
dockerRegistryCreds = 'mazhora-github-token'

IS_MASTER         = (env.BRANCH_NAME == 'main') ? true : false
IS_PROD           = (env.BRANCH_NAME == 'prod')   ? true : false

node {

    try {
        stage('Checkout') {
            checkout scm
            commitSha = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
            echo "Commit SHA: ${commitSha}"
            commitMessage = sh(script: "git log -1 --pretty=%B", returnStdout: true).trim()
            echo "Commit message: ${commitMessage}"
            
            if (commitMessage.contains('[skip-ci]')) {
                echo "Found [skip-ci]. Skipping pipeline"
                currentBuild.result = 'SUCCESS'
                skipCI = true
            }

        }

        if (!skipCI) {

            if (IS_PROD) {
                imageTag = "prod-${pipelineId}-${commitSha}"
            }
            if (IS_MASTER) {
                imageTag = "${pipelineId}-${commitSha}"
            }

            stage('Build and Push Docker Image') {
                echo "imageTag"
                echo "${imageTag}"
                sh "docker build -f ./Dockerfile -t ${dockerRegistry}/${appName}:${imageTag} ."
                echo "Docker Image: ${dockerRegistry}/${appName}:${imageTag}"
                echo "Pushing Docker image..."
                sh "docker push ${dockerRegistry}/${appName}:${imageTag}"
                sh "echo 'Очищаем локальные ресурсы'"
                sh "docker rmi ${dockerRegistry}/${appName}:${imageTag}"
            }

            stage('Checkout deploy repo') {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: 'refs/heads/main']],
                    extensions: [
                        [$class: 'RelativeTargetDirectory', relativeTargetDir: 'ansible'],
                        [$class: 'CloneOption', depth: 100, noTags: true, shallow: true]
                    ],
                    userRemoteConfigs: [[credentialsId: dockerRegistryCreds, url: 'https://github.com/mazhora/it-breakfast-tg-bot-infra.git']]
                ])
            }

            dir('ansible'){
                stage('deploy docker') {
                    if (IS_PROD) {
                        ansiblePlaybook(
                            credentialsId: 'jenkins-ssh-key',
                            playbook: 'deploy-prod.yml',
                            tags: 'deploy',
                            extraVars: [
                                image_version: "${imageTag}"
                            ]
                        )
                    }
                    if (IS_MASTER) {
                        ansiblePlaybook(
                            credentialsId: 'jenkins-ssh-key',
                            playbook: 'deploy-stage.yml',
                            tags: 'deploy',
                            extraVars: [
                                image_version: "${imageTag}"
                            ]
                        )
                    }
                }
            }

        }
    } catch (Exception e) {
        echo "Pipeline failed: ${e.getMessage()}"
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        if (!skipCI && currentBuild.result != 'FAILURE') {
            echo "Deploy done"
        } else {
            if (skipCI) {
                echo "deploy was skipped due to the [skip-ci] mark"
            }
        }
        echo "Pipeline result: ${currentBuild.result == 'FAILURE' ? 'FAILURE' : 'SUCCESS'}"
    }
}


