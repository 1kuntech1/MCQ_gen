from setuptools import find_packages, setup

setup(
    name ='mqgenrator',
    verision = '0.0.1',
    author = '1kuntech1',
    author_email = 'Kundan9910558927@gmail.com',
    install_requirments = ['openai', 'langchain', 'streamlit', 'python-dotenv', 'PyPDF2'],
    packages = find_packages()
)