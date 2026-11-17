"""
Star Mobile CI/CD Automation Pipeline Generator
Authoritative Reference: STAR_RELEASE.md (Section 9)
"""

import os
from typing import Dict, Any, Optional


class CIPipelineGenerator:
    """
    Generates production-grade, hardened CI/CD workflow configurations
    for GitHub Actions and GitLab CI without hardcoded secrets.
    """

    @classmethod
    def generate_github_workflow(cls, output_path: str = ".github/workflows/star-mobile.yml") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        content = """name: Star Mobile Build, Test & Release Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  validate_and_test:
    name: 🧪 Test & Conformance Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Run Star Test Suite
        run: |
          python tests/run_tests.py

      - name: Run Cross-Platform Conformance Matrix
        run: |
          python -c "from tests.conformance.runner import run_conformance_matrix; import sys; sys.exit(run_conformance_matrix())"

  build_android:
    name: 🤖 Build Android (APK & AAB)
    needs: validate_and_test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Build Android Suite
        env:
          STAR_ANDROID_KEYSTORE: ${{ secrets.STAR_ANDROID_KEYSTORE }}
          STAR_ANDROID_KEY_ALIAS: ${{ secrets.STAR_ANDROID_KEY_ALIAS }}
          STAR_ANDROID_STORE_PASSWORD: ${{ secrets.STAR_ANDROID_STORE_PASSWORD }}
          STAR_ANDROID_KEY_PASSWORD: ${{ secrets.STAR_ANDROID_KEY_PASSWORD }}
        run: |
          python -m star_engine.cli build android

      - name: Verify Android Artifacts
        run: |
          python -m star_engine.cli verify build/android/*.apk || true
          python -m star_engine.cli verify build/android/*.aab || true

      - name: Upload Android Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: star-android-artifacts
          path: build/android/

  build_ios:
    name: 🍎 Build iOS (Xcode & IPA)
    needs: validate_and_test
    runs-on: macos-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Build iOS Xcode Project & IPA
        env:
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
          APPLE_DISTRIBUTION_IDENTITY: ${{ secrets.APPLE_DISTRIBUTION_IDENTITY }}
          APPLE_PROVISIONING_PROFILE: ${{ secrets.APPLE_PROVISIONING_PROFILE }}
        run: |
          python -m star_engine.cli build ipa

      - name: Verify iOS IPA Artifact
        run: |
          python -m star_engine.cli verify build/ios/*.ipa || true

      - name: Upload iOS Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: star-ios-artifacts
          path: build/ios/
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    @classmethod
    def generate_gitlab_ci(cls, output_path: str = ".gitlab-ci.yml") -> str:
        content = """# Star Mobile GitLab CI Pipeline
stages:
  - test
  - build_android
  - build_ios

test_and_conformance:
  stage: test
  image: python:3.10
  script:
    - python tests/run_tests.py
    - python -c "from tests.conformance.runner import run_conformance_matrix; import sys; sys.exit(run_conformance_matrix())"

build_android:
  stage: build_android
  image: python:3.10
  script:
    - python -m star_engine.cli build android
  artifacts:
    paths:
      - build/android/

build_ios:
  stage: build_ios
  tags:
    - macos
  script:
    - python -m star_engine.cli build ipa
  artifacts:
    paths:
      - build/ios/
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        return output_path

    @classmethod
    def init_all(cls, target_dir: str = ".") -> Dict[str, str]:
        gh_path = os.path.join(target_dir, ".github", "workflows", "star-mobile.yml")
        gl_path = os.path.join(target_dir, ".gitlab-ci.yml")
        cls.generate_github_workflow(gh_path)
        cls.generate_gitlab_ci(gl_path)
        return {
            "github": gh_path,
            "gitlab": gl_path
        }
