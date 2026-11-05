---
title: WT9932S3-NANO 常见坑与排查
board: Wireless-TAG WT9932S3-NANO
source: 实操与官方文档整理
source_doc: https://wiki.wireless-tag.com/docs/zh/WT9932S3-NANO/getting_started.html
retrieved: 2026-11-05
tags: [wt9932s3-nano, 排查, dfu, 引脚编号, 分区表, psram, usb]
---

# 常见坑与排查

## 1. 上传失败 / 找不到设备

- 现象：编译通过，上传卡住或提示找不到 DFU 设备
- 判据：设备管理器 / `ls /dev/cu.*` 里是否有 `2341:0070`
- 处理：按住 **BOOT**（GPIO0）→ 点一下 **RESET** → 松开 BOOT，再上传
- 根因：`nano_nora` 板定义使用 `dfu-util` 烧录，需要 Board 处于 DFU 模式

## 2. 代码没错但不工作（引脚编号陷阱）

- 现象：照抄示例，代码编译通过，外设无反应
- 判据：示例里写的是 `D4` 还是 `4`。板定义默认 `PinNumbers = By Arduino pin`，`D4` = GPIO7，而裸数字 `4` 指 GPIO4
- 处理：统一用 `D0..D13` / `A0..A7` 宏；或把 `PinNumbers` 菜单切成 native GPIO

## 3. 固件太大烧不进去

- 现象：`Sketch too big`
- 判据：默认分区 `app3M_fat9M_fact512k_16MB`，APP 上限约 3 MB
- 处理：自定义分区表，把 app 分区调大；16 MB Flash 不会自动全部可用

## 4. 用了 PSRAM 的库报分配失败

- 现象：`ps_malloc` 返回 NULL / 摄像头初始化失败
- 判据：`ESP.getPsramSize()` 是否为 8 MB
- 处理：板定义已设 `psram_type=opi` 且定义 `BOARD_HAS_PSRAM`，正常应可用；若自己换了板型或自定义 memory type，需重新对齐为 OPI

## 5. 改 USB 模式后串口消失

- 现象：切换为 HID 后电脑上不再出现串口
- 判据：`usb_mode` 与 `cdc_on_boot` 的取值
- 处理：属预期行为；需要恢复时按住 BOOT 进 DFU 重新烧回 CDC 固件

## 6. 双核代码行为异常

- 现象：`loop()` 里的任务与预期核不符
- 判据：板定义 `ARDUINO_RUNNING_CORE=1`
- 处理：`loop()` 跑在 core 1，`setup()` 也在 core 1；要固定核用 `xTaskCreatePinnedToCore`

## 7. 对外宣传时的口径风险

- 不要写"官方 Arduino Nano ESP32 没有 PSRAM，所以我们有 8 MB"——官方板定义是 16 MB flash + OPI PSRAM，两边同档
- 真正可讲的差异：半孔焊盘可贴片、板载 BOOT/RESET、尺寸更小、供货与价格
