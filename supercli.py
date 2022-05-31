from asyncio import FastChildWatcher
import click
import pandas as pd
import json
import urllib.request
import os

@click.group()
def supercli():
    '''
    Retrives data from the csv File

    '''
    pass

@click.group(name='get')
def get_group():
    '''
    Group of commands to get something
    '''
    pass

def download_file(url):
    path = os.path.abspath(os.getcwd())
    filename, headers = urllib.request.urlretrieve(url, filename= path + '/package.json')

def read_json(dependency):
    with open('package.json', 'r') as f:
        data = json.load(f)
        data = data['dependencies'][dependency]
        data = data.replace('^','')
        return data

def version_satisfied(version, dependency):
    x = version.split('.')
    y = read_json(dependency)
    y = y.split('.')
    for i in range(len(y)):
        if(y[i] < x[i]):
            return False
    return True

def track_dependencies(filename, versions, version_satisfied):
    df = pd.read_csv(filename)
    df['version'] = versions
    df['version_satisfied'] = version_satisfied
    df.to_csv('updated_csv.csv', index=False)
    return df




@click.command(name='dataset')
@click.argument('filename')
@click.argument('dependency')
@click.argument('version')
def read_data(filename, dependency, version):
    df = pd.read_csv(filename)
    links = df['repo']
    versions = []
    versions_satisfied = []

    for test in links:
        test += 'main/package.json'
        url = test.replace('github.com','raw.githubusercontent.com')
        download_file(url)
        v = read_json(dependency)
        b = version_satisfied(version, dependency)
        versions.append(v)
        versions_satisfied.append(b)
        os.remove("package.json")
    
    data = track_dependencies(filename, versions, versions_satisfied)
    print(data)


get_group.add_command(read_data)

supercli.add_command(get_group)