import os
from functools import lru_cache

import requests

from data import query

github_api_endpoint = "https://api.github.com"
github_graph_api_endpoint = "https://api.github.com/graphql"


class static:
    def __init__(self,start_time,end_time):
        self.ci = os.getenv('CI')
        self.start_time = start_time
        self.end_time = end_time

    json_header = {"Accept": "application/vnd.github.v3+json"}
    beta_json_header = {"Accept": "application/vnd.github.inertia-preview+json"}

    time_struct = "%Y-"

    GraphQL_query_template = query

    @property
    @lru_cache
    def _github_token(self):
        if self.ci:
            GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
        else:
            from conf import GITHUB_TOKEN
        if not GITHUB_TOKEN:
            raise RuntimeError("Cannot running without Github Token.")
        return GITHUB_TOKEN

    @property
    @lru_cache
    def _github_auth_param(self):
        if self._github_token:
            return {'access_token': self._github_token}

    @property
    @lru_cache
    def _github_auth_header(self):
        if self._github_token:
            return {'Authorization': 'bearer ' + self._github_token}

    @property
    @lru_cache
    def _authed_session(self):
        s = requests.session()
        s.params.update(self._github_auth_param)
        return s

    @property
    @lru_cache
    def _authed_graph_session(self):
        s = requests.session()
        s.headers.update(self._github_auth_header)
        return s

    @property
    @lru_cache
    def session(self):
        s = self._authed_session
        s.headers.update(self.json_header)
        return s

    @property
    @lru_cache
    def beta_session(self):
        s = self._authed_session
        s.headers.update(self.beta_json_header)
        return s

    @property
    @lru_cache
    def user(self):
        s = self._authed_session
        resp = s.get(github_api_endpoint + '/user').json()
        return resp['login']

    @lru_cache
    def _get_query(self):
        return self.GraphQL_query_template.replace("nameholder", self.user) \
            .replace("startholder", self.start_time) \
            .replace("endholder", self.end_time)

    @lru_cache
    def get_info(self,):
        query_str = self._get_query()
        resp = self._authed_graph_session.post(github_graph_api_endpoint, json={
            "query": query_str
        }).json()
        return resp


