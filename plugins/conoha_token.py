ANSIBLE_METADATA = {
  'metadata_version': '1.1',
  'status': ['preview'],
  'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: conoha_token

short_description: Get a ConoHa access token

version_added: "2.4"

description:
    - ""

options:
    username:
        description:
            - the username displayed in https://manage.conoha.jp/API/
        required: true
    password:
        description:
            - the password set in https://manage.conoha.jp/API/
        required: True

extends_documentation_fragment:
    - azure

author:
    - ohtacaesar (@ohtacaesar)
'''

EXAMPLES = '''
# Pass in a message
- name: Get a Conoha Access Token
  conoha_token:
    username: username
    password: password
  register: token

'''

RETURN = '''
token:
    description: ConoHa Access Token
    type: str
    returned: always
'''

import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url


def run_module():
  module_args = dict(
      username=dict(type='str', required=True),
      password=dict(type='str', required=True, no_log=True),
      tenantId=dict(type='str', required=False),
  )

  result = dict(
      changed=False,
      token='token',
  )

  module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)

  payload = {
    'auth': {
      'passwordCredentials': {
        'username': module.params['username'],
        'password': module.params['password'],
      }
    }
  }
  if 'tenantId' in module.params:
    payload['tenantId'] = module.params['tenantId']

  resp, info = fetch_url(
      module,
      url='https://identity.tyo1.conoha.io/v2.0/tokens',
      data=json.dumps(payload),
      headers={'Content-type': 'application/json'},
      method='POST',
  )

  # result['info'] = info
  body = json.loads(resp.read())
  result['token'] = body['access']['token']['audit_ids'][0]

  # if module.params['name'] == 'fail me':
  #  module.fail_json(msg='You requested this to fail', **result)

  module.exit_json(**result)


def main():
  run_module()


if __name__ == '__main__':
  main()
