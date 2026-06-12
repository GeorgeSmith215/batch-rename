import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# --- 全局中英文双语配置字典 ---
LANGUAGES = {
    "zh": {
        "title": "文件名称批量替换工具 (安全预览版)",
        "path_lbl": "选择路径:",
        "browse_btn": "浏览...",
        "old_lbl": "查找字符:",
        "new_lbl": "替换为:",
        "tip_lbl": "（留空则直接清除查找字符）",
        "search_btn": "1. 搜索并预览文件",
        "run_btn": "2. 执行批量替换",
        "toggle_btn": "English",
        "select_all": "全选",
        "deselect_all": "取消全选",
        "col_status": "选择",
        "col_old": "原文件名",
        "col_new": "新文件名",
        "warn_no_path": "请先选择目标文件夹路径！",
        "err_path_not_exist": "指定的文件夹路径不存在，请检查！",
        "warn_no_match": "请输入需要被替换的待查字符！",
        "info_no_files": "未找到包含该字符的文件。",
        "info_no_selected": "请先在列表中勾选需要修改的文件！",
        "success_title": "处理完成",
        "success_msg": "批量重命名结束！\n成功修改: {} 个文件\n失败: {} 个",
        "err_scan": "遍历文件时发生异常: ",
    },
    "en": {
        "title": "Batch File Renamer (Safe Preview)",
        "path_lbl": "Folder Path:",
        "browse_btn": "Browse...",
        "old_lbl": "Find Target:",
        "new_lbl": "Replace With:",
        "tip_lbl": "(Leave blank to delete target string)",
        "search_btn": "1. Search & Preview",
        "run_btn": "2. Execute Rename",
        "toggle_btn": "中文",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "col_status": "Select",
        "col_old": "Original Name",
        "col_new": "New Name",
        "warn_no_path": "Please select a target folder path first!",
        "err_path_not_exist": "The specified folder path does not exist!",
        "warn_no_match": "Please enter the character string to find!",
        "info_no_files": "No matching files found.",
        "info_no_selected": "Please check at least one file from the list!",
        "success_title": "Completed",
        "success_msg": "Batch rename finished!\nSuccessfully modified: {} files\nFailed: {}",
        "err_scan": "Exception occurred during scanning: ",
    },
}


