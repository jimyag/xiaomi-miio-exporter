# 小米物联网设置 exporter

## 使用

获取设备 token，参考 [获取设备 token](#获取设备-token)

修改 `config.py` 文件中的设备信息

```bash
pip install -r requirements.txt
python exporter.py
```

访问 `http://localhost:8000/metrics` 查看数据

使用 docker 运行

```bash
make

```

## 获取设备 token

```bash
pip install micloud

micloud get-devices  -u <邮箱/手机号> --pretty --country 'cn'
# 输入密码
```

即可获取米家设备列表

## 参考

- [小米物联网平台](https://home.miot-spec.com/spec/cuco.plug.v3)