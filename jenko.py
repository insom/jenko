#!/usr/bin/env python
from __future__ import with_statement
import urllib
import json
import sys
import os
import time
from os.path import join, dirname, exists
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
import socket
from jenkinsapi.jenkins import Jenkins

socket.setdefaulttimeout(15)

PROJ_ROOT = dirname(__file__)

DEBUG = True

JOBS_CONF = './jobs.conf'
JENKINS_URL = "http://ci.server/jenkins"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('JENKO_CONFIG', silent=True)

@app.route('/api/jenkins')
def jenkins():
    notes = []
    return jsonify(notes=notes)

class Job(object):
    def __init__(self, name, description=None, git_prefix=None):
        self.name = name
        self.description = description or name
        self.git_prefix = git_prefix

    def url(self, hash):
        if self.git_prefix:
            return self.git_prefix + hash
        else:
            return False


def status_and_changeset(job, jenkins):
    lb = jenkins.get_job(job.name).get_last_build()
    # comment, id
    items = lb._data.get('changeSet', {}).get('items', [])
    res = [(item.get('comment'), item.get('id')) for item in items]
    return job, lb.get_status(), res

@app.route('/')
def index():
    jenkins = Jenkins(app.config['JENKINS_URL'])
    jobs = eval(file(app.config['JOBS_CONF']).read(), globals(), locals())
    results = [status_and_changeset(x, jenkins) for x in jobs]
    return render_template(
        'index.html',
        results=results,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
