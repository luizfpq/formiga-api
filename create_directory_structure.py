import os

def create_directory_structure(project_name):
    directories = [
        project_name+'/app/views',
        project_name+'/app/controllers',
        project_name+'/app/utils',
        project_name+'/config',
        project_name+'/migrations',
        project_name+'/tests'
    ]

    files = [
        project_name+'/app/__init__.py',
        project_name+'/app/models/__init__.py',
        project_name+'/app/views/__init__.py',
        project_name+'/app/controllers/__init__.py',
        project_name+'/app/utils/__init__.py',
        project_name+'/config/__init__.py',
        project_name+'/config/development.py',
        project_name+'/config/production.py',
        project_name+'/config/testing.py',
        project_name+'/run.py',
        project_name+'/requirements.txt'
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    for file in files:
        open(file, 'w').close()

    print("Estrutura de diretórios e arquivos criada com sucesso!")

if __name__ == "__main__":
    create_directory_structure()
