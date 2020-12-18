# Changelog

## [1.2.0](https://www.github.com/kjappelbaum/oximachinerunner/compare/v1.1.3...v1.2.0) (2020-12-18)


### Features

* only loading model when needed ([#44](https://www.github.com/kjappelbaum/oximachinerunner/issues/44)) ([dbbb89d](https://www.github.com/kjappelbaum/oximachinerunner/commit/dbbb89d54b3adf6ced553dc28ff03a322406d2bb))


### Miscellaneous

* bumping version of oximachine_featurizer ([80b0def](https://www.github.com/kjappelbaum/oximachinerunner/commit/80b0def70d29b7c205736ab622e8713172c55fa2))
* cleanup ([cbdee83](https://www.github.com/kjappelbaum/oximachinerunner/commit/cbdee83fb9ddb601475fc6a0dfc7bfbf039a6eef))
* cleanup model loading implementation and docstrings ([#47](https://www.github.com/kjappelbaum/oximachinerunner/issues/47)) ([a8723eb](https://www.github.com/kjappelbaum/oximachinerunner/commit/a8723ebfecaa59ea58f85aba47709aee9ac88a67))
* update example notebook ([0472238](https://www.github.com/kjappelbaum/oximachinerunner/commit/04722385b4d11e936018c86b04ce574937bc85ea))
* updating docs ([79ecf19](https://www.github.com/kjappelbaum/oximachinerunner/commit/79ecf19a3cbda8c8f7633dd9807d4199f774b10e))

### [1.1.3](https://www.github.com/kjappelbaum/oximachinerunner/compare/v1.1.2...v1.1.3) (2020-12-15)


### Miscellaneous

* allow to access the feature names ([e70a25a](https://www.github.com/kjappelbaum/oximachinerunner/commit/e70a25af40495b19fd39e62ebdd87eeeb794048b))
* allow to access the feature names ([5dabb21](https://www.github.com/kjappelbaum/oximachinerunner/commit/5dabb21ab659cd8a3d66caa0508da6e7820f43a4))
* extending tests, ignoring vscode ([92d53a3](https://www.github.com/kjappelbaum/oximachinerunner/commit/92d53a3cd8afa86ccaf6fbc9bb20046d2dd76367))

### [1.1.2](https://www.github.com/kjappelbaum/oximachinerunner/compare/v1.1.1...v1.1.2) (2020-12-15)


### Miscellaneous

* cleanup ([282c69c](https://www.github.com/kjappelbaum/oximachinerunner/commit/282c69cb25b24c7f6e7076efdd5ae6db4ddc1b67))

### [1.1.1](https://www.github.com/kjappelbaum/oximachinerunner/compare/v1.1.0...v1.1.1) (2020-12-15)


### Bug Fixes

* return the classes instead of indices, closes [#32](https://www.github.com/kjappelbaum/oximachinerunner/issues/32) ([879863f](https://www.github.com/kjappelbaum/oximachinerunner/commit/879863f51a832dd0f8ff3334573bdc0a8e1e73b5))


### Miscellaneous

* **deps:** use new oximachine_featurizer ([8307ac8](https://www.github.com/kjappelbaum/oximachinerunner/commit/8307ac82715b12c55169187bf9c6d9b88ebb1985))
* adding macos go github actions ([44c0110](https://www.github.com/kjappelbaum/oximachinerunner/commit/44c0110b43ef7a701c86a7b1ccd1f83b0dfc2efa))
* fix typo in gh actions ([db8762f](https://www.github.com/kjappelbaum/oximachinerunner/commit/db8762fd275dc2e537b3ebb6fe2ab56ac1b2ae94))
* removed widget ([2b2727e](https://www.github.com/kjappelbaum/oximachinerunner/commit/2b2727e6cb832afdcec1e05b921a83ad9a4cc172))

## [1.1.0](https://www.github.com/kjappelbaum/oximachinerunner/compare/v1.0.2...v1.1.0) (2020-12-15)


### Features

* returning more information ([379620b](https://www.github.com/kjappelbaum/oximachinerunner/commit/379620b9506340d8e14a2f837bd8e2f4eecc8d9e)), closes [#10](https://www.github.com/kjappelbaum/oximachinerunner/issues/10)


### Miscellaneous

* add md5 of model to repr ([5c6eecc](https://www.github.com/kjappelbaum/oximachinerunner/commit/5c6eecce7c76302e0ed195a7c4daf9bcacab5426))
* added 3.8 to test matrix ([8469b60](https://www.github.com/kjappelbaum/oximachinerunner/commit/8469b60dccc8237e87cfdb4ef48e42182884f0a5))
* added more tests, closes [#17](https://www.github.com/kjappelbaum/oximachinerunner/issues/17) ([45ab231](https://www.github.com/kjappelbaum/oximachinerunner/commit/45ab23165bb816e842f31a1166f60e15246fa510))
* added py3.9 test and docs ([7faaf03](https://www.github.com/kjappelbaum/oximachinerunner/commit/7faaf0346df3899a5fffd51069b274b91e130774))
* added test for MOF model ([0961c76](https://www.github.com/kjappelbaum/oximachinerunner/commit/0961c76f9b75632cc1082b968f5c1ef77a66aa78))
* adding repr ([c559933](https://www.github.com/kjappelbaum/oximachinerunner/commit/c5599336967f91bf0e3e7647e877338debf05e8f))
* bump feautrizer version ([b8094d8](https://www.github.com/kjappelbaum/oximachinerunner/commit/b8094d80c33646f07c11186f7e694ba7a3507d74))
* dirty fix: downgrading numpy for docs ([f440385](https://www.github.com/kjappelbaum/oximachinerunner/commit/f440385caad953b09853e71940b4d6915decb52f))
* do not install everything on rtd ([5b780de](https://www.github.com/kjappelbaum/oximachinerunner/commit/5b780deaa8446fdc4cb21d028cc75117ace5c9b2))
* dropping py3.9 support due to numba ([5c60148](https://www.github.com/kjappelbaum/oximachinerunner/commit/5c60148639431a107753a93a3440a3d601009d4a))
* fix gh actions ([3c9daea](https://www.github.com/kjappelbaum/oximachinerunner/commit/3c9daea6e8362000f615907766524da3c51ab6b3))
* github actions for python 3.6 ([d5f67e1](https://www.github.com/kjappelbaum/oximachinerunner/commit/d5f67e12b224bd7d370727ff441482c1851a6d9e))
* need to add path before i import ([1097378](https://www.github.com/kjappelbaum/oximachinerunner/commit/1097378339cec00fc8dba95826c7751260cf692d))
* pinning dependencies ([07bb672](https://www.github.com/kjappelbaum/oximachinerunner/commit/07bb672e66dfc498e95ccf224baa8b94bb212e44))
* pinning dependencies ([7b14c4b](https://www.github.com/kjappelbaum/oximachinerunner/commit/7b14c4bac0d6af39f7be780d42434131c1f83b2e))
* pinning dependencies ([63c5d79](https://www.github.com/kjappelbaum/oximachinerunner/commit/63c5d79101c84f831fa798363c249caa7dd6805e))
* pre-commit ([89529b0](https://www.github.com/kjappelbaum/oximachinerunner/commit/89529b0629d70fd9c9d20b0b397206155298f199))
* remove ipynb checkpoint dir ([cc17e69](https://www.github.com/kjappelbaum/oximachinerunner/commit/cc17e692650c8d80eb3e712401ed0c4e3bb07951))
* setting up dependabot ([a47e8cc](https://www.github.com/kjappelbaum/oximachinerunner/commit/a47e8cc4b2acb6ccf4abb6109275fd005535a4f6))
* started docs and refactoring dev tools ([a5c6d8b](https://www.github.com/kjappelbaum/oximachinerunner/commit/a5c6d8b5f4e1e9688307fab315769bd2bafadc99)), closes [#11](https://www.github.com/kjappelbaum/oximachinerunner/issues/11)
* trying to pinpoint the issue with the docs ([396d1cf](https://www.github.com/kjappelbaum/oximachinerunner/commit/396d1cf68cd4d736fb620e96e913997e8cc1ed76))
* trying to pinpoint the issue with the docs ([7fc0382](https://www.github.com/kjappelbaum/oximachinerunner/commit/7fc0382cc9bd9134bfedf153a41535dd8885ff81))
* trying to pinpoint the issue with the docs ([d8309ec](https://www.github.com/kjappelbaum/oximachinerunner/commit/d8309ec25991d2c974e1ab836700de3f63fcf924))
* trying to test code in py3.7 ([965709d](https://www.github.com/kjappelbaum/oximachinerunner/commit/965709d582492c5db09ec1f9f7bba82b429e6abe))
* trying to use conda for readthedocs ([2f65eb7](https://www.github.com/kjappelbaum/oximachinerunner/commit/2f65eb747ea6446147d0fdc9bb245873ef9c4b0f))
* trying to use conda for readthedocs ([21124cd](https://www.github.com/kjappelbaum/oximachinerunner/commit/21124cdfcae8130941269f6ace0dadad5a512d07))
* trying to use conda for readthedocs ([a462b86](https://www.github.com/kjappelbaum/oximachinerunner/commit/a462b861e59ec11f0bc7bad1a1085d304752cd19))
* update pylint settings ([df83d8b](https://www.github.com/kjappelbaum/oximachinerunner/commit/df83d8b8c695af5fd8baf5acb8fb93d3ebbc051d))
* updating docs requirements ([da6ee2f](https://www.github.com/kjappelbaum/oximachinerunner/commit/da6ee2fcb723d658f1e564dc2467f709a77bc3b3))
* updating the actions and docs ([921915f](https://www.github.com/kjappelbaum/oximachinerunner/commit/921915f697ea59a14a24e6be714e95d1b61145c6))
* using the featurization method from the oximachine_featurizer package ([659fd67](https://www.github.com/kjappelbaum/oximachinerunner/commit/659fd67c4b2ce4ed7318b762c779ec7d96928ce5))
* **deps:** bump xgboost from 1.2.0 to 1.2.1 ([1dd9301](https://www.github.com/kjappelbaum/oximachinerunner/commit/1dd9301f96da85ba6210cbcfa6f03a6a5dfc2911))
* **deps:** update traitlets requirement from ~=4.3.3 to ~=5.0.5 ([cc7095c](https://www.github.com/kjappelbaum/oximachinerunner/commit/cc7095cd286d2faedefb661d8d4b10ed7db9bb82))
* **deps:** update xgboost requirement from ~=1.2.0 to ~=1.3.0 ([0f6f58b](https://www.github.com/kjappelbaum/oximachinerunner/commit/0f6f58b4e16ccfdb6792e5a7314f8b9ac3c705f0))
* updating the actions and docs ([18d8a20](https://www.github.com/kjappelbaum/oximachinerunner/commit/18d8a20de2c26ae95b0370f1b88571ce9a890229))

## v1.0.2 (2020-09-01)

### Changes

-   Chore: changelog. \[Kevin\]
-   Chore: updated readme. \[Kevin\]
-   Chore: updated changelog. \[Kevin\]
-   Chore: updated example for new API. \[Kevin\]
-   Chore: updating manifest. \[Kevin\]

## v1.0.0 (2020-09-01)

### New

-   Feat: complete refactoring into OO API. \[Kevin\]
-   Feat: complete refactoring into OO API. \[Kevin\]

### Changes

-   Chore: preparing release. \[Kevin\]
-   Chore: dirty commit for checkout. \[Kevin\]
-   Chore: preparing merge with master and new release. \[Kevin\]
-   Chore: updating docstrings. \[Kevin\]
-   Chore: tests migrated to new API. \[Kevin\]
-   Chore: deleting files. \[Kevin\]
-   Chore: preparing for all CSD model. \[Kevin\]
-   Chore: preparing for all CSD model. \[Kevin\]

### Other

-   Merge branch \'master\' into multiple_models. \[Kevin\]
    -   preparing release of the new API

## v0.2.6 (2020-08-26)

### Changes

-   Chore: bumping featurizer dependency. \[Kevin\]

## v0.2.5 (2020-08-26)

### Changes

-   Chore: being more specific in MANIFEST. \[Kevin\]

## v0.2.4 (2020-08-26)

### Changes

-   Chore: preparing release. \[Kevin\]
-   Chore: adding requirements to MANIFEST for pypi. \[Kevin\]
-   Chore: adding requirements to MANIFEST for pypi. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]

## v0.2.3 (2020-08-26)

### Changes

-   Chore: removing large files for pypi release. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]
-   Chore: removing large files for pypi release. \[Kevin\]

## v0.2.2 (2020-08-26)

### New

-   Feat: adding option for model trained on all CSD, updating examples
    and pinning dependencies. \[Kevin\]
-   Feat: adding option for model trained on all CSD, updating examples
    and pinning dependencies. \[Kevin\]
-   Feat: adding option for model trained on all CSD, updating examples
    and pinning dependencies. \[Kevin\]

### Changes

-   Chore: preparing next release. \[Kevin\]
-   Chore: preparing next release. \[Kevin\]
-   Chore: updating example. \[Kevin\]
-   Chore: updated changelog. \[Kevin\]
-   Chore: moving example notebook. \[Kevin\]
-   Chore: updated readme. \[Kevin\]
-   Chore: updated changelog. \[Kevin\]
-   Chore: updated changelog. \[Kevin\]
-   Chore: updated dependencies. \[Kevin\]

## v0.2.1 (2020-07-31)

### New

-   Feat: added widget. \[Kevin\]
-   Feat: implementing featurizer class directly in this package.
    \[Kevin\]

### Changes

-   Chore: updated changelog. \[Kevin\]

-   Chore: updated changelog. \[Kevin\]

-   Chore: updated dependencies. \[Kevin\]

-   Chore: trying to fix installation issue. \[Kevin\]

-   Chore: trying to fix installation issue. \[Kevin\]

-   Chore: updating pre-commit hooks. \[Kevin\]

-   Chore(deps): bump sympy from 1.5.1 to 1.6.
    \[dependabot-preview\[bot\]\]

    Bumps \[sympy\](<https://github.com/sympy/sympy>) from 1.5.1 to 1.6.

    -   \[Release notes\](<https://github.com/sympy/sympy/releases>)
    -   \[Commits\](<https://github.com/sympy/sympy/compare/sympy-1.5.1>\...sympy-1.6)

-   Chore(deps): update pandas requirement from \<1,\>=0.22
    to \>=0.22,\<2. \[dependabot-preview\[bot\]\]

    Updates the requirements on
    \[pandas\](<https://github.com/pandas-dev/pandas>) to permit the
    latest version.

    -   \[Release
        notes\](<https://github.com/pandas-dev/pandas/releases>)
    -   \[Changelog\](<https://github.com/pandas-dev/pandas/blob/master/RELEASE.md>)
    -   \[Commits\](<https://github.com/pandas-dev/pandas/compare/v0.22.0>\...v1.0.5)

-   Chore: linting. \[Kevin\]

-   Chore: updating manifest for publication. \[Kevin\]

-   Chore: linting. \[Kevin\]

-   Chore: linting. \[Kevin\]

-   Chore: updatin python version. \[Kevin\]

-   Chore: updating pre-commit hooks. \[Kevin\]

-   Chore: updating badge. \[Kevin\]

-   Chore: reran notebook, remove py3.5 from CI. \[Kevin\]

-   Chore: trying to drop two more dependencies. \[Kevin\]

-   Chore: trigger CI. \[Kevin\]

### Fix

-   Imports now cleaner, there is still an ERROR message in
    installation, but this is just due to pinned version in matminer.
    \[Kevin\]
-   Missing six dependency. \[Kevin\]

### Other

-   Merge pull request \#2 from kjappelbaum/dependabot/pip/sympy-1.6.
    \[Kevin Jablonka\]

    chore(deps): bump sympy from 1.5.1 to 1.6

-   Merge pull request \#1 from
    kjappelbaum/dependabot/pip/pandas-gte-0.22-and-lt-2. \[Kevin
    Jablonka\]

    chore(deps): update pandas requirement from \<1,\>=0.22
    to \>=0.22,\<2

-   Create python-package.yml. \[Kevin Jablonka\]

## v0.2-alpha (2020-06-23)

### New

-   Feat: added widget. \[Kevin\]

## v0.1-alpha (2020-06-23)

### Changes

-   Chore: trying to fix installation issue. \[Kevin\]

-   Chore: trying to fix installation issue. \[Kevin\]

-   Chore: updating pre-commit hooks. \[Kevin\]

-   Chore(deps): bump sympy from 1.5.1 to 1.6.
    \[dependabot-preview\[bot\]\]

    Bumps \[sympy\](<https://github.com/sympy/sympy>) from 1.5.1 to 1.6.

    -   \[Release notes\](<https://github.com/sympy/sympy/releases>)
    -   \[Commits\](<https://github.com/sympy/sympy/compare/sympy-1.5.1>\...sympy-1.6)

-   Chore(deps): update pandas requirement from \<1,\>=0.22
    to \>=0.22,\<2. \[dependabot-preview\[bot\]\]

    Updates the requirements on
    \[pandas\](<https://github.com/pandas-dev/pandas>) to permit the
    latest version.

    -   \[Release
        notes\](<https://github.com/pandas-dev/pandas/releases>)
    -   \[Changelog\](<https://github.com/pandas-dev/pandas/blob/master/RELEASE.md>)
    -   \[Commits\](<https://github.com/pandas-dev/pandas/compare/v0.22.0>\...v1.0.5)

-   Chore: linting. \[Kevin\]

-   Chore: updating manifest for publication. \[Kevin\]

-   Chore: linting. \[Kevin\]

-   Chore: linting. \[Kevin\]

### Other

-   Merge pull request \#2 from kjappelbaum/dependabot/pip/sympy-1.6.
    \[Kevin Jablonka\]

    chore(deps): bump sympy from 1.5.1 to 1.6

-   Merge pull request \#1 from
    kjappelbaum/dependabot/pip/pandas-gte-0.22-and-lt-2. \[Kevin
    Jablonka\]

    chore(deps): update pandas requirement from \<1,\>=0.22
    to \>=0.22,\<2

## v0.0.1 (2020-05-23)

### New

-   Feat: implementing featurizer class directly in this package.
    \[Kevin\]
-   Feat: examples in jupyter notebook work. \[Kevin\]
-   Feat: moving most dependencies directly in this repo. \[Kevin\]
-   Feat: adding boilerplate - copied form the oximachine app for
    materialscloud - could be used in the future as example of how to
    deploy oximachine (which is great!) - still need to fix the
    dependencies. \[Kevin\]

### Changes

-   Chore: updatin python version. \[Kevin\]
-   Chore: updating pre-commit hooks. \[Kevin\]
-   Chore: updating badge. \[Kevin\]
-   Chore: reran notebook, remove py3.5 from CI. \[Kevin\]
-   Chore: trying to drop two more dependencies. \[Kevin\]
-   Chore: trigger CI. \[Kevin\]
-   Chore: trigger CI. \[Kevin\]
-   Chore: fixing ci yml file. \[Kevin\]
-   Chore: finished linting, added versioneer. \[Kevin\]
-   Chore: first linting. \[Kevin\]
-   Chore: first linting. \[Kevin\]

### Fix

-   Imports now cleaner, there is still an ERROR message in
    installation, but this is just due to pinned version in matminer.
    \[Kevin\]
-   Missing six dependency. \[Kevin\]
-   Make subpackage with learnmofox due to the joblib file
    compatability. \[Kevin\]
-   Dependencies cleaned and pinned. \[Kevin\]

### Other

-   Create python-package.yml. \[Kevin Jablonka\]
-   Break: learnmofox as subpackage, import works now. \[Kevin\]
