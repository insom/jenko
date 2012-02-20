Jenko, the Jenkins/Bootstrap dashboard
======================================

Use example.config as an template, changing at least the CI server URL, and
then define each of the jobs you care about, along with a description and the
Git prefix in your jobs.conf file.

GitHub & Gitorious URLs look like:

    http://hostname/person/project/commit/hash

Then you can run the server locally with:

    JENKO_CONFIG=your.config python jenko.py
