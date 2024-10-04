import os

required_os_envs = {'ZYTE_API_KEY', 'CRAWLERA_KEY', 'STATIC_IP_PROXY'}

if any(os.getenv(key) is None for key in required_os_envs):
    raise RuntimeError('Missing some or all of environment variables: {}'.format(', '.join(required_os_envs)))
