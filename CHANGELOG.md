# Changelog

All notable changes to this project will be documented in this file.

## [0.4.1-dev0] - 2024-10-17

### Fixed

- Workaround for staticfiles by @kod-kristoff
- Ignore S603 for now by @kod-kristoff

### Miscellaneous Tasks

- *(dev-deps)* Add bump-my-version by @kod-kristoff
- *(scheduled)* Remove nighlty job by @kod-kristoff
- Bump ruff in precommit-config by @kod-kristoff
- *(dev-deps)* Add uvicorn and watchfiles by @kod-kristoff
- Add traefik settings by @kod-kristoff
- Remove old file by @kod-kristoff
- Disable doctests by @kod-kristoff
- Use uv instead of pdm by @kod-kristoff
- Adapt workflows by @kod-kristoff
- Adapt Makefile by @kod-kristoff
- Also test for python 3.14-dev by @kod-kristoff
- Also test for python 3.13 by @kod-kristoff
- Set python 3.9 as minimum version by @kod-kristoff
- Do not use hashes from workflow file by @kod-kristoff
- Bump uv to 0.4.18 by @kod-kristoff
- *(test)* Fix python-version by @kod-kristoff
- Remove unused actions by @kod-kristoff
- Use env namespace by @kod-kristoff
- Add uv based workflows by @kod-kristoff
- Add uv based Makefile by @kod-kristoff
- Remove pdm based workflows by @kod-kristoff
- Remove pdm Makefile by @kod-kristoff
- Ignore some files by @kod-kristoff

### Testing

- Remove duplicate fixture by @kod-kristoff

## [0.4.0] - 2024-06-14

### Added

- Port para/xml route by @kod-kristoff
- Port para/html route by @kod-kristoff

### Fixed

- Render secoondary descriptors correct by @kod-kristoff
- Render <sup> by @kod-kristoff
- Return 404 on missing lids by @kod-kristoff
- Add gap in UI by @kod-kristoff

## [0.4.0-rc0] - 2024-06-13

### Changed

- Return None on non-existing by @kod-kristoff

### Fixed

- Remove redundant info by @kod-kristoff
- Handle response errors by @kod-kristoff

### Miscellaneous Tasks

- Use hashes from pdm.lock also by @kod-kristoff
- *(check)* Fix typo by @kod-kristoff
- Generate test lock file w/o hashes by @kod-kristoff
- *(make)* Add project line by @kod-kristoff
- Mark CHANGELOG.md as phony by @kod-kristoff
- *(make)* Add lock target by @kod-kristoff
- *(make)* Dont use backticks by @kod-kristoff
- Add snapshot-update target by @kod-kristoff
- Add changelog update by @kod-kristoff
- Update ruff config by @kod-kristoff
- Remove unused issue templates by @kod-kristoff
- Update issue_templates by @kod-kristoff
- Rename issue templates by @kod-kristoff

## [0.4.0-dev0] - 2024-04-19

### Added

- Make the image link to fl/html by @kod-kristoff
- Port para json api by @kod-kristoff

### Fixed

- Use relevant titles for gen route by @kod-kristoff
- Use relevant titles for ff route by @kod-kristoff
- Use relevant title for fl route by @kod-kristoff
- Add relevant title for lid html by @kod-kristoff
- Add center for lexemes by @kod-kristoff

### Miscellaneous Tasks

- *(release)* Prepare release by @kod-kristoff

## [0.3.1-dev2] - 2024-04-17

### Changed

- Move version info to shared/version_info by @kod-kristoff

### Fixed

- Add config validation by @kod-kristoff
- Adjust openapi_url by @kod-kristoff

### Miscellaneous Tasks

- Use pdm sync instead of pdm install by @kod-kristoff

## [0.3.1-dev0] - 2024-03-28

### Fixed

- Add date to version api by @kod-kristoff

### Miscellaneous Tasks

- Fix by @kod-kristoff
- Add git-cliff config by @kod-kristoff

## [0.3.0-dev211] - 2024-03-27

### Miscellaneous Tasks

- Bump to 0.3.0-dev211 by @kod-kristoff
- Bump by @kod-kristoff

## [0.3.0-dev210] - 2024-03-27

### Miscellaneous Tasks

- Update bump-my-version config by @kod-kristoff

## [0.3.0-dev209] - 2024-03-27

### Added

- Return 404 if gen/json is missing by @kod-kristoff
- Return 404 if lid/json is missing by @kod-kristoff
- Return 404 if fl/json is missing by @kod-kristoff
- Add rnd lookup of lexeme by @kod-kristoff
- Port lid-protojs by @kod-kristoff
- Port fl-html by @kod-kristoff
- Port gen json api by @kod-kristoff
- Add get_inflection_table_query to deps by @kod-kristoff
- Add gen-json-api by @kod-kristoff
- Add FmRunnerInflectionTable by @kod-kristoff
- Configure telemetry by @kod-kristoff
- Add minimal and doctests jobs by @kod-kristoff
- Port compound json by @kod-kristoff
- Make morph a separate server by @kod-kristoff
- Track call time to service by @kod-kristoff
- Add root_path to settings by @kod-kristoff

