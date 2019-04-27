from distutils.core import setup
from distutils.errors import DistutilsArgError
from distutils.command.install import install
import os, shutil

package_name = 'tobii_pro_wrapper'

class OverridenInstallCommend(install):
    user_options = install.user_options + [('lang=', None, 'specify the language')]
    def initialize_options(self):
        install.initialize_options(self)
        self.lang = None
    def finalize_options(self):
        install.finalize_options(self)
        if self.lang not in (None, 'hu'):
            raise DistutilsArgError("Only 'hu' language is allowed.")
    def run(self):
        # install localization files
        if self.lang == 'hu':
            source_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "locales", "hu", "LC_MESSAGES")
            target_dir = os.path.join(self.install_lib, package_name, "locales", "hu", "LC_MESSAGES")
            os.makedirs(target_dir)
            shutil.copyfile(os.path.join(source_dir, "all_strings.mo"), os.path.join(target_dir, "all_strings.mo")) 
        install.run(self)

setup(
    name=package_name,
    version='0.1',
    author='Olivia Guayasamin',
    author_email='oguayasa@gmail.com',
    packages=['tobii_pro_wrapper'],
    cmdclass={'install': OverridenInstallCommend},
    url='https://github.com/oguayasa/tobii_pro_wrapper',
    license='LICENSE.txt',
    description='Wrapper for the new Tobii Pro SDK',
    long_description='README.md',
    install_requires=[
        'numpy',
        'psychopy',
        'pyglet',
        'tobii_research==1.0.1.128',
    ],
)
