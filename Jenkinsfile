// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
node('docker') {
    env.CPU = "cheri256"
    def app
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

//    def dockerBuildTasks = [:]
//    // TODO: parallel build of cheri256/cheri128/mips
//    for(String cpu : ["cheri256"]) {
//        dockerBuildTasks["${cpu}"] = { }
//    }
//    parallel dockerBuildTasks


    stage ("Build images") {
        node("docker") {
            echo "CPU=${cpu}"
            sh "env | sort"
            /* This builds the actual image; synonymous to
             * docker build on the command line */
            app = docker.build("ctsrd/cheri-sdk-${cpu}")
        }
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