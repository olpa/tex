#

# rm -f MANIFEST; python setup.py sdist

from distutils.core import setup
setup(name='template_designer',
      version='100127',
      packages=['template_designer', 'template_designer.colors', 'template_designer.data', 'template_designer.help', 'template_designer.menu', 'template_designer.printing', 'template_designer.propertiespanel', 'template_designer.settingsdialog', 'template_designer.tdparser'],
      package_dir = {'template_designer': '.'},
      package_data = {'template_designer': [
        'help/*/*.html', 'help/*/*/*', 'definitions/*',
        'graphics/oxygen/*/*.png', 'graphics/oxygen/*/*/*.png',
        'templatedesigner.conf', 'logo.png',  'splash.png',
        'AUTHOR', 'COPYING', 'DESCRIPTION', 'INSTALLATION'
        ]},
      )
