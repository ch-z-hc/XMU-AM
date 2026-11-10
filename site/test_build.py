import unittest
import re
import subprocess
from pathlib import Path
from build import catalog, LOCAL_LIMIT


class CatalogTests(unittest.TestCase):
    def test_tracked_exam_names_are_normalized(self):
        paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=Path(__file__).resolve().parents[1]).decode().split('\0')
        exams = [p for p in paths if p.endswith('.pdf') and p.split('/')[0].startswith('大') and any(s in p.split('/') for s in ['期中', '期末'])]
        self.assertTrue(exams)
        for path in exams:
            name = Path(path).name
            with self.subTest(path=path):
                self.assertIsNone(re.search(r'[（）()]|级|学院|第[一二三123]学期|试题|卷|\bv\d', name))
                self.assertRegex(name, r'^(?:\d{4}(?:-\d{4})? .+(?:期中|期末)|.+(?:期中|期末) [A-Z])\.pdf$')
        series = {}
        for path in exams:
            match = re.match(r'^(.*(?:期中|期末)) ([A-Z])\.pdf$', path)
            if match:
                series.setdefault(match[1], []).append(match[2])
        for prefix, letters in series.items():
            with self.subTest(series=prefix):
                self.assertEqual(sorted(letters), [chr(ord('A') + i) for i in range(len(letters))])

    def entry(self, path, size=100):
        return {'type': 'blob', 'path': path, 'size': size, 'sha': 'a' * 40}

    def test_only_materials_and_no_duplicate_latex_directory(self):
        rows = catalog([self.entry('大三上/UNIX 系统编程/期中/2025 UNIX 期中.pdf'), self.entry('源文件/LaTeX 试卷/UNIX 系统编程/期中/2025 UNIX 期中.pdf'), self.entry('.github/workflows/pages.yml'), self.entry('大三上/UNIX 系统编程/期中/paper.tex')], 'revision')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['kind'], '试卷')
        self.assertTrue(rows[0]['preview'].startswith('files/'))

    def test_large_files_keep_encoded_immutable_github_links(self):
        row = catalog([self.entry('大一上/微积分/教材/A #1 + 中文.pdf', LOCAL_LIMIT + 1)], 'revision')[0]
        self.assertIsNone(row['preview'])
        self.assertIn('/revision/', row['download'])
        self.assertIn('A%20%231%20%2B%20', row['download'])
        self.assertEqual(row['kind'], '教材')

    def test_reviewed_mechanics_pdf_remains_a_note(self):
        rows = catalog([self.entry('大一上/力学/笔记/力学期末.pdf'), self.entry('大一上/力学/笔记/力学期末.md')], 'revision')
        self.assertEqual(len(rows), 1)
        self.assertEqual({row['kind'] for row in rows}, {'笔记'})
        note = next(row for row in rows if row['format'] == 'PDF')
        self.assertEqual(note['category'], '笔记')
        self.assertIn('%E7%AC%94%E8%AE%B0', note['source'])

    def test_exam_recollections_show_only_pdf(self):
        for stem in ['大一上/力学/期中/2024 力学期中', '大一下/热学/期中/2024-2025 热学期中']:
            with self.subTest(stem=stem):
                rows = catalog([self.entry(stem + '.md'), self.entry(stem + '.pdf')], 'revision')
                self.assertEqual([row['kind'] for row in rows], ['试卷'])
                self.assertEqual({row['category'] for row in rows}, {'期中'})

    def test_non_pdf_and_source_materials_are_excluded(self):
        paths = ['大一上/力学/笔记/file' + ext for ext in
                 ['.md', '.tex', '.txt', '.docx', '.ppt', '.png', '.c', '.rar']]
        paths += ['源文件/大一上/力学/笔记/file.pdf']
        self.assertEqual(catalog([self.entry(p) for p in paths], 'revision'), [])

    def test_uppercase_pdf_extension_is_supported(self):
        row = catalog([self.entry('大一下/热学/笔记/麦克斯韦分布的积分技巧.PDF')], 'revision')[0]
        self.assertEqual(row['format'], 'PDF')
        self.assertEqual(row['kind'], '笔记')

    def test_reviewed_study_aid_is_a_note(self):
        row = catalog([self.entry('大二下/面向对象程序设计/笔记/C++ 期末复习.pdf')], 'revision')[0]
        self.assertEqual(row['kind'], '笔记')


if __name__ == '__main__':
    unittest.main()
