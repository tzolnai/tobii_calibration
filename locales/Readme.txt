To generate pot file:
python C:\Python35\Tools\i18n\pygettext.py -d all_strings -o ..\locales\all_strings.pot tobii_pro_wrapper.py

Generate *.mo files:
python C:\Python35\Tools\i18n\msgfmt.py -o all_strings.mo all_strings