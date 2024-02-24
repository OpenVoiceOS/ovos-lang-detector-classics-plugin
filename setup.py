import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]



PLUGIN_ENTRY_POINT = (
    'ovos-lang-detector-plugin-voter=ovos_lang_detector_classics_plugin:VotingLangDetectPlugin',
    'ovos-lang-detector-plugin-cld2=ovos_lang_detector_classics_plugin.neon_cld2:Pycld2Detector',
    'ovos-lang-detector-plugin-cld3=ovos_lang_detector_classics_plugin.neon_cld3:Pycld3Detector',
    'ovos-lang-detector-plugin-langdetect=ovos_lang_detector_classics_plugin.neon_langdetect:LangDetectDetector',
    'ovos-lang-detector-plugin-fastlang=ovos_lang_detector_classics_plugin.neon_fastlang:FastLangDetector'
)

setup(
    name='ovos-lang-detector-classics-plugin',
    version='0.0.0a2',
    packages=['ovos_lang_detector_classics_plugin'],
    url='https://github.com/OpenVoiceOS/ovos-lang-detector-classics-plugin',
    license='apache-2',
    author='JarbasAI',
    include_package_data=True,
    install_requires=required("requirements.txt"),
    author_email='jarbasai@mailfence.com',
    description='average plugin classifications for language detection',
    entry_points={'neon.plugin.lang.detect': PLUGIN_ENTRY_POINT}
)
