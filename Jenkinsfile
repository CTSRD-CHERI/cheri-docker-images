// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
properties([[$class: 'CopyArtifactPermissionProperty', projectNames: '*']])
def targets = ["cheri256", "cheri128", "mips"]

node("docker") {
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
        sh "pwd"
    }
    for (String cpu : targets) {
        stage("Copy artifacts for ${cpu}") {
            def ISA = "vanilla"
            def SdkProject = "CHERI-SDK/ALLOC=jemalloc,CPU=${cpu},ISA=${ISA},label=linux/"
            def SdkArtifactFilter = "${cpu}-${ISA}-jemalloc-sdk.tar.xz"
            echo "Copying SDK project=${SdkProject}, filter=${SdkArtifactFilter}"
            step([$class     : 'CopyArtifact',
                  projectName: SdkProject,
                  filter     : SdkArtifactFilter])
            def qemuCPU
            if (cpu == "cheri256" || cpu == "mips") {
                qemuCPU = "cheri"
            } else if (cpu == "cheri128") {
                qemuCPU == "cheri128"
            }
            step([$class     : 'CopyArtifact',
                  projectName: "QEMU-CHERI-multi/CPU=${qemuCPU},label=linux/",
                  filter     : "qemu-cheri-install/**",
                  target     : "QEMU-${cpu}"])
        }
    }
    for (String cpu : targets) {
        def app
        stage("Build ${cpu} image") {
            sh "pwd"
            echo "CPU=${cpu}"
            env.CPU = "${cpu}"

            // sh "env | sort"
            /* This builds the actual image; synonymous to docker build on the command line */
            app = docker.build("ctsrd/cheri-sdk-${cpu}", "--build-arg target=${cpu} .")
        }

        stage("Test ${cpu} image") {
            /* Ideally, we would run a test framework against our image.
                 * For this example, we're using a Volkswagen-type approach ;-) */
            app.inside {
                sh 'echo "Tests passed"'
                sh "env | sort"
            }
        }

        stage("Push ${cpu} image") {
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