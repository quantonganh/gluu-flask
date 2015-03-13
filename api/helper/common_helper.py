# -*- coding: utf-8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2014 Gluu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import hashlib
import os
import random
import string
import subprocess
import sys

# Default charset
_DEFAULT_CHARS = "".join([string.ascii_uppercase,
                          string.digits,
                          string.lowercase])


def run(command, exit_on_error=True, cwd=None):
    try:
        print("Shell command called (blocking): {}".format(command))
        return subprocess.check_output(command, stderr=subprocess.STDOUT,
                                       shell=True, cwd=cwd)
    except subprocess.CalledProcessError, e:
        if exit_on_error:
            sys.exit(e.returncode)
        else:
            raise


def get_random_chars(size=12, chars=_DEFAULT_CHARS):
    return ''.join(random.choice(chars) for _ in range(size))


def encrypt_password(password):
    # borrowed from https://github.com/GluuFederation/community-edition-setup
    # /blob/c23aa9a4353867060fc9faf674c72708059ae3bb/setup.py#L960-L966
    salt = os.urandom(4)
    sha = hashlib.sha1(password)
    sha.update(salt)
    b64encoded = '{0}{1}'.format(sha.digest(), salt).encode('base64').strip()
    encrypted_password = '{{SSHA}}{0}'.format(b64encoded)
    return encrypted_password
