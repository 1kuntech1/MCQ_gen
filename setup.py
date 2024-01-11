from setuptools import find_packages, setup

setup(
    name = 'mcqgenrator',
    version = '0.0.1',
    description = "mcqgenrator can genrate the mcq by receving inputs",
    author = 'Kundan',
    author_email = 'kundan9910558927@gmail.com',
    install_requires = ["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages(),
    long_description = 'mcqgenrator python module',
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: python :: 3.7 - 3.10",
        "Operating System :: os Independent",
        ],
    )
