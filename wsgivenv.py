import sys
import os

def activate_venv(path, venv="flask"):
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), venv)
    if sys.platform == 'win32':
        bin_dir = os.path.join(path, 'Scripts')
        site_packages = os.path.join(base, 'Lib', 'site-packages')
    else:
        bin_dir = os.path.join(path, 'bin')
        site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
    os.environ['PATH'] = bin_dir + os.pathsep + os.environ['PATH']
    prev_sys_path = list(sys.path)
    import site
    site.addsitedir(site_packages)
    sys.prefix, sys.real_prefix = path, sys.prefix

    # Move the added items to the front of the path:
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path