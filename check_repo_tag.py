# Copyright 2016 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import requests
import argparse

_PROJECT_ALL = '/api/v3/projects/all?page=%s&per_page=100'
_PROJECT_OWN = '/api/v3/projects?page=%s&per_page=100'
_PROJECT_LABELS = '/api/v3/projects/%s/labels'
_PROJECT_INFO = '/api/v3/projects/%s'
_USER_INFO = '/api/v3/users/%s'


def get_all_projects(gitlab_host, token, is_admin=False):
    headers = {
        'content-type': 'application/json',
        'PRIVATE-TOKEN': token
    }

    # get all projects
    if is_admin:
        url = 'http://%s%s' % (gitlab_host, _PROJECT_ALL)
    else:
        url = 'http://%s%s' % (gitlab_host, _PROJECT_OWN)
    i = 1
    all_project_list = []
    while True:

        project_list_per_page = requests.get(url % i, headers=headers)
        if not len(project_list_per_page.json()):
            break
        i += 1
        all_project_list.extend(project_list_per_page.json())

    print len(all_project_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help="gitlab host ip adddress or DNS name", required=True)
    parser.add_argument('--token', type=str, help='gitlab token for user', required=True)
    parser.add_argument('--admin', type=bool, help='token belong to admin or not', default=False)
    args = parser.parse_args()
    get_all_projects(args.host, args.token, args.admin)


if __name__ == '__main__':
    main()
