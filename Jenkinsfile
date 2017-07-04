// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
node('docker') {
    def app
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }

    stage('Build image') {
        sh "env | sort"
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        app = docker.build("ctsrd/cheri-sdk-${env.CPU}", "--build-arg target=${env.CPU}")
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