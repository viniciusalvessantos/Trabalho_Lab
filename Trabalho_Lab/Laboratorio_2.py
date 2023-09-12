#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
import os
from datetime import datetime
import pytz

URL = 'https://api.github.com/graphql'
TOKEN = ''
headers = {
    'Authorization': f'Bearer {TOKEN}',
}

query = """
query SearchRepositories($queryString: String!, $first: Int!, $after: String) {
  search(query: $queryString, type: REPOSITORY, first: $first, after: $after) {
    edges {
      node {
        ... on Repository {
          name
          defaultBranchRef {
            target {
              ... on Commit {
                zipballUrl
              }
            }
          }
          stargazers {
            totalCount
          }
          createdAt
          releases {
            totalCount
          }
          primaryLanguage {
            name
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
    response = {'data': {'search': {'edges': []}}}
    after_cursor = None
    remaining_results = 10

    while remaining_results > 0:
        variables = {
            "queryString": "stars:>1000 and language:java",
            "first": min(10, remaining_results),  # Limitando a 10 por consulta
            "after": after_cursor
        }
        response_data = make_github_api_request(query, variables)

        edges = response_data["data"]["search"]["edges"]
        response["data"]["search"]["edges"].extend(edges)
        remaining_results -= len(edges)
        
        page_info = response_data["data"]["search"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        after_cursor = page_info["endCursor"]

        print(remaining_results)

        if not has_next_page:
            break

    return response

def calculate_age(data):
    formato = "%Y-%m-%dT%H:%M:%SZ"
    data_atual = datetime.now(pytz.UTC)
    fuso_horario_brasil = pytz.timezone('America/Sao_Paulo')
    data_hora_objeto = datetime.strptime(data, formato).replace(tzinfo=fuso_horario_brasil)
    diferenca = data_atual - data_hora_objeto 
    idade_em_dias = diferenca.days
    idade_em_anos = idade_em_dias // 365
    return idade_em_anos

def filter_query(query):
    response = []
    for node in query['data']['search']['edges']:
        response.append({
            'name': node['node']['name'],
            'stars': node['node']['stargazers']['totalCount'],
            'age': calculate_age(node['node']['createdAt']),
            'releases': node['node']['releases']['totalCount'],
            'language': node['node']['primaryLanguage']['name'],
            'clone_url': node['node']['defaultBranchRef']['target']['zipballUrl']
        })
    return response

def export_csv(objetc, name):
    fieldnames = []
    for a in objetc[0]:
        fieldnames.append(a)

    if not os.path.isdir(f'csv'):
        os.mkdir(f'csv')

    with open(f'csv/'+name+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(objetc)

def export_zip(date):
    if not os.path.isdir(f'downloads'):
        os.mkdir(f'downloads')
    for item in date:
        name = item["name"]
        url = item["clone_url"]
        r = requests.get(url, allow_redirects=True)
        open("downloads/"+name+".zip", 'wb').write(r.content)

if __name__ == '__main__':
  query = get_all_repositories()
  if query['data'] is None:
      for erro in query['errors']:
          print(erro['message'])
  else:
    date = filter_query(query)
    export_csv(date,"questao00")
    export_zip(date)
