// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
properties([[$class: 'CopyArtifactPermissionProperty', projectNames: '*']])
def targets = ["cheri256", "cheri128", "mips"]

node("docker") {
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
        sh "pwd"
    }
    // fetch cmake
    stage("Download CMake") {
        def cmakeArchive = 'cmake-3.9.0-rc5-Linux-x86_64.tar.gz'
        sh "test -e ${cmakeArchive} || curl -O https://cmake.org/files/v3.9/${cmakeArchive}"
    }
    stage("Copy binutils") {
        step([$class     : 'CopyArtifact',
              projectName: "CHERI-binutils/label=linux/",
              filter     : "binutils.tar.bz2"])
    }

    for (String cpu : targets) {
        stage("Copy artifacts for ${cpu}") {
            sh "mkdir -p ${cpu}-build"
            echo "Copying CheriBSD sysroot"
            step([$class     : 'CopyArtifact',
                  projectName: "CHERIBSD-WORLD/ALLOC=jemalloc,CPU=${cpu},ISA=vanilla/",
                  filter     : "$cpu-vanilla-jemalloc-cheribsd-world.tar.xz",
                  target     : "${cpu}-build"])
            // def SdkProject = "CHERI-SDK/ALLOC=jemalloc,CPU=${cpu},ISA=${ISA},label=linux/"
            if (cpu == "cheri128" || cpu == "cheri256") {
                echo "Copying clang artifacts"
                step([$class     : 'CopyArtifact',
                      projectName: "CLANG-LLVM-master/CPU=${cpu},label=linux/",
                      filter     : "*.tar.xz",
                      target     : "${cpu}-build"])
                def qemuCPU = cpu == "cheri128" ? "cheri128" : "cheri"
                echo "Copying QEMU artifacts"
                step([$class     : 'CopyArtifact',
                      projectName: "QEMU-CHERI-multi/CPU=${qemuCPU},label=linux/",
                      filter     : "qemu-cheri-install/**",
                      target     : "${cpu}-build"])
            } else {
                dir("${cpu}-build") {
                    sh "ln -sf ../cheri256-build/cheri256-master-clang-llvm.tar.xz ${cpu}-master-clang-llvm.tar.xz"
                    sh "ln -sf ../cheri256-build/qemu-cheri-install ."
                }
            }
        }
    }
    sh "ls -la"
    sh "ls -la *-build"
    for (String cpu : targets) {
        def app
        stage("Build ${cpu} image") {
            dir("${cpu}-build") {
                sh "ln -sf ../Dockerfile ."
                sh "ln -sf ../binutils.tar.gz ."

                sh "pwd; ls -la"
                sh "cat Dockerfile"
                echo "CPU=${cpu}"
                env.CPU = "${cpu}"

                // sh "env | sort"
                /* This builds the actual image; synonymous to docker build on the command line */
                app = docker.build("ctsrd/cheri-sdk-${cpu}", "-q --build-arg target=${cpu} .")
            }
        }

        stage("Test ${cpu} image") {
            /* Ideally, we would run a test framework against our image.
             * For this example, we're using a Volkswagen-type approach ;-) */
            app.inside {
                sh 'echo "Tests passed"'
                sh "env | sort"
            }
        }
        if (false) {
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

    stage ("Cleaning up") {
        for (String cpu : targets) {
            dir("${cpu}-build") {
                deleteDir()
            }
        }
    }
}