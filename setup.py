from setuptools import setup
import os

def readme():
  with open('README.md', 'r') as f:
    return f.read()

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def read_version():
    version_ns = {}
    with open(os.path.join("omada_client", "_version.py")) as f:
        exec(f.read(), version_ns)
    return version_ns["__version__"]

setup(name='omada_client',
      version=read_version(),
      description='Execute API calls to Omada Controller from python code',
      long_description=readme(),
      long_description_content_type='text/markdown',
      install_requires=read_requirements("requirements.txt"),
      extras_require={
            "dev": read_requirements("requirements-dev.txt"),
      },
      license = "MIT",
      python_requires=">=3.9",
      packages=['omada_client'],
      url='https://github.com/ErilovNikita/omada-client',
      author_email='minitwiks@gmail.com',
      zip_safe=False)