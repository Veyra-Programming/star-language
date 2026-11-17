# 🚀 STAR MOBILE DEPLOYMENT, SIGNING & CI/CD PIPELINE SPECIFICATION
**Specification Version: 0.8.6**  
**Status: Authoritative Standard for Build, Signing, Verification & CI Release Automation**

---

## 1. Vision & Release Pipeline

Star 0.8.6 introduces an end-to-end, deterministic build, cryptographic signing, integrity verification, and deployment pipeline for Android and iOS mobile applications:

```text
                  ⭐ Star Source Code (.star)
                              │
                    AST → Star IR Compiler
                              │
                    📦 .starmobile Bundle
                              │
             ┌────────────────┴────────────────┐
             ↓                                 ↓
     Android Packaging                  iOS Packaging
   (APK + AAB Dual Build)             (Xcode + IPA Build)
             │                                 │
             ↓                                 ↓
     Android Signing                     Apple Signing
    (Debug / Release)                (Dev / Distribution)
             │                                 │
             └────────────────┬────────────────┘
                              ↓
                  Artifact Verification & SHA-256
                              ↓
                 Provenance (.build.json)
                              ↓
                  🚀 Distribution & CI/CD
```

---

## 2. Signing Architecture & Profiles

### 2.1 Android Signing Profiles
- **Debug / Development (`debug`)**: Automatically generates and uses `~/.star/android/debug.keystore` with standard development credentials.
- **Release / Distribution (`release`)**: Strictly requires explicit developer credentials declared in `star.toml` or via environment variables (`STAR_ANDROID_KEYSTORE`, `STAR_ANDROID_KEY_ALIAS`). Star **never** silently generates or replaces release keys.

```toml
[android.signing]

[android.signing.debug]
mode = "auto"

[android.signing.release]
keystore = "${STAR_ANDROID_KEYSTORE}"
alias = "${STAR_ANDROID_KEY_ALIAS}"
store_password = "${STAR_ANDROID_STORE_PASSWORD}"
key_password = "${STAR_ANDROID_KEY_PASSWORD}"
```

### 2.2 iOS Signing Profiles
- **Development (`development`)**: Uses local Apple developer identity and simulator profiles.
- **Distribution / App Store (`distribution`)**: Requires explicit Apple Team ID and Distribution Certificate from the developer's Apple Developer account.

```toml
[ios.signing]

[ios.signing.development]
team_id = "${APPLE_TEAM_ID}"
identity = "${APPLE_DEVELOPMENT_IDENTITY}"

[ios.signing.distribution]
team_id = "${APPLE_TEAM_ID}"
identity = "${APPLE_DISTRIBUTION_IDENTITY}"
profile = "${APPLE_PROVISIONING_PROFILE}"
```

---

## 3. Artifact Verification

The Star verification engine inspects containers, manifests, bytecodes, architectures, and cryptographic signatures:

```bash
# Verify Android APK
star verify apk build/android/Counter-debug.apk

# Verify Android App Bundle
star verify aab build/android/Counter-release.aab

# Verify iOS IPA
star verify ipa build/ios/Counter.ipa
```

---

## 4. CI/CD Workflow Generation

Generate reproducible, hardened CI/CD configurations for GitHub Actions and GitLab CI:

```bash
star ci init
```

Generates:
- `.github/workflows/star-mobile.yml`
- `.gitlab-ci.yml`

All secrets are mapped to environment variables (`${{ secrets.* }}`) and never hardcoded in repository files.

---

## 5. Unified Release Command

Execute the full compilation, conformance, signing, verification, and provenance pipeline in a single command:

```bash
star release mobile [entry.star] [--profile <debug|release>]
```

Standardized Output Structure:
```text
build/
├── mobile/
│   └── Counter.starmobile
├── android/
│   ├── Counter-debug.apk
│   ├── Counter-release.apk
│   ├── Counter.aab
│   ├── Counter.apk.sha256
│   ├── Counter.aab.sha256
│   └── Counter.build.json
└── ios/
    ├── project/
    ├── Counter.ipa
    ├── Counter.ipa.sha256
    └── Counter.build.json
```
