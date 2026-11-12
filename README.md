# 英语回译教练

看中文译文，写出英文，再逐句核对指定范文。适合考研、六级作文背诵和回译练习。

## 使用方式

### 在支持 Skills 的工具中使用

下载仓库，将整个 `english-backtranslation-coach` 文件夹放到对应工具的技能目录。在 Codex 中可放入 `~/.codex/skills/`，然后调用 `$english-backtranslation-coach`。

### 通过聊天附件使用

下载仓库 ZIP。如果聊天工具支持读取压缩包，可以上传整个文件。也可以解压后上传 `SKILL.md` 和所选范文文件，并发送以下提示。

> 请阅读 SKILL.md，按照英语回译教练的流程，用附件里的社交媒体篇开始练习。先展示中文译文，等我提交英文后，再逐句对照固定原文，说明信息遗漏、拼写、语法、搭配和可接受的表达差异。

读取附件后能否执行核对脚本，取决于所用工具的能力。无法运行脚本时，使用逐句反馈和定性判断。

## 练习材料

| 材料 | 文件 |
| --- | --- |
| 2005 年考研英语辞职与道歉信 | [references/resignation-2005.json](references/resignation-2005.json) |
| 正确使用社交媒体的重要性，英文与中文对照 | [references/social-media-cet6-2025-06.md](references/social-media-cet6-2025-06.md) |
| 社交媒体篇结构化原文及译文 | [references/social-media-cet6-2025-06.json](references/social-media-cet6-2025-06.json) |

支持上传自己的范文和译文，并指定只练某一段或某一句。

## 字面相似度核对

安装 Python 3 后，准备 UTF-8 编码的 JSON 文件，包含 `reference` 和 `draft` 两个字符串字段。

```json
{
  "reference": "I have decided to quit.",
  "draft": "I have decide to quit."
}
```

```sh
python scripts/compare.py --input input.json
```

脚本忽略空白及直弯单撇号差异，保留大小写和标点差异，并返回匹配比例与差异片段。默认以 90% 作为字面接近的参考阈值，语义和语法还需要结合完整句子判断。

## 材料来源

辞职信来自用户提供的《考研英语高分写作》经典范文 001 照片。社交媒体篇来自用户提供的、标有“星火英语”的《2025 年 6 月大学英语六级考试真题（一）答案与详解》参考范文页。社交媒体篇中文译文根据英文生成。各材料文件保留了来源说明，相关范文版权归原权利人所有。
