node('docker&&linux') {
    def app

    stage('Checkout and Sync Repo') {
        /* Let's make sure we have the repository cloned to our workspace */

        cleanWs()
        checkout scm
        git branch: 'mjindal', credentialsId: 'f461068a-544a-4e84-8446-4666adca56dc', url: 'https://github.com/manishjindal/Kubernetes-for-starters'
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("manishjindal/myflaskapp-forminikube")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */

        app.inside {
            sh 'echo "Tests passed"'
        }
    }
}