# -*- mode: python -*-

block_cipher = None


a = Analysis(['dungeon.py'],
             pathex=['D:\\Files\\Documents\\Projects\\Spark'],
             binaries=[('BearLibTerminal.dll', '.')],
             datas=[('enemies.json', '.'), ('items.json', '.'), ('materials.json', '.'), ('names.json', '.'), ('unifont-8.0.01.ttf', '.'), ('data/dungeon/dungeon_adjectives.txt', 'data/dungeon'), ('data/dungeon/dungeon_attributes.txt', 'data/dungeon'), ('data/dungeon/dungeon_words.txt', 'data/dungeon'), ('data/dungeon/geographical_features.txt', 'data/dungeon'), ('names/female.txt', 'names'), ('names/male.txt', 'names'), ('names/female_dist.txt', 'names'), ('names/male_dist.txt', 'names')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='dungeon',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dungeon')
