import os

def extract():
    print("##############____________ STARTING EXTRACTION")
    os.system("python ./extract.py")

def transform():
    print("##############____________ STARTING TRANSFORMATION")
    os.system("python ./transform.py")

def load():
    print("##############____________ DATA IS BEING INGESTED")
    os.system("python ./load.py")


def main():
    extract()
    transform()
    load()

    print("PIPELINE PROCESSES SUCCESSFULY EXECUTED")


main()