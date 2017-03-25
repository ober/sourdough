#!/usr/bin/env python
#
# Sourdough
#
# Copyright 2015 Joe Block <jpb@unixorn.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
setup.py for sourdough
"""

import os
import shutil
import subprocess
from setuptools import setup, find_packages, Command

def system_call(command):
  """Run a command and return stdout.

  Would be better to use subprocess.check_output, but this works on 2.6,
  which is still the system Python on CentOS 7."""
  p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
  return p.stdout.read()


name = "sourdough"
version = "0.1.%s" % (system_call('git rev-list HEAD --count'))


class CleanCommand(Command):
  """
  Add a clean option to setup.py's commands
  """
  description = "Clean up"
  user_options = []


  def initialize_options(self):
    self.cwd = None


  def finalize_options(self):
    self.cwd = os.getcwd()


  def run(self):
    assert os.getcwd() == self.cwd, "Must be in package root: %s" % self.cwd
    if os.path.isdir("build"):
      shutil.rmtree("build")
    if os.path.isdir("dist"):
      shutil.rmtree("dist")


setup(
  name=name,
  author="Joe Block",
  author_email="jpb@unixorn.net",
  description="sourdough is a tool to make an instance automatically register with Chef during boot",
  url="https://github.com/unixorn/bigriver.sourdough",
  packages=find_packages(),
  install_requires=[
    "boto>=2.38.0",
    "haze>=0.0.12",
    "logrus>=0.0.2",
    "pytoml>=0.1.11"
  ],
  cmdclass={
    "clean": CleanCommand,
  },
  version=version,
  download_url="https://github.com/unixorn/bigriver.sourdough/tarball/%s" % version,
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Operating System :: POSIX",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 2.7",
    "Topic :: System :: Systems Administration",
  ],
  keywords=['aws', 'chef', 'cloud', 'configuration-management', 'ec2'],
  entry_points={
    "console_scripts": [
      "sourdough-starter = %s.sourdough:run" % name,
      "sourdough-bootstrap = %s.sourdough:bootstrap" % name
    ]
  }
)