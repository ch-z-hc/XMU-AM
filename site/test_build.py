import unittest
from build import catalog, LOCAL_LIMIT


class CatalogTests(unittest.TestCase):
    def entry(self, path, size=100):
        return {'type': 'blob', 'path': path, 'size': size, 'sha': 'a' * 40}

    def test_only_materials_and_no_duplicate_latex_directory(self):
        rows = catalog([self.entry('大三上/UNIX 系统编程/期中/2025 UNIX 期中.pdf'), self.entry('LaTeX 试卷/UNIX 系统编程/期中/2025 UNIX 期中.pdf'), self.entry('.github/workflows/pages.yml'), self.entry('大三上/UNIX 系统编程/期中/paper.tex')], 'revision')
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['kind'], '试卷')
        self.assertTrue(rows[0]['preview'].startswith('files/'))

    def test_large_files_keep_encoded_immutable_github_links(self):
        row = catalog([self.entry('大一上/微积分/教材/A #1 + 中文.pdf', LOCAL_LIMIT + 1)], 'revision')[0]
        self.assertIsNone(row['preview'])
        self.assertIn('/revision/', row['download'])
        self.assertIn('A%20%231%20%2B%20', row['download'])
        self.assertEqual(row['kind'], '教材')

    def test_notes_directory_and_markdown_use_notes_column(self):
        rows = catalog([self.entry('大一下/热学/笔记/热学 - 复习.pdf'), self.entry('大一上/力学/期末/力学期末.md')], 'revision')
        self.assertEqual({row['kind'] for row in rows}, {'笔记'})
        note = next(row for row in rows if row['format'] == 'PDF')
        self.assertEqual(note['category'], '笔记')
        self.assertIn('%E7%AC%94%E8%AE%B0', note['source'])

    def test_exam_folder_study_aids_are_notes(self):
        row = catalog([self.entry('大三上/UNIX 系统编程/期中/UNIX 期中开卷速查.pdf')], 'revision')[0]
        self.assertEqual(row['kind'], '笔记')


if __name__ == '__main__':
    unittest.main()
