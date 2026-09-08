# 演示图片素材

本目录用于随 Git 仓库分发开发和演示素材，文件名与 `server/sql/data.sql` 中的种子数据一致。

## 目录

```text
server/assets/
├── README.md
└── product/
    ├── phone.jpg / phone1.jpg
    ├── earphone.jpg / earphone1.jpg
    ├── watch.jpg / watch1.jpg
    ├── aircon.jpg / aircon1.jpg
    ├── washer.jpg / washer1.jpg
    ├── fridge.jpg / fridge1.jpg
    ├── shoes.jpg / shoes1.jpg
    ├── tshirt.jpg / tshirt1.jpg
    ├── milk.jpg / milk1.jpg
    └── apple.jpg / apple1.jpg
```

这些是开发环境演示素材，不是生产商品摄影图。初始化数据库后，将 `product/` 目录复制到 `.env` 中 `UPLOAD_DIR` 对应目录下，即可通过 `/uploads14/product/*.jpg` 访问：

```powershell
Copy-Item server/assets/product F:/uploads14/product -Recurse -Force
```

生产环境应替换为经过授权的正式商品图，不要提交用户上传文件、密钥、Chroma 数据或运行时生成目录。