### Changed

- Don't depend on javascript by @kod-kristoff
- Add tracing to all routes by @kod-kristoff
- Port sms xml api by @kod-kristoff
- Port sms-html by @kod-kristoff
- Port sms json api by @kod-kristoff
- Simplify inits by @kod-kristoff
- Move inits by @kod-kristoff
- Port version api by @kod-kristoff
- Clean code by @kod-kristoff
- Port rnd lookup of lexeme by @kod-kristoff
- Port wordforms by @kod-kristoff
- Port lid-graph route by @kod-kristoff
- Remove old code lemma by @kod-kristoff
- Use segment as query parameter by @kod-kristoff
- Port gen xml api by @kod-kristoff
- Port gen-html by @kod-kristoff
- Rename GenerateInflectionTable by @kod-kristoff
- Make prints to log calls by @kod-kristoff
- Simplify expression by @kod-kristoff
- Rename webapp to saldo_ws by @kod-kristoff
- Rename main to server by @kod-kristoff
- Small fixes by @kod-kristoff
- Use new telemetry module by @kod-kristoff
- Make telemetry a separate module by @kod-kristoff
- Rename to check-check by @kod-kristoff
- Stuff by @kod-kristoff
- Remove unused import by @kod-kristoff
- Log settings by @kod-kristoff
- Add logging by @kod-kristoff
- Use rfind by @kod-kristoff
- Make all interfaces async by @kod-kristoff
- Remove unused code by @kod-kristoff

### Documentation

- Add load_morphology example by @kod-kristoff
- Add response_model for fl-json by @kod-kristoff
- Add info about publish by @kod-kristoff
- Add reason by @kod-kristoff

### Fixed

- Add type annotation by @kod-kristoff
- Use fragment as query for fullform by @kod-kristoff
- Add missing templates by @kod-kristoff
- Temporarily disable sms routes by @kod-kristoff
- Use functools.cmp_to_key by @kod-kristoff
- Correctly draw random key by @kod-kristoff
- Make korp link correct by @kod-kristoff
- Adjust return type by @kod-kristoff
- Make korpus_ref work by @kod-kristoff
- Separate paradigm,word and data by @kod-kristoff
- Make fm_runner handle empty output by @kod-kristoff
- Fix type errors by @kod-kristoff
- Fix some lints by @kod-kristoff
- Add note that compound analysis doesn't work by @kod-kristoff
- Sort dict based on key by @kod-kristoff
- Nested prefixes with '__' by @kod-kristoff
- Add missing call by @kod-kristoff
- Update TemplateResposne by @kod-kristoff
- Use saldo_ws.config.Settings by @kod-kristoff
- Adjust telemetry by @kod-kristoff
- Adjust json_arrays imports by @kod-kristoff
- Make code more mergeable by @kod-kristoff
- Adjust names by @kod-kristoff
- Use correct openapi_url by @kod-kristoff
- Mk test pass by @kod-kristoff
- Base_url by @kod-kristoff
- Add base_url by @kod-kristoff
- Links by @kod-kristoff
- Links by @kod-kristoff
- Make fullform and fullform_lex more stable by @kod-kristoff
- Layout by @kod-kristoff
- Adjust base tempalte by @kod-kristoff
- *(html)* Add new form by @kod-kristoff
- Handle not list by @kod-kristoff
- Silence lints by @kod-kristoff
- Lid stuff by @kod-kristoff
- Lids by @kod-kristoff
- Ignore tracking html from backend by @kod-kristoff
- Add telemery attribute by @kod-kristoff
- Add saldo.css as static file by @kod-kristoff
- Use strings by @kod-kristoff
- Add matomo frontend tracking by @kod-kristoff

### Miscellaneous Tasks

