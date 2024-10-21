from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(name='omada_client',
      version='1.1.3',
      description='Execute API calls to Omada Controller from python code',
       long_description=readme(),
      long_description_content_type='text/markdown',
      install_requires=[
            'requests==2.32.3', 
            'urllib3==2.2.3'
      ],
      packages=['omada_client'],
      url='https://github.com/ErilovNikita/omada_client',
      author_email='minitwiks@gmail.com',
      zip_safe=False)