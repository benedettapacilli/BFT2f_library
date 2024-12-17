from setuptools import setup, find_packages

setup(
    name='BFT2F-library',
    version='1.0.0',
    description='BFT2F Algorithm Library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://dvcs.apice.unibo.it/pika-lab/courses/ds/projects/ds-project-pacilli-pieri-ay2324',
    author='Benedetta Pacilli, Valentina Pieri',
    author_email='benedetta.pacilli@studio.unibo.it, valentina.pieri5@studio.unibo.it',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
