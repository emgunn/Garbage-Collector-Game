# -*- mode: python -*-

block_cipher = None


a = Analysis(['Collector.py'],
             pathex=['C:\\Users\\Eric Gunn\\Desktop\\Collector'],
             binaries=[],
             datas=[('data/leaderboard.txt', 'data'), ('data/options/*txt', 'data/options'), ('images/*.png', 'images'), ('sounds/*.wav', 'sounds'), (
             'freesansbold.ttf', '.')],
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
          name='Collector',
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
               name='Collector')
