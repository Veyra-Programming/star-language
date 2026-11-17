# 📜 STAR PROGRAMMING LANGUAGE SOFTWARE LICENSE AGREEMENT & EULA
**Effective Date: March 2026**  
**Applies To: Star 1.2.x Ecosystem, StarVM, Toolchain, Libraries, and Distribution Archives**

---

### IMPORTANT — READ CAREFULLY BEFORE INSTALLING OR USING THE SOFTWARE:

This Software License Agreement and End-User License Agreement ("Agreement") is a legal agreement between you (either an individual or a single entity, referred to as "You" or "Licensee") and the **Star Language Open Source Project & Contributors** ("Licensor"). 

By downloading, installing, compiling, executing, copying, or otherwise using the **Star Programming Language SDK**, its runtimes (**StarVM**), compilers (**starc**), tools, packages, or associated documentation (collectively, the "Software"), you agree to be bound by the terms of this Agreement.

If you do not agree to the terms of this Agreement, do not install, copy, or use the Software.

---

## 1. DUAL LICENSE MODEL & CORE RIGHTS

### 1.1 Open Source Core (MIT License)
The Star Programming Language source code, StarVM bytecode virtual machine, core libraries, and standard tools are licensed under the terms of the **MIT License** (as set forth in `LICENSE`). You have full freedom to inspect, modify, fork, distribute, and contribute to the open-source codebase.

### 1.2 Binary Distribution & Royalty-Free Commercial Deployment
You are granted an unconditional, perpetual, worldwide, non-exclusive, royalty-free license to:
* **Develop Applications**: Create commercial, enterprise, proprietary, or open-source software using the Star Programming Language for Web, Desktop (Windows, macOS, Linux), Android, and iOS.
* **Redistribute Compiled Binaries**: Embed, link, and ship compiled Star bytecode (`.starb`), standalone executables, APKs, AABs, and IPAs to your customers, app stores (Google Play, Apple App Store, Microsoft Store), or private servers without any payment, fees, or royalties owed to Licensor.
* **Ownership of Output**: All intellectual property rights, code, assets, and applications authored by You using Star remain 100% your exclusive property. Licensor claims zero ownership over applications built with Star.

---

## 2. WINDOWS & THIRD-PARTY TOOLCHAIN INTEGRATION

### 2.1 Microsoft Visual Studio & Windows SDK
* **Zero Dependency Default**: Star includes an in-tree, self-contained Windows desktop runtime engine that functions out-of-the-box without requiring Microsoft Visual Studio or the Windows SDK.
* **Optional Native Toolchain Use**: When You elect to use native MSVC compilation (`star build desktop --vs` or native C++ extensions), Star interfaces with your locally installed Microsoft Visual Studio (2017, 2019, 2022, or Visual Studio Build Tools). Your use of Microsoft Visual Studio and the Windows SDK is governed separately by Microsoft Corporation's applicable license terms and conditions.

### 2.2 Android SDK & Apple Toolchain Integration
* **Android SDK**: Full Android builds interface with the Android SDK (Google LLC) under Android Software Development Kit License Agreement terms.
* **iOS Inbuild System**: iOS builds utilize Star's built-in cross-platform Inbuild System & Star SDKs, requiring zero macOS hardware for standard IPA generation.

---

## 3. PACKAGE REGISTRY & ECOSYSTEM RULES

When using the Star Package Registry (`star search`, `star install`, `star publish`):
* **Security & Integrity**: You agree not to upload malicious code, spyware, backdoors, or software designed to compromise target systems.
* **Path Traversal Protection**: Star enforces strict Zip-Slip and path traversal barriers. Any attempt to exploit packaging tools is strictly prohibited.
* **Provenance**: Packages published to the ecosystem must accurately state their license and authorship.

---

## 4. TELEMETRY, PRIVACY & DATA COLLECTION

* **Zero Surveillance Guarantee**: Star does **NOT** collect involuntary telemetry, keystrokes, source code, or private developer data.
* **Local Diagnostics**: Commands such as `star doctor` execute purely locally on your machine and do not send machine telemetry to external servers without explicit user invocation.

---

## 5. DISCLAIMER OF WARRANTY

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS, CONTRIBUTORS, OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## 6. LIMITATION OF LIABILITY

UNDER NO CIRCUMSTANCES SHALL LICENSOR BE LIABLE FOR ANY INDIRECT, INCIDENTAL, CONSEQUENTIAL, SPECIAL, OR EXEMPLARY DAMAGES (INCLUDING LOSS OF PROFITS, DATA, OR BUSINESS INTERRUPTION) ARISING OUT OF THE USE OR INABILITY TO USE THE SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

---

## 7. TERMINATION & ACCEPTANCE

* **Acceptance**: Installation via `setup.cmd`, `install.ps1`, `star setup`, or `star license --accept` constitutes acceptance of these terms.
* **Termination**: This Agreement is effective until terminated. Your rights under this Agreement will terminate automatically without notice if you fail to comply with any of its material terms.

---
*Copyright © 2026 Star Language Open Source Project & Contributors. All rights reserved.*
