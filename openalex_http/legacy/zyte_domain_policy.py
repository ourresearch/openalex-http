import csv
import json
import os
import re
from enum import Enum
from typing import Dict, Optional

class ZytePolicyType(Enum):
    URL = 'url'
    DOI = 'doi'

class ZyteProfile(Enum):
    PROXY = 'proxy'
    API = 'api'
    BYPASS = 'bypass'

from dataclasses import dataclass

@dataclass
class ZytePolicy:
    id: int
    type: str
    regex: str
    profile: str
    params: Optional[Dict[str, str]] = None
    priority: int = 1
    parent_id: int = None
    def __eq__(self, other):
        return (isinstance(other, ZytePolicy) and
                self.id == other.id and
                self.type == other.type and
                self.regex == other.regex and
                self.profile == other.profile and
                self.params == other.params and
                self.priority == other.priority and
                self.parent_id == other.parent_id)

    def match(self, doi_or_domain):
        return bool(re.search(self.regex, doi_or_domain))


def get_zyte_domain_policies():
    fpath = os.path.join(os.path.dirname(__file__), 'data', 'zyte_domain_policies.csv')
    f = open(fpath)
    reader = csv.DictReader(f)
    domain_policies = [ZytePolicy(id=int(row['id']),
                                    type=row['type'],
                                    regex=row['regex'],
                                    profile=row['profile'],
                                    params=json.loads(row['params']) if row['params'] else None,
                                    priority=int(row['priority']) if row['priority'] else 1,
                                    parent_id=int(row['parent_id']) if row['parent_id'] else None)
                        for row in reader]
    return domain_policies

_ALL_POLICIES = get_zyte_domain_policies()


def get_matching_policies(url):
    matching_policies = [policy for policy in _ALL_POLICIES if
                         policy.match(url)]
    if not matching_policies:
        return []
    parent_policies = sorted(
        [policy for policy in matching_policies if policy.parent_id is None],
        key=lambda policy: (
            policy.type == 'api' and policy.params is not None,
            policy.type == 'api',
            policy.type == 'proxy'
        )
    )
    if len(parent_policies) > 1 and parent_policies[0].params is not None and \
            parent_policies[1].params is not None:
        raise Exception(
            f'Colliding Zyte HTTP policies for URL: {url} - {parent_policies}')
    parent_policy = parent_policies[0]
    retry_policies = sorted(
        [policy for policy in matching_policies if
         policy.parent_id == parent_policy.id],
        key=lambda policy: (
            policy.type == 'api' and policy.params is not None,
            policy.type == 'api',
            policy.type == 'proxy'
        )
    )
    return [parent_policy] + retry_policies