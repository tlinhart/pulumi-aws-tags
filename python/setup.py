from setuptools import find_packages, setup


def long_description():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='pulumi-aws-tags',
    version='0.0.2',
    author='Tomáš Linhart',
    author_email='pasmen@gmail.com',
    description='Pulumi package that helps manage tags for AWS resources',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/tlinhart/pulumi-aws-tags',
    license='MIT',
    packages=find_packages(),
    keywords='pulumi aws tags',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=[
        'pulumi>=2.0.0,<3.0.0',
        'pulumi-aws>=3.2.0,<4.0.0'
    ]
)
