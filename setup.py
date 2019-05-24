from setuptools import setup

setup(
    name="Construct A Cog",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.bam',
                '**/*.py',
            ],
            'gui_apps': {
                'Construct A Cog': 'main.py',
            },
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
