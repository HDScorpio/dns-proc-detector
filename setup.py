from setuptools import setup

setup(
    name='dns-proc-detector',
    version='0.1.0.dev1',
    packages=['dns_proc_detector'],
    url='https://github.com/HDScorpio/dns-proc-detector',
    license='MIT',
    author='Andrey Ulagashev',
    author_email='ulagashev.andrey@gmail.com',
    description='Process detector by DNS usage',
    python_requires='>= 3.6',
    setup_requires=['setuptools'],
    install_requires=['dnslib', 'psutil'],
    entry_points={
        'console_scripts': ['dns-proc-detect = dns_proc_detector.server:main']
    },
    classifier=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet'
        'Topic :: Internet :: Name Service (DNS)'

    ]
)
