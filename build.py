#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import tools
from subprocess import check_call
import importlib
import os


def get_module_location():
    repo = os.getenv("CONAN_MODULE_REPO", "https://raw.githubusercontent.com/bincrafters/conan-templates")
    branch = os.getenv("CONAN_MODULE_BRANCH", "package_tools_modules")
    return repo + "/" + branch


def get_module_name():
    return os.getenv("CONAN_MODULE_NAME", "build_template_default")


def get_module_filename():
    return get_module_name() + ".py"


def get_module_url():
    return get_module_location() + "/" + get_module_filename()


if __name__ == "__main__":
    if os.environ.get('CONAN_DOCKER_IMAGE'):
        image = os.environ['CONAN_DOCKER_IMAGE']
        print("Installing tzdata in {}".format(image))
        modified_image = '{}-tzdata'.format(image)
        check_call(['docker', 'pull', image])
        check_call(['docker', 'run', '--name', 'img', image, 'bash', '-c', 'sudo apt-get update && sudo apt-get install -qy tzdata'])
        check_call(['docker', 'commit', 'img', modified_image])
        os.environ['CONAN_DOCKER_IMAGE'] = modified_image

    tools.download(get_module_url(), get_module_filename(), overwrite=True)

    module = importlib.import_module(get_module_name())

    builder = module.get_builder()

    builder.run()
