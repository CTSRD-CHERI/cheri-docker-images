// https://getintodevops.com/blog/building-your-first-docker-image-with-jenkins-2-guide-for-developers
properties([[$class: 'CopyArtifactPermissionProperty', projectNames: '*']])
def targets = ["cheri256", "cheri128", "mips"]
cmakeArchive = 'cmake-3.9.4-Linux-x86_64.tar.gz'

def buildSDKImage(String cpu) {
    def app
    stage("Build ${cpu} image") {
        // sh "env | sort"
        sh "pwd && ls -la"
        dir ("sdk-${cpu}-build") {
            sh "cp -f ../cheri-sdk/Dockerfile ../binutils.tar.bz2 ../elftoolchain.tar.xz ../${cmakeArchive} ."
            sh "pwd && ls -la"
            /* This builds the actual image; synonymous to docker build on the command line */
            app = docker.build("ctsrd/cheri-sdk-${cpu}", "-q --build-arg target=${cpu} .")
        }
    }

    stage("Test ${cpu} image") {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */
        app.inside {
            sh "env | sort"
            // check that QEMU works
            sh "qemu-system-cheri --help > /dev/null"
            sh "cheri-unknown-freebsd-clang --version"
            sh "ls -l /cheri-sdk/bin"

        }
    }
    // TODO: make the pushing configurable
    if (true) {
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
timeout(120) {
node("docker") {
    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
        sh "pwd"
    }
    stage("Copy artifacts") {
        // fetch cmake
        sh "test -e $cmakeArchive || curl -O https://cmake.org/files/v3.9/$cmakeArchive"
        step([$class     : 'CopyArtifact',
              projectName: "CHERI-binutils/label=linux/",
              filter     : "binutils.tar.bz2"])
        step([$class     : 'CopyArtifact',
              projectName: "elftoolchain/label=linux/",
              filter     : "elftoolchain.tar.xz"])
        for (String cpu : targets) {
            dir ("sdk-${cpu}-build") {
                echo "Copying CheriBSD ${cpu} sysroot"
                // copyArtifacts filter: 'cheri-multi-master-clang-llvm.tar.xz', projectName: 'CLANG-LLVM-master', selector: lastSuccessful()
                step([$class     : 'CopyArtifact',
                      projectName: "CHERIBSD-WORLD/ALLOC=jemalloc,CPU=${cpu},ISA=vanilla/",
                      filter     : "$cpu-vanilla-jemalloc-cheribsd-world.tar.xz"])
                // def SdkProject = "CHERI-SDK/ALLOC=jemalloc,CPU=${cpu},ISA=${ISA},label=linux/"
                if (cpu == "cheri128" || cpu == "cheri256") {
                    echo "Copying clang ${cpu} artifacts"
                    step([$class     : 'CopyArtifact',
                          projectName: "CLANG-LLVM-master/CPU=${cpu},label=linux/",
                          filter     : "*.tar.xz"])
                    def qemuCPU = cpu == "cheri128" ? "cheri128" : "cheri"
                    echo "Copying QEMU ${cpu} artifacts"
                    step([$class     : 'CopyArtifact',
                          projectName: "QEMU-CHERI-multi/CPU=${qemuCPU},label=linux/",
                          filter     : "qemu-cheri-install/**",
                          target     : "QEMU-$cpu"])
                    sh "chmod -v +x QEMU-$cpu/qemu-cheri-install/bin/*"
                } else {
                    sh "cp -f ../sdk-cheri256-build/cheri256-master-clang-llvm.tar.xz ${cpu}-master-clang-llvm.tar.xz"
                    sh "cp -Rf ../sdk-cheri256-build/QEMU-cheri256 QEMU-$cpu"
                }
                sh "pwd && ls -la"
            }
        }
        sh "ls -la"
    }
    // don't user for loops and closures: http://blog.freeside.co/2013/03/29/groovy-gotcha-for-loops-and-closure-scope/
    stage('Build SDK docker images') {
        parallel targets.collectEntries{
            [(it): { buildSDKImage(it) }]
        }
    }

    stage ("Cleaning up") {
        sh "ls -la"
        sh "rm -rf binutils.tar.bz *-build"
    }
}
}
