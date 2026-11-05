---
title: 用 Arduino 环境开发 WT9932S3-NANO（板定义、FQBN、烧录方式）
board: Wireless-TAG WT9932S3-NANO
source: https://github.com/espressif/arduino-esp32/blob/master/boards.txt
source_doc: https://wiki.wireless-tag.com/docs/zh/WT9932S3-NANO/getting_started.html
retrieved: 2026-11-05
tags: [wt9932s3-nano, arduino, 板定义, fqbn, dfu, 分区表, nano_nora]
---

# 用 Arduino 环境开发 WT9932S3-NANO

## 结论

在 Arduino IDE 里安装 **esp32** 板包（Espressif 出品），选板 **Arduino Nano ESP32**，即可编译下载。原因：WT9932S3-NANO 与 Arduino Nano ESP32 引脚兼容，且内存配置相同。

## 板定义事实（来自 espressif/arduino-esp32 的 boards.txt）

```
nano_nora.name=Arduino Nano ESP32
nano_nora.build.mcu=esp32s3
nano_nora.build.variant=arduino_nano_nora
nano_nora.build.usb_mode=0
nano_nora.build.cdc_on_boot=1
nano_nora.build.dfu_on_boot=1
nano_nora.build.flash_size=16MB
nano_nora.build.partitions=app3M_fat9M_fact512k_16MB
nano_nora.build.psram_type=opi
nano_nora.build.defines=... -DBOARD_HAS_PSRAM ...
nano_nora.upload.tool=dfu-util
```

要点：

- 板 id 是 `nano_nora`，显示名是 `Arduino Nano ESP32`
- Flash 16 MB，默认分区 `app3M_fat9M_fact512k_16MB` → **APP 只有 3 MB**
- PSRAM 类型 opi，且定义了 `BOARD_HAS_PSRAM`
- 烧录工具是 **dfu-util**，不是 esptool

## 命令行

```bash
arduino-cli core install esp32:esp32
arduino-cli compile --fqbn esp32:esp32:nano_nora .
arduino-cli upload  --fqbn esp32:esp32:nano_nora -p /dev/cu.usbmodemXXXX .
```

FQBN 格式：`包名:平台名:板 id` → `esp32:esp32:nano_nora`。

## PlatformIO

```ini
[env:nano]
platform = espressif32
board = arduino_nano_esp32
framework = arduino
```

`platformio/platform-espressif32` 的 `boards/arduino_nano_esp32.json`：mcu 为 esp32s3，flash 16 MB。

## 烧录（DFU）

官方入门指南里的成功日志特征：

```
Opening DFU capable USB device...
Device ID 2341:0070
DFU state(2) = dfuIDLE, status(0) = No error condition is present
```

- VID:PID = `2341:0070`（Arduino 的 Vendor ID）
- 进不了下载模式时：按住 **BOOT**（GPIO0）→ 点 **RESET** → 松开 BOOT

## 易混淆项

- `arduino/arduino-esp32`（Arduino 自家仓库）里只有 `nora_w10` 变体（4 MB Flash、QSPI PSRAM），是**裸 NORA-W10 模组**，不是整板；不要拿它和本板对照。
- 需要 HID 时改 USB Mode；改完串口会消失，属正常现象。