class FileRenamerApp:

    def __init__(self, root):
        self.root = root
        self.current_lang = "zh"  # 默认中文
        self.matched_files = []  # 核心缓存数组

        self.initialize_ui()
        self.refresh_ui_text()

    def initialize_ui(self):
        """构建整体应用程序的容器及布局"""
        self.root.geometry("700x540")
        self.root.minsize(650, 480)

        # 1. 顶部语言切换
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=15, pady=5)

        self.lang_btn = tk.Button(
            top_frame, text="", command=self.toggle_language, relief=tk.GROOVE
        )
        self.lang_btn.pack(side="right")

        # 2. 上半部分：核心输入卡片区
        config_card = tk.LabelFrame(self.root, text="", padx=15, pady=10)
        config_card.pack(fill="x", padx=15, pady=5)

        self.path_label = tk.Label(config_card)
        self.path_label.grid(row=0, column=0, sticky="e", pady=5)
        self.path_entry = tk.Entry(config_card, width=50)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.path_btn = tk.Button(
            config_card, text="", command=self.select_folder_path
        )
        self.path_btn.grid(row=0, column=2, padx=5, pady=5)

        self.old_str_label = tk.Label(config_card)
        self.old_str_label.grid(row=1, column=0, sticky="e", pady=5)
        self.old_str_entry = tk.Entry(config_card)
        self.old_str_entry.grid(
            row=1, column=1, columnspan=2, padx=5, pady=5, sticky="we"
        )

        self.new_str_label = tk.Label(config_card)
        self.new_str_label.grid(row=2, column=0, sticky="e", pady=5)
        self.new_str_entry = tk.Entry(config_card)
        self.new_str_entry.grid(
            row=2, column=1, columnspan=2, padx=5, pady=5, sticky="we"
        )

        self.tip_label = tk.Label(config_card, text="", fg="#7f8c8d", font=("", 9))
        self.tip_label.grid(row=3, column=1, columnspan=2, sticky="w", padx=5)

        config_card.columnconfigure(1, weight=1)

        # 3. 中间部分：工具栏
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.pack(fill="x", padx=15, pady=5)

        self.search_btn = tk.Button(
            toolbar_frame,
            text="",
            bg="#0275d8",
            fg="white",
            font=("", 10, "bold"),
            command=self.execute_search_scan,
        )
        self.search_btn.pack(side="left", ipady=2, ipadx=5)

        self.select_all_btn = tk.Button(
            toolbar_frame, text="", command=lambda: self.update_global_selection(True)
        )
        self.select_all_btn.pack(side="right", padx=2)

        self.deselect_all_btn = tk.Button(
            toolbar_frame, text="", command=lambda: self.update_global_selection(False)
        )
        self.deselect_all_btn.pack(side="right", padx=2)

        # 4. Treeview 预览区
        tree_container = tk.Frame(self.root)
        tree_container.pack(fill="both", expand=True, padx=15, pady=5)

        self.preview_tree = ttk.Treeview(
            tree_container, columns=("check", "old", "new"), show="headings"
        )
        self.preview_tree.pack(side="left", fill="both", expand=True)

        v_scrollbar = ttk.Scrollbar(
            tree_container, orient="vertical", command=self.preview_tree.yview
        )
        self.preview_tree.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

        self.preview_tree.bind("<Double-1>", self.handle_row_toggle)

        # 5. 底部执行区域
        self.run_btn = tk.Button(
            self.root,
            text="",
            bg="#107c41",
            fg="white",
            font=("", 11, "bold"),
            height=2,
            command=self.execute_batch_rename,
        )
        self.run_btn.pack(fill="x", padx=15, pady=15)

    def refresh_ui_text(self):
        """同步全界面语言文本"""
        lang_pack = LANGUAGES[self.current_lang]
        self.root.title(lang_pack["title"])
        self.lang_btn.config(text=lang_pack["toggle_btn"])
        self.path_label.config(text=lang_pack["path_lbl"])
        self.path_btn.config(text=lang_pack["browse_btn"])
        self.old_str_label.config(text=lang_pack["old_lbl"])
        self.new_str_label.config(text=lang_pack["new_lbl"])
        self.tip_label.config(text=lang_pack["tip_lbl"])
        self.search_btn.config(text=lang_pack["search_btn"])
        self.run_btn.config(text=lang_pack["run_btn"])
        self.select_all_btn.config(text=lang_pack["select_all"])
        self.deselect_all_btn.config(text=lang_pack["deselect_all"])

        self.preview_tree.heading("check", text=lang_pack["col_status"])
        self.preview_tree.heading("old", text=lang_pack["col_old"])
        self.preview_tree.heading("new", text=lang_pack["col_new"])

        self.preview_tree.column("check", width=70, minwidth=60, anchor="center")
        self.preview_tree.column("old", width=280, minwidth=150, anchor="w")
        self.preview_tree.column("new", width=280, minwidth=150, anchor="w")

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "zh" else "zh"
        self.refresh_ui_text()
        if self.matched_files:
            self.render_data_to_treeview()

    def select_folder_path(self):
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_dir)

    def execute_search_scan(self):
        """扫描路径，动态生成包含替换预期的新文件名数据"""
        lang_pack = LANGUAGES[self.current_lang]
        folder_path = self.path_entry.get().strip()
        old_str = self.old_str_entry.get()
        new_str = self.new_str_entry.get()  # 捕获当前输入的替换字符

        if not folder_path:
            messagebox.showwarning("⚠️", lang_pack["warn_no_path"])
            return
        if not os.path.exists(folder_path):
            messagebox.showerror("❌", lang_pack["err_path_not_exist"])
            return
        if not old_str:
            messagebox.showwarning("⚠️", lang_pack["warn_no_match"])
            return

        self.matched_files.clear()
        self.clear_treeview_nodes()

        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path) and old_str in filename:
                    # 修复点：直接在此处实时将真正的 new_str 塞入缓存
                    new_filename = filename.replace(old_str, new_str)
                    self.matched_files.append({
                        "checked": True,
                        "old_name": filename,
                        "new_name": new_filename,
                        "full_path": file_path
                    })

            if not self.matched_files:
                messagebox.showinfo("ℹ️", lang_pack["info_no_files"])
                return

            self.render_data_to_treeview()

        except Exception as e:
            messagebox.showerror("❌", f"{lang_pack['err_scan']}{str(e)}")

    def render_data_to_treeview(self):
        """渲染更新，规避非标准空格错误"""
        self.clear_treeview_nodes()

        # 实时获取输入框中最新的替换文本，防止中途点击全选或切语言时新名称丢失
        old_str = self.old_str_entry.get()
        new_str = self.new_str_entry.get()

        for idx, file_info in enumerate(self.matched_files):
            # 动态重新计算新名字，保证替换实时生效
            if old_str:
                file_info["new_name"] = file_info["old_name"].replace(old_str, new_str)

            # 标准 ASCII 空格，杜绝底层字符集解析 Bug
            status_checkbox = "[ X ]" if file_info["checked"] else "[   ]"
            self.preview_tree.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(
                    status_checkbox,
                    file_info["old_name"],
                    file_info["new_name"]
                )
            )

    def handle_row_toggle(self, event):
        selected_item_id = self.preview_tree.identify_row(event.y)
        if selected_item_id:
            idx = int(selected_item_id)
            self.matched_files[idx]["checked"] = not self.matched_files[idx]["checked"]
            status_checkbox = "[ X ]" if self.matched_files[idx]["checked"] else "[   ]"
            self.preview_tree.set(selected_item_id, column="check", value=status_checkbox)

    def update_global_selection(self, status):
        if not self.matched_files:
            return
        for file_info in self.matched_files:
            file_info["checked"] = status
        self.render_data_to_treeview()

    def clear_treeview_nodes(self):
        for node in self.preview_tree.get_children():
            self.preview_tree.delete(node)

    def execute_batch_rename(self):
        lang_pack = LANGUAGES[self.current_lang]
        folder_path = self.path_entry.get().strip()
        old_str = self.old_str_entry.get()
        new_str = self.new_str_entry.get()

        active_payloads = [file for file in self.matched_files if file["checked"]]
        if not active_payloads:
            messagebox.showwarning("⚠️", lang_pack["info_no_selected"])
            return

        success_count = 0
        fail_count = 0

        for file_info in active_payloads:
            source_path = file_info["full_path"]
            # 最终执行重命名时，做最后一层安全校验，确保采用的是输入框当前最新输入的值
            final_new_name = file_info["old_name"].replace(old_str, new_str)
            target_path = os.path.join(folder_path, final_new_name)

            try:
                if os.path.exists(source_path):
                    os.rename(source_path, target_path)
                    success_count += 1
                else:
                    fail_count += 1
            except Exception:
                fail_count += 1

        messagebox.showinfo(
            lang_pack["success_title"],
            lang_pack["success_msg"].format(success_count, fail_count)
        )

        self.matched_files.clear()
        self.clear_treeview_nodes()


if __name__ == "__main__":
    app_root = tk.Tk()
    app = FileRenamerApp(app_root)
    app_root.mainloop()