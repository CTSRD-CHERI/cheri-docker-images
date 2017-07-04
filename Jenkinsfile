// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
properties([[$class: 'CopyArtifactPermissionProperty', projectNames: '*']])
def targets = ["cheri256"]

def dockerBuildTasks = [:]

for (String cpu : targets) {
    dockerBuildTasks["${cpu}"] = {
        node('docker') {
            def app
            sh "pwd"

            stage("Copy artifacts for ${cpu}") {
                def ISA = "vanilla"
                def SdkProject = "CHERI-SDK/ALLOC=jemalloc,CPU=${cpu},ISA=${ISA},label=linux/"
                def SdkArtifactFilter = "${cpu}-${ISA}-jemalloc-sdk.tar.xz"
                echo "Copying SDK project=${SdkProject}, filter=${SdkArtifactFilter}"
                step([$class     : 'CopyArtifact',
                      projectName: SdkProject,
                      filter     : SdkArtifactFilter])
                if (cpu == "cheri256") {
                    step([$class     : 'CopyArtifact',
                          projectName: "QEMU-CHERI-multi/CPU=cheri,label=linux/",
                          filter     : "qemu-cheri-install/**"])
                } else if (cpu == "cheri128") {
                    step([$class     : 'CopyArtifact',
                          projectName: "QEMU-CHERI-multi/CPU=cheri,label=linux/",
                          filter     : "qemu-cheri-install/**"])
                }
            }

            stage("Build image") {
                sh "pwd"
                echo "CPU=${cpu}"
                env.CPU = "${cpu}"
                sh "env | sort"
                /* This builds the actual image; synonymous to docker build on the command line */
                app = docker.build("ctsrd/cheri-sdk-${cpu}", "--build-arg target=${cpu} .")
            }

            stage('Test image') {
                /* Ideally, we would run a test framework against our image.
                     * For this example, we're using a Volkswagen-type approach ;-) */
                app.inside {
                    sh 'echo "Tests passed"'
                    sh "env | sort"
                }
            }

            stage('Push image') {
                /* Finally, we'll push the image with two tags:
                     * First, the incremental build number from Jenkins
                     * Second, the 'latest' tag.
                     * Pushing multiple tags is cheap, as all the layers are reused. */
                docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
    }
}
node {
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
        sh "pwd"
    }
    stage("Build images") {
        sh "pwd"
        parallel dockerBuildTasks
    }
}