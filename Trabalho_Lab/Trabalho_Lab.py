#!/usr/bin/env python
# -*- coding: utf-8 -*-


from doctest import Example
from re import search
from datetime import datetime
import matplotlib.pyplot as plt
import pytz
import requests
import json
import numpy as np
from collections import Counter
def calcular_idade(data):
    formato = "%Y-%m-%dT%H:%M:%SZ"
    data_atual = datetime.now(pytz.UTC)
    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_objeto = datetime.strptime(data, formato).replace(tzinfo=fuso_horario_brasil)
    diferenca = data_atual - data_hora_objeto 
    idade_em_dias = diferenca.days
    idade_em_anos = idade_em_dias // 365
    return idade_em_anos
def replace_null(obj, replacement):
    if isinstance(obj, dict):
        return {k: replace_null(v, replacement) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_null(item, replacement) for item in obj]
    elif obj is None:
        return replacement
    else:
        return obj
def calcular_tempo_ultima_atualizacao(updated_at):
    agora = datetime.now()
    ultima_atualizacao = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')  # Convertendo a string para formato de data
    diferenca = agora - ultima_atualizacao
    segundos_total = abs(diferenca.total_seconds())     
    horas = int(segundos_total // 3600)
    minutos = int((segundos_total % 3600) // 60)
    return minutos # Diferença em horas


TOKEN = "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"

# URL da GitHub GraphQL API
URL = "https://api.github.com/graphql"

# Consulta GraphQL
query = """
query SearchRepositories($queryString: String!, $first: Int!, $after: String) {
  search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
    edges {
      node {
        ... on Repository {
          name
          createdAt
          updatedAt
          pullRequests(states: MERGED) {
            totalCount
          }
          releases {
            totalCount
          }
          primaryLanguage {
            name
          }
          issues {
            totalCount
          }
          issuesClosed: issues(states: CLOSED) {
            totalCount
          }
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
"""

def make_github_api_request(query, variables):
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(URL, json={"query": query, "variables": variables}, headers=headers)
    response_data = response.json()
    return response_data





def get_all_repositories():
    all_repositories = []
    after_cursor = None
    remaining_results = 100

    while remaining_results > 0:
        variables = {
            "queryString": "stars:>10000",
            "first": min(10, remaining_results),  # Limitando a 100 por consulta
            "after": after_cursor
        }
        response_data = make_github_api_request(query, variables)

        edges = response_data["data"]["search"]["edges"]
        all_repositories.extend(edges)
        remaining_results -= len(edges)

        page_info = response_data["data"]["search"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]

        if not has_next_page:
            break

    return all_repositories


if __name__ == "__main__":
    data = get_all_repositories()
    replacement_value = json.loads('{"name": "N/A"}') 
    data_with_replacement = replace_null(data, replacement_value)
    repositories = data_with_replacement
    nomes_repositorios = []
    idades = []
    totalpullreq = []
    totalreleases = []
    lamguegeprimary = []
    timeupdate = []
    totalissues = []
    totalCloseissues =[]
    for repo in repositories:
        name = repo['node']['name']
        created_at = repo['node']['createdAt']
        updated_at = repo['node']['updatedAt']
        totalrequest = repo['node']['pullRequests']['totalCount']
        totalreles = repo['node']['releases']['totalCount']
        linguagem = repo['node']['primaryLanguage']['name']  
        issues = repo['node']['issues']['totalCount']
        issueClose = repo['node']['issuesClosed']['totalCount']
        idade = calcular_idade(created_at)        
        #print(f"Nome: {name}, Idade em anos: {idade}")
        nomes_repositorios.append(name)
        idades.append(idade)
        totalpullreq.append(totalrequest)
        totalreleases.append(totalreles)
        lamguegeprimary.append(linguagem)
        totalissues.append(issues)
        totalCloseissues.append(issueClose)
        timeupdate.append(updated_at)
        

    plt.bar(nomes_repositorios, idades)
    plt.xlabel('Nome')
    plt.ylabel('Idade em anos')
    plt.title('Idade dos Repositorios em Anos')
    plt.xticks(rotation=90, ha='right')
    for i, v in enumerate(idades):
      plt.text(i, v + 0.5, str(v), color='black', ha='center')
    plt.tight_layout()
    plt.show()        

    
        # RQ2
    plt.bar(nomes_repositorios, totalpullreq)
    plt.xlabel('Nome')
    plt.ylabel('Total pull requests aceitas')
    plt.title('Total de pull requests aceitas')
    plt.xticks(rotation=90, ha='right')
    for i, v in enumerate(totalpullreq):
        plt.text(i, v, str(v), color='black', ha='center')
    plt.tight_layout()
    plt.show()      

        # RQ3
    plt.bar(nomes_repositorios, totalreleases)
    plt.xlabel('Nome')
    plt.ylabel('Total releases')
    plt.title('Total releases')
    plt.xticks(rotation=90, ha='right')
    for i, v in enumerate(totalreleases):
        plt.text(i, v, str(v), color='black', ha='center')
    plt.tight_layout()
    plt.show() 
    
        # RQ4
    tempos_ultima_atualizacao = [calcular_tempo_ultima_atualizacao(updated_at) for updated_at in timeupdate]

    plt.figure(figsize=(10, 6))
    plt.bar(nomes_repositorios, tempos_ultima_atualizacao, color='skyblue')
    plt.xlabel('Repositorio')
    plt.ylabel('Tempo desde a Ultima Atualizacao (minutos)')
    plt.title('Tempo desde a Ultima Atualizacao nos Repositorios')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


        #RQ5
    plt.figure(figsize=(10, 6))
    plt.bar(nomes_repositorios, lamguegeprimary, color='skyblue')
    plt.xlabel('Repositorio')
    plt.ylabel('Linguagem Principal')
    plt.title('Linguagem Principal dos Repositorios em Python')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()
    
        #RQ6
    razoes = []
    
    for fechadas, total in zip(totalCloseissues, totalissues):
        if total != 0:
           razao = fechadas / total
           razoes.append(razao)
        else:
           razoes.append(0)


    plt.figure(figsize=(10, 6))
    bars = plt.bar(nomes_repositorios, razoes, color='skyblue')
    plt.xlabel('Repositorio')
    plt.ylabel('Razao de Issues Fechadas / Total de Issues')
    plt.title('Razao de Issues Fechadas pelo Total de Issues nos Repositorios')
    plt.xticks(rotation=45, ha='right')
    for bar, razao in zip(bars, razoes):
       plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{razao:.2%}', ha='center', va='bottom')
    plt.tight_layout()
    plt.show()



 # if response.status_code == 200:
 #    data = response.json()

    
 #    print(data_with_replacement)
 #    repositories = data_with_replacement['data']['search']['edges']
      

 #    nomes_repositorios = []
 #    idades = []
 #    totalpullreq = []
 #    totalreleases = []
 #    lamguegeprimary = []
 #    timeupdate = []
 #    totalissues = []
 #    totalCloseissues =[]

 #    for repo in get_all_repositories():
 #        name = repo['node']['name']
 #        created_at = repo['node']['createdAt']
 #        updated_at = repo['node']['updatedAt']
 #        totalrequest = repo['node']['pullRequests']['totalCount']
 #        totalreles = repo['node']['releases']['totalCount']
 #        linguagem = repo['node']['primaryLanguage']['name']  
 #        issues = repo['node']['issues']['totalCount']
 #        issueClose = repo['node']['issuesClosed']['totalCount']

 #        idade = calcular_idade(created_at)        
 #        #print(f"Nome: {name}, Idade em anos: {idade}")
 #        nomes_repositorios.append(name)
 #        idades.append(idade)
 #        totalpullreq.append(totalrequest)
 #        totalreleases.append(totalreles)
 #        lamguegeprimary.append(linguagem)
 #        totalissues.append(issues)
 #        totalCloseissues.append(issueClose)
 #        timeupdate.append(updated_at)
    


# url = 'https://api.github.com/graphql';
# token = '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';
# headers = {
#     'Authorization': f'Bearer {token}',
# }
# query = """
# {
#   search(query: "stars:>10000", type: REPOSITORY, first: 100,after: ) {
#     edges {
#       node {
#         ... on Repository {
#           name
#           createdAt
#           updatedAt
#           pullRequests(states: MERGED) {
#             totalCount
#           }
#           releases {
#             totalCount
#           }
#           primaryLanguage {
#             name
#           }
#           issues {
#             totalCount
#           }
#           issuesClosed: issues(states: CLOSED) {
#             totalCount
#           }
#         }
#       }
#     }
#   }
# }
# """
# response = requests.post(url, json={'query': query}, headers=headers)

# if response.status_code == 200:
#     data = response.json()
#     replacement_value = json.loads('{"name": "N/A"}') 
#     data_with_replacement = replace_null(data, replacement_value)
#     print(data_with_replacement)
#     repositories = data_with_replacement['data']['search']['edges']
      

#     nomes_repositorios = []
#     idades = []
#     totalpullreq = []
#     totalreleases = []
#     lamguegeprimary = []
#     timeupdate = []
#     totalissues = []
#     totalCloseissues =[]

#     for repo in get_all_repositories():
#         name = repo['node']['name']
#         created_at = repo['node']['createdAt']
#         updated_at = repo['node']['updatedAt']
#         totalrequest = repo['node']['pullRequests']['totalCount']
#         totalreles = repo['node']['releases']['totalCount']
#         linguagem = repo['node']['primaryLanguage']['name']  
#         issues = repo['node']['issues']['totalCount']
#         issueClose = repo['node']['issuesClosed']['totalCount']

#         idade = calcular_idade(created_at)        
#         #print(f"Nome: {name}, Idade em anos: {idade}")
#         nomes_repositorios.append(name)
#         idades.append(idade)
#         totalpullreq.append(totalrequest)
#         totalreleases.append(totalreles)
#         lamguegeprimary.append(linguagem)
#         totalissues.append(issues)
#         totalCloseissues.append(issueClose)
#         timeupdate.append(updated_at)
#       # RQ1
#     plt.bar(nomes_repositorios, idades)
#     plt.xlabel('Nome')
#     plt.ylabel('Idade em anos')
#     plt.title('Idade dos Repositorios em Anos')
#     plt.xticks(rotation=90, ha='right')
#     for i, v in enumerate(idades):
#         plt.text(i, v + 0.5, str(v), color='black', ha='center')
#     plt.tight_layout()
#     plt.show()        

    
#     # RQ2
#     plt.bar(nomes_repositorios, totalpullreq)
#     plt.xlabel('Nome')
#     plt.ylabel('Total pull requests aceitas')
#     plt.title('Total de pull requests aceitas')
#     plt.xticks(rotation=90, ha='right')
#     for i, v in enumerate(totalpullreq):
#         plt.text(i, v, str(v), color='black', ha='center')
#     plt.tight_layout()
#     plt.show()      

#      # RQ3
#     plt.bar(nomes_repositorios, totalreleases)
#     plt.xlabel('Nome')
#     plt.ylabel('Total releases')
#     plt.title('Total releases')
#     plt.xticks(rotation=90, ha='right')
#     for i, v in enumerate(totalreleases):
#         plt.text(i, v, str(v), color='black', ha='center')
#     plt.tight_layout()
#     plt.show() 
    
#     # RQ4
#     tempos_ultima_atualizacao = [calcular_tempo_ultima_atualizacao(updated_at) for updated_at in timeupdate]

#     plt.figure(figsize=(10, 6))
#     plt.bar(nomes_repositorios, tempos_ultima_atualizacao, color='skyblue')
#     plt.xlabel('Repositorio')
#     plt.ylabel('Tempo desde a Ultima Atualizacao (minutos)')
#     plt.title('Tempo desde a Ultima Atualizacao nos Repositorios')
#     plt.xticks(rotation=45, ha='right')
#     plt.tight_layout()
#     plt.show()


#     #RQ5
#     plt.figure(figsize=(10, 6))
#     plt.bar(nomes_repositorios, lamguegeprimary, color='skyblue')
#     plt.xlabel('Repositorio')
#     plt.ylabel('Linguagem Principal')
#     plt.title('Linguagem Principal dos Repositorios em Python')
#     plt.xticks(rotation=45, ha='right')
    
#     plt.tight_layout()
#     plt.show()
    
#     #RQ6
#     razoes = []
    
#     for fechadas, total in zip(totalCloseissues, totalissues):
#         if total != 0:
#             razao = fechadas / total
#             razoes.append(razao)
#         else:
#             razoes.append(0)


#     plt.figure(figsize=(10, 6))
#     bars = plt.bar(nomes_repositorios, razoes, color='skyblue')
#     plt.xlabel('Repositorio')
#     plt.ylabel('Razao de Issues Fechadas / Total de Issues')
#     plt.title('Razao de Issues Fechadas pelo Total de Issues nos Repositorios')
#     plt.xticks(rotation=45, ha='right')
#     for bar, razao in zip(bars, razoes):
#         plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{razao:.2%}', ha='center', va='bottom')
#     plt.tight_layout()
#     plt.show()
# else:
#     print(f"Failed to retrieve data. Status Code: {response.status_code}")









