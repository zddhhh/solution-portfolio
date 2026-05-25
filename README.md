# Portfolio Site - AI+行业方案自动化作品集

个人作品集网站，用于展示AI自动化+解决方案工程的项目案例。

## 使用方式

1. 直接浏览器打开 `index.html` 预览
2. 部署到 GitHub Pages：
   - 创建仓库（如 `yourname.github.io` 或任意仓库名）
   - 推送 `index.html` + `assets/` 到 `main` 分支
   - Settings → Pages → Source 选 `main` 分支
   - 访问 `https://yourname.github.io/`

## 添加案例素材

1. 将截图放到 `assets/` 目录（建议 `case1.png`, `case2.png` ...）
2. 在 `index.html` 中找到对应 case-card 的 `<div class="placeholder">`
3. 替换为 `<img src="assets/case1.png" alt="案例截图">`

## 脱敏要求

- 去掉客户名称/logo
- 模糊或替换具体价格数字
- 不暴露内部流程细节
- 设备型号可保留（公开信息）

## 目录结构

```
29-portfolio-site/
├── index.html      # 主页面
├── assets/         # 截图素材
│   ├── case1.png
│   ├── case2.png
│   └── ...
└── README.md
```