- Swithc to bump-my-version by @kod-kristoff
- *(scheduled)* Remove nightly action by @kod-kristoff
- *(check)* Fix typo by @kod-kristoff
- Remove unused action by @kod-kristoff
- Add pre-commit config by @kod-kristoff
- Fix bump-my-version command by @kod-kristoff
- Switch to bump-my-version by @kod-kristoff
- Don't run test workflows on tags by @kod-kristoff
- Remove doctests by @kod-kristoff
- Set MINIMUM_PYTHON_VERSION to 3.10 by @kod-kristoff
- Remove release and ci workflow by @kod-kristoff
- Fix typo by @kod-kristoff
- Change new on release workflow by @kod-kristoff
- Also checkout submodules as default by @kod-kristoff
- Set 3.8 as minimum_python_version by @kod-kristoff
- Split test in release and test by @kod-kristoff
- Also run test on tags v by @kod-kristoff
- Use right lockfile by @kod-kristoff
- Remove check-for-updates by @kod-kristoff
- *(scheduled)* Bump update-deps-action by @kod-kristoff
- *(test)* Add cov_report=xml by @kod-kristoff
- *(test)* Move codecov upload by @kod-kristoff
- Add check-for-updates by @kod-kristoff
- *(scheduled)* Install pdm separate by @kod-kristoff
- Add concurreny to test by @kod-kristoff
- Fix typo by @kod-kristoff
- Fix so that nightly uses 3.13-dev by @kod-kristoff
- Remove unused token by @kod-kristoff
- Use token correct by @kod-kristoff
- Use token by @kod-kristoff
- Also test python 3.12 by @kod-kristoff
- Check github-actions by @kod-kristoff
- Strengthen permissions by @kod-kristoff
- Add permissions monitoring by @kod-kristoff
- Allow for codecov to fail by @kod-kristoff
- Add ruff to ci group by @kod-kristoff
- Add github actions workflow by @kod-kristoff
- Add ruff config by @kod-kristoff
- Bump deps by @kod-kristoff

### Testing

- Use snapshots for lid-api by @kod-kristoff
- Use snapshot tests for gen-api by @kod-kristoff
- Use snapshots for fullform-lex by @kod-kristoff
- Rewrte test to use segment instead of q by @kod-kristoff
- Silent mypy on tests by @kod-kristoff
- Move  adapters to tests by @kod-kristoff
- Make tests a package by @kod-kristoff
- Add schema tests by @kod-kristoff
- Adjust saldo_ws_Server fixture by @kod-kristoff
- Adjust saldo_ws_Server fixture by @kod-kristoff
- Rename lock file by @kod-kristoff
- Add deptracpy by @kod-kristoff
- Disable test_fm_runner in Github Actions by @kod-kristoff

### New Contributors
* @dependabot[bot] made their first contribution
## [0.2.3] - 2023-05-10

### Fixed

- Put redoc in root by @kod-kristoff

## [0.2.2] - 2023-05-10

### Fixed

- Use deault redoc url by @kod-kristoff

## [0.2.1] - 2023-05-10

### Fixed

- Put opentelemetry as first called middleware by @kod-kristoff

## [0.1.1] - 2023-05-10

### Added

- Add opentelemetry by @kod-kristoff
- Add lookup-lid query by @kod-kristoff
- Add fullform_lex_query interface by @kod-kristoff

### Changed

- Move prlex to formatting by @kod-kristoff
- Lexeme xmlize and htmlize to templates by @kod-kristoff
- Lemma xmlize and htmlize to templates by @kod-kristoff
- Move predicates by @kod-kristoff
- Move xmlize to xml-template by @kod-kristoff
- Port to python3 by @kod-kristoff

### Documentation

- Fix typo by @kod-kristoff

### Fixed

- Add version to service by @kod-kristoff
- Update telemetry by @kod-kristoff
- Add explicit call to startup tasks by @kod-kristoff
- Rm startup handler by @kod-kristoff
- Set log level to INFO by @kod-kristoff
- Use lifespan by @kod-kristoff
- Add event_handler earlier by @kod-kristoff
- Fullform-lex api by @kod-kristoff
- Use fullform_lex_query in webapp by @kod-kristoff

### Other

- Add logs by @kod-kristoff

[0.4.1-dev0]: https://github.com/spraakbanken/sblex-server/compare/v0.4.0..v0.4.1-dev0
[0.4.0]: https://github.com/spraakbanken/sblex-server/compare/v0.4.0-rc0..v0.4.0
[0.4.0-rc0]: https://github.com/spraakbanken/sblex-server/compare/v0.4.0-dev0..v0.4.0-rc0
[0.4.0-dev0]: https://github.com/spraakbanken/sblex-server/compare/v0.3.1-dev2..v0.4.0-dev0
[0.3.1-dev2]: https://github.com/spraakbanken/sblex-server/compare/v0.3.1-dev1..v0.3.1-dev2
[0.3.1-dev0]: https://github.com/spraakbanken/sblex-server/compare/v0.3.0-dev211..v0.3.1-dev0
[0.3.0-dev211]: https://github.com/spraakbanken/sblex-server/compare/v0.3.0-dev210..v0.3.0-dev211
[0.3.0-dev210]: https://github.com/spraakbanken/sblex-server/compare/v0.3.0-dev209..v0.3.0-dev210
[0.3.0-dev209]: https://github.com/spraakbanken/sblex-server/compare/v0.2.3..v0.3.0-dev209
[0.2.3]: https://github.com/spraakbanken/sblex-server/compare/v0.2.2..v0.2.3
[0.2.2]: https://github.com/spraakbanken/sblex-server/compare/v0.2.1..v0.2.2
[0.2.1]: https://github.com/spraakbanken/sblex-server/compare/v0.2.0..v0.2.1

<!-- generated by git-cliff -->
