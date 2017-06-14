import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_long_description():
    path = os.path.join(os.path.dirname(__file__), 'README.md')

    try:
        import pypandoc
        return pypandoc.convert(path, 'rst')
    except(IOError, ImportError, RuntimeError):
        with open(path, 'r') as f:
        	return f.read()

setup(
    name='manspy',
    version='0.1.0',
    license='LGPL-3.0',
    description='Management system',
    packages=['manspy', 'ifmodules'],
    #long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    long_description=get_long_description(),
    author='Konstantin Polyakov',
    author_email='shyzik93@mail.ru',
    maintainer='Konstantin Polyakov',
    maintainer_email='shyzik93@mail.ru',
    url='https://github.com/shyzik93/ManSPy',
    download_url='https://github.com/shyzik93/manspy/archive/master.zip',

    install_requires=['tkinter'],

    entry_points={
        'console_scripts': ['manspy = manspy.cli:do_cmd']
    },
    include_package_data=True,
    classifiers=[
		"Environment :: Console",
		"Natural Language :: English",
        "Natural Language :: Esperanto",
		"Programming Language :: Python :: 3.4",
		"Topic :: Scientific/Engineering",
        "Topic :: Text Processing :: Linguistic"
    ]
)

'''
# uninstall globally
sudo python setup.py install --record installed.txt
sudo xargs rm -vr < installed.txt

# uinstall in your home directory
python setup.py install --user --record installed.txt
xargs rm -vr < installed.txt

Из папки rep://dist:
cd manspy-0.1.0 ; xargs rm -vr < installed.txt ; cd .. ; tar -xzf manspy-0.1.0.tar.gz ; cd manspy-0.1.0 ; python3 setup.py install ; cd ..
'''