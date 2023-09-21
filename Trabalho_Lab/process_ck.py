import subprocess
import requests
import zipfile
import csv
import os

ck_path = "C:/Users/Marco/Documents/ck-master/ck-master"
start = 6
end = 10

def import_csv(path):
    response = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            response.append(row)
    return response

def download_zip(name, file_url):
    if not os.path.isdir(f'downloads'):
        os.mkdir(f'downloads')
    path = "downloads/"+name+".zip"

    r = requests.get(file_url, allow_redirects=True)
    open(path, 'wb').write(r.content)

def unzip(name):
    if not os.path.isdir(f'extract'):
        os.mkdir(f'extract')
    
    path = "downloads/"+name+".zip"
    with zipfile.ZipFile(path, 'r') as arq:
        path_download = 'extract/'+name
        if not os.path.isdir(path_download):
            os.mkdir(path_download)
          
        arq.extractall(path_download)

def clone_repository(clone_url):
    if not os.path.isdir(f'downloads'):
        os.mkdir(f'downloads')
    
    command = "git clone "+clone_url
    diretory = os. getcwd()+'\\downloads'
    print(subprocess.check_output(command, shell=True, universal_newlines=True, cwd=diretory)) 

def extract_ck(name):
    if not os.path.isdir(f'extract'):
        os.mkdir(f'extract')
    if not os.path.isdir(f'extract/'+name):
        os.mkdir(f'extract/'+name)    
    repository_path = os.getcwd()+'\\downloads\\'+name
    repository_destiny = os.getcwd()+'\\extract\\'+name
    command = "java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar "+repository_path+" false 0 true "+repository_destiny+"/"
    subprocess.check_output(command, shell=True, universal_newlines=True, cwd=ck_path)

def delete_file(name):
    path = 'downloads/'+name
    os.system('rmdir /S /Q "{}"'.format(path))
    #for f in os.listdir(path):
    #    os.remove(os.path.join(path,f))

if __name__ == '__main__':
    data = import_csv('csv\\questao00.csv')

    count = start - 1
    while count < end:
        count += 1
        try:
            clone_repository(data[count]['clone_url'])
            extract_ck(data[count]['name'])
            delete_file(data[count]['name'])
        except:
            with open("erro.txt", "a") as f:
                f.write(data[count]['clone_url'])



#if not os.path.isdir(f'extract'):
#    os.mkdir(f'extract')




#link= "git clone https://github.com/daimajia/AndroidViewAnimations"
#comando = "java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar D:/PUC/downloads/AndroidNote false 0 true D:/PUC/aqui/"
#diretory = "D:/PUC/downloads/extract/"
#print(subprocess.check_output(link, shell=True, universal_newlines=True, cwd=diretory))

#dir = "D:\\PUC\\downloads\\extract"
#for f in os.listdir(dir):
#    os.remove(os.path.join(dir,f))

#comando = "java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar D:/PUC/downloads/AndroidNote false 0 true D:/PUC/aqui/"
#diretory = "C:/Users/Marco/Documents/ck-master/ck-master"
#print(subprocess.check_output(comando, shell=True, universal_newlines=True, cwd=diretory))


