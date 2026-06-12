# FileRenamer - Safe Batch File Renamer (with Preview) / 安全批量文件名替换工具 🚀

[English](#english) | [中文](#中文)

---

## English

A lightweight, secure, and zero-dependency local GUI utility powered by Python Tkinter. It features a **"Search-Preview-Execute"** workflow with a bilingual interface to prevent accidental file modifications.

### ✨ Key Features

- **Dynamic Sync & Fix**: Fully fixed the live-updating placeholder bug. The preview list and memory buffer dynamically calibrate to your "Replace With" entry in real-time, even if inputs are modified mid-session.
- **Accidental Deletion Prevention**: View exactly what your new filenames will look like in the Treeview box before committing to any changes.
- **Bilingual Interface**: Seamlessly toggle between English and Chinese with a single click.
- **Flexible Rules (With Clear Mode)**: Replace target characters with new ones, or leave the "Replace With" field blank to completely erase the target characters.
- **Selection Control**: Features a simulated checkbox [ X ] system. Supports standalone row toggles via Double-Click, as well as global "Select All" and "Deselect All" operations.
- **Directory Protection**: Only modifies pure files within the selected directory; skips subfolders automatically to prevent catastrophic path drift.

### 🛠️ Environment Prerequisites

- **Python 3.8+** (Recommended for running from source)
- **Dependencies**: None. Built completely using Python Standard Libraries (tkinter, os).

### 📥 Download Pre-built Release (No Python Required)

If you don't want to run the script via terminal or install Python, you can directly download the fully self-contained executable file:

1. Navigate to the [Releases](https://github.com/your_username/FileRenamer/releases) page of this repository.
2. Download the latest version matching your operating system:
   - **Windows**: `FileRenamer.exe`
3. Double-click the downloaded `FileRenamer.exe` to launch the application instantly. All necessary dependencies and the core runtime are pre-packaged inside.

---

### 🚀 Quick Start (Running from Source)

1. Clone this repository:
   git clone https://github.com/your_username/FileRenamer.git
   cd FileRenamer

2. Run the application:
   python main.py

*(Optional) To bundle your own standalone release build using PyInstaller:*
   pip install pyinstaller
   pyinstaller --clean -F -w --name="FileRenamer" main.py

---

### 📖 Step-by-Step Guide

1. **Path Selection**: Click "Browse..." to select your target folder.
2. **Define Search Criteria**: Type the substring you want to get rid of into the "Find Target" box.
3. **Set Replacement String**: 
   - Type your new desired string in "Replace With". 
   - *Leave it completely blank if you intend to just strip the search substring away.*
4. **Scan & Verify**: Click "1. Search & Preview". Double-click specific rows to toggle their selection if you want to skip certain files.
5. **Execution**: Click the green "2. Execute Rename" button to apply changes instantly.

---

## 中文

一个基于 Python Tkinter 打造的本地轻量级图形界面（GUI）文件批处理安全工具。采用**“搜索 -> 预览 -> 勾选 -> 执行”**的可视化管道工程，并支持中英双语一键切换，彻底杜绝盲改带来的误伤。

### ✨ 核心特性

- **动态校准机制 (Bug已修复)**：彻底修复了旧版“替换字符失效变直接删除”的内存缓存同步漏洞。无论何时改动“替换为”输入框，预览表格与核心数据流均会毫秒级实时联动，确保替换百分百生效。
- **安全预览沙箱**：引入 ttk.Treeview 预览架构，改名结果在表格中提前演练，所见即所得。
- **一键动态双语**：右上角一键无缝切换中/英文界面，提示词、表头、弹窗完美同步国际化。
- **留空消除模式**：在“替换为”输入框中输入新字符即可实现替换；**若完全留空，则代表直接剔除/删掉**原文件名中的查找字符。
- **智能拟合多选框**：利用标准 ASCII 码拟合 [ X ] 复选状态，支持**鼠标双击单行切换**，并配有一键“全选”/“取消全选”控制面板。
- **浅层文件保护**：默认仅修改当前根目录下的纯文件，自动跳过深层子文件夹，保护目录结构。

### 🛠️ 环境准备

- **Python 3.8+**（仅通过源码运行或自行打包时需要）
- **第三方依赖**：**无**。完全基于 Python 原生标准库（tkinter, os）构建，开箱即用。

### 📥 下载开箱即用版本 (无需安装 Python)

如果你不想配置任何代码环境或执行终端命令，可以直接下载已经封装了所有环境和依赖的独立绿色版：

1. 点击进入本仓库的 [Releases](https://github.com/your_username/FileRenamer/releases) 发布页面。
2. 下载最新版程序：
   - **Windows 系统**：下载 `文件批量替换工具.exe`
3. 直接双击下载好的 `.exe` 文件即可启动工具，内部已完整集成了所有运行依赖。

---

### 🚀 快速使用 (通过源码运行)

1. 克隆本仓库到本地：
   git clone https://github.com/your_username/FileRenamer.git
   cd FileRenamer

2. 直接运行源码：
   python main.py

*(可选) 如果你想亲自使用 PyInstaller 重新打包含所有依赖的单文件可执行程序：*
   pip install pyinstaller
   pyinstaller --clean -F -w --name="文件批量替换工具" main.py

---

### 📖 操作指南

1. **选择路径**：点击 “浏览...” 按钮，选中需要批量修改文件的目标文件夹。
2. **输入查找字符**：在 “查找字符” 框中输入文件名里含有的垃圾片段（如：`_副本`、`[草稿]`）。
3. **输入替换字符**：
   - 在 “替换为” 框中输入期望的新文字。
   - *若想直接删掉查找字符，请保持此框完全空白。*
4. **搜索并验证**：点击 “1. 搜索并预览文件” 按钮。如需排除个别文件，用鼠标**双击**该行即可取消勾选。
5. **执行改名**：核对“新文件名”一列无误后，点击底部绿色的 “2. 执行批量替换” 按钮完成处理。

---

## 📄 License / 开源协议

This project is open-sourced under the [MIT License](LICENSE). 
本项目基于 MIT 协议开源，欢迎自由衍生与演绎。