import zipfile
import argparse
import requests
import shutil
import os
import os.path as path
import re
import fnmatch

def getLatestReleaseVersion():
    r = requests.get('https://github.com/AnalyticalGraphicsInc/cesium/releases/latest', allow_redirects=True)
    print (r.url)
    l = r.url
    tag = re.search('(?:/releases/tag/)(.*)', l, re.IGNORECASE).group(1)
    return tag

def download(basedir, tag):
    filename = 'Cesium-{}.zip'.format(tag)
    url = 'https://github.com/AnalyticalGraphicsInc/cesium/releases/download/{}/{}'.format(tag, filename)
    print('Download {}'.format(url))
    r = requests.get(url)

    downloaded = path.join(basedir, filename)
    open(downloaded, 'wb').write(r.content)

    print('Saved as {}'.format(downloaded))

    return downloaded


def unzip(basedir, downloaded, tag, do_not_delete):
    dest = path.join(basedir, 'cesium-{}'.format(tag))

    if not path.exists(dest):
        os.mkdir(dest)

    print('Extract to'.format(dest))
    with zipfile.ZipFile(downloaded, 'r') as zip_ref:
        zip_ref.extractall(dest)

    if not do_not_delete:
        print('Remove temp zip {}'.format(downloaded))
        os.remove(downloaded)

def purge_dir(folder, remove_root = False, skip=[]):
    print('Purge {}'.format(folder))
    for filename in os.listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if any(fnmatch.fnmatch(filename, p) for p in skip):
                print("Skip {}".format(file_path))
                continue
            if path.isfile(file_path) or path.islink(file_path):
                os.unlink(file_path)
            elif path.isdir(file_path):
                if '.git' in filename:
                    print('Skip .git folder')
                else:
                    shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete {}. Reason: {}'.format(file_path, e))
    if remove_root:
        shutil.rmtree(folder)

def copy_dir(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download cesium releases')


    parser.add_argument('--tag', dest='tag', default='latest',
                    help='Download specific tag')

    parser.add_argument('--only-tag', dest='onlytag', action='store_true',
        help='Show latest tag, and immediately exit')

    parser.add_argument('--save-zip', dest='save', action='store_true',
        help='Do not delete zip file')

    parser.add_argument('--overwrite', dest='overwrite', action='store_true',
        help='Overwrite existing downloaded release')

    parser.add_argument('--base-dir', dest='basedir',
        help='Base directory')

    parser.add_argument('--copy-build', dest='copy_to',
        help='Copy build (/Build/Cesium) to destination dir, overwrites existing')

    parser.add_argument('--remove', dest='remove', action='store_true',
        help='Remove downloaded release, after copy')

    args = parser.parse_args()

    tag = args.tag
    if tag is 'latest' or args.onlytag:
        latest_tag = getLatestReleaseVersion()
        if args.onlytag:
            print(latest_tag)
            exit(0)

        print('Latest release tag: {}'.format(latest_tag))
        tag = latest_tag

    basedir = path.dirname(__file__)
    if args.basedir:
        basedir = args.basedir
    print('Basedir: {}'.format(basedir))

    dest = path.join(basedir, 'cesium-{}'.format(tag))
    not_empty = path.exists(path.join(dest, 'package.json'))

    if path.exists(dest) and not_empty:
        print('Release {} already downloaded'.format(tag))

        if args.overwrite:
            print('Overwrite {}'.format(dest))
            shutil.rmtree(dest)

            downloaded = download(basedir, tag)
            unzip(basedir, downloaded, tag, args.save)

    else:
        downloaded = download(basedir, tag)
        unzip(basedir, downloaded, tag, args.save)

        if args.copy_to:
            overwrite = True
            if os.path.exists(path.join(args.copy_to, 'version.txt')):
                with open(path.join(args.copy_to, 'version.txt'), "r") as version:
                    latest_tag = version.read()
                    if latest_tag == tag:
                        overwrite = False
                        print("Latest is already {} version".format(tag))

            if overwrite:
                purge_dir(args.copy_to)
                copy_dir(path.join(dest, 'Build', 'Cesium'), args.copy_to)

            with open(path.join(args.copy_to, 'version.txt'), "w") as version:
                version.write(tag)

    if args.remove:
        purge_dir(dest, skip=['package.json'])
