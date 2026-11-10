"""Build a static course catalog from tracked materials; no third-party dependencies."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
TERMS = ['大一上', '大一下', '大二上', '大二下', '大三上', '大三下', '大四上', '大四下']
EXTENSIONS = {'.pdf', '.md', '.txt', '.docx', '.doc', '.ppt', '.pptx', '.rar', '.zip', '.c', '.cpp'}
LOCAL_LIMIT = 16 * 1024 * 1024


def catalog(tree, revision):
    entries = []
    for item in tree:
        path = item['path']
        parts = path.split('/')
        suffix = Path(path).suffix.lower()
        if item['type'] != 'blob' or len(parts) < 3 or parts[0] not in TERMS or suffix not in EXTENSIONS:
            continue
        category = parts[2] if len(parts) > 3 else '笔记'
        kind = '试卷' if category in {'期中', '期末', '考试资料（期次待核）'} else ('教材' if category == '教材' else '笔记')
        # Directories reflect content review; format and title do not determine kind.
        local = suffix == '.pdf' and item['size'] <= LOCAL_LIMIT
        url_path = quote(path, safe='/')
        local_path = f"files/{item['sha']}{suffix}" if local else None
        entries.append({
            'id': path, 'name': Path(path).stem, 'filename': parts[-1], 'term': parts[0], 'course': parts[1],
            'category': category, 'kind': kind, 'format': suffix[1:].upper(), 'size': item['size'],
            'preview': local_path,
            'download': local_path or f'https://raw.githubusercontent.com/ch-z-hc/XMU-AM/{revision}/{url_path}',
            'source': f'https://github.com/ch-z-hc/XMU-AM/blob/{revision}/{url_path}',
        })
    return sorted(entries, key=lambda e: (TERMS.index(e['term']), e['course'], e['category'], e['name']))


def git_tree():
    data = subprocess.check_output(['git', 'ls-tree', '-r', '-l', '-z', 'HEAD'], cwd=ROOT).decode()
    result = []
    for row in data.split('\0'):
        if not row:
            continue
        header, path = row.split('\t', 1)
        _, kind, sha, size = header.split()
        result.append({'path': path, 'type': kind, 'sha': sha, 'size': int(size) if size != '-' else 0})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tree', type=Path, help='GitHub recursive tree snapshot for a sparse local checkout')
    parser.add_argument('--preview', action='store_true', help='Link available PDFs locally; do not fetch missing files')
    args = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    if args.tree:
        snapshot = json.loads(args.tree.read_text())
        if snapshot.get('truncated'):
            raise ValueError('Incomplete Git tree')
        tree = snapshot['tree']
    else:
        tree = git_tree()
    entries = catalog(tree, revision)
    if not entries:
        raise ValueError('No course materials found')
    out = ROOT / 'site/dist'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    for name in ['index.html', 'style.css', 'app.js']:
        shutil.copyfile(ROOT / 'site' / name, out / name)
    (out / '.nojekyll').touch()
    (out / 'catalog.json').write_text(json.dumps({'terms': [t for t in TERMS if any(e['term'] == t for e in entries)], 'files': entries}, ensure_ascii=False), encoding='utf-8')
    total = 0
    for entry in entries:
        if not entry['preview']:
            continue
        target = out / entry['preview']
        if target.exists():
            continue
        source = ROOT / entry['id']
        target.parent.mkdir(exist_ok=True)
        if args.preview:
            if source.exists():
                target.symlink_to(source)
        else:
            if not source.is_file():
                raise FileNotFoundError(source)
            shutil.copyfile(source, target)
        total += entry['size']
    if total > 900 * 1024 * 1024:
        raise ValueError('Pages artifact exceeds the size budget')
    print(f'{len(entries)} materials, {len(set((e["term"], e["course"]) for e in entries))} courses; PDFs {total / 1024**2:.1f} MiB')


if __name__ == '__main__':
    main()
