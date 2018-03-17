node('master') {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://inhvm-binrepo-01.india.mentorg.com:18018/iesd', 'bf062e7b-bb0b-4737-9d10-27b715690d60') {
            Image.push("1.0")
        }
    }
}