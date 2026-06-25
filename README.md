# ZeroTier - mipsel
<p align="center">
  <img alt="GitHub Created At" src="https://img.shields.io/github/created-at/lmq8267/ZeroTierOne?logo=github&label=%E5%88%9B%E5%BB%BA%E6%97%A5%E6%9C%9F">
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flmq8267%2FZeroTierOne&count_bg=%2395C10D&title_bg=%23555555&icon=github.svg&icon_color=%238DC409&title=%E8%AE%BF%E9%97%AE%E6%95%B0&edge_flat=false"/></a>
<a href="https://github.com/lmq8267/ZeroTierOne/releases"><img src="https://img.shields.io/github/downloads/lmq8267/ZeroTierOne/total?logo=github&label=%E4%B8%8B%E8%BD%BD%E9%87%8F"></a>
<a href="https://github.com/lmq8267/ZeroTierOne/graphs/contributors"><img src="https://img.shields.io/github/contributors-anon/lmq8267/ZeroTierOne?logo=github&label=%E8%B4%A1%E7%8C%AE%E8%80%85"></a>
<a href="https://github.com/lmq8267/ZeroTierOne/releases/"><img src="https://img.shields.io/github/release/lmq8267/ZeroTierOne?logo=github&label=%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC"></a>
<a href="https://github.com/lmq8267/ZeroTierOne/issues"><img src="https://img.shields.io/github/issues-raw/lmq8267/ZeroTierOne?logo=github&label=%E9%97%AE%E9%A2%98"></a>
<a href="https://github.com/lmq8267/ZeroTierOne/discussions"><img src="https://img.shields.io/github/discussions/lmq8267/ZeroTierOne?logo=github&label=%E8%AE%A8%E8%AE%BA"></a>
<a href="GitHub repo size"><img src="https://img.shields.io/github/repo-size/lmq8267/ZeroTierOne?logo=github&label=%E4%BB%93%E5%BA%93%E5%A4%A7%E5%B0%8F"></a>
<a href="https://github.com/lmq8267/ZeroTierOne/actions?query=workflow%3ABuild"><img src="https://img.shields.io/github/actions/workflow/status/lmq8267/ZeroTierOne/zerotier.yml?branch=dev&logo=github&label=%E6%9E%84%E5%BB%BA%E7%8A%B6%E6%80%81" alt="Build status"></a>
</p>

下载点右边的Releases

项目地址https://github.com/zerotier/ZeroTierOne

### `Star`

[![Stargazers](https://bytecrank.com/nastyox/reporoster/php/stargazersSVG.php?user=lmq8267&repo=ZeroTierOne)](https://github.com/lmq8267/ZeroTierOne/stargazers)

### `Fork`

[![Forkers](https://bytecrank.com/nastyox/reporoster/php/forkersSVG.php?user=lmq8267&repo=poster-design)](https://github.com/lmq8267/ZeroTierOne/network/members)

## 可靠性与校验

本 fork 面向 Padavan/mipsel 场景提供预编译 `zerotier-one`。为避免下载到 GitHub HTML 页面、旧版兜底包或损坏文件导致程序不可用，安装脚本会下载二进制及对应 MD5，并在启动前校验。

维护者发布或手动上传二进制时，请同时更新以下校验文件：

- `install/<版本>/MD5.txt`：对应 `install/<版本>/zerotier-one` 的 MD5。
- `install/<版本>/tarMD5.txt`：对应 `install/<版本>/zerotier.tar.gz` 的 MD5。
- `install/SHA256SUMS`：仓库内所有发行二进制和 tar 包的 SHA-256 清单，供人工审查和发布前复核。

发布前建议执行：

```sh
sh -n install/zerotier.sh
bash -n install/hiboyzerotier.sh
sh -n install/installzero.sh
(cd install && sha256sum -c SHA256SUMS)
```

## 二进制来源风险

当前仓库只保存预编译 mipsel 二进制和安装脚本，不包含完整 ZeroTier 源码与交叉编译工具链，因此只能校验“仓库里的文件下载后没有损坏或被替换”，不能从本仓库证明这些二进制一定由上游源码可复现构建。

降低风险的建议：

1. 优先使用 `tools/verify-release-artifacts.sh` 做发布前审计，确认二进制是 ELF、压缩包可解包、MD5 与 SHA-256 清单一致。
2. 发布新版本时保留构建环境、上游 ZeroTier commit、交叉编译工具链版本和构建日志。
3. 如果要达到更高可信度，应新增 CI 从 ZeroTier 上游源码交叉编译 mipsel 产物，并把源码 commit、构建脚本和校验和一起发布。
4. 不建议从未知 fork 或不透明网盘替换 `zerotier-one`；替换后必须同步更新 `MD5.txt`、`tarMD5.txt` 和 `SHA256SUMS`。
