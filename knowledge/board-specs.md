---
title: WT9932S3-NANO 硬件规格
board: Wireless-TAG WT9932S3-NANO
source: https://wiki.wireless-tag.com/docs/zh/WT9932S3-NANO/board_features.html
source_en: https://wiki.wireless-tag.com/docs/en/WT9932S3-NANO/board_features.html
doc_version: v1.0.1 (2026-05-12)
retrieved: 2026-11-05
tags: [wt9932s3-nano, 硬件规格, esp32-s3, psram, flash, 供电]
---

# WT9932S3-NANO 硬件规格

WT9932S3-NANO 是深圳市启明云端（Wireless-TAG）推出的超小尺寸无线开发板，基于乐鑫 **ESP32-S3R8**，兼容 Arduino Nano ESP32 生态。

## 主控与存储

- 主控：ESP32-S3R8，Xtensa® 32 位 LX7 双核，主频最高 240 MHz
- ROM：384 kB
- SRAM：512 kB
- Flash：**16 MB**
- PSRAM：**8 MB**

## 无线与接口

- 2.4 GHz Wi-Fi（802.11 b/g/n）
- Bluetooth LE
- USB HID：可通过 USB 模拟键盘、鼠标等人机接口设备
- 兼容 Arduino IoT Cloud

## 供电

- 工作电压：3.3 V
- 外部供电：5 V
- 供电方式（三选一）：
  1. Type-C 接口供电
  2. 排针供电（VIN 或 VBUS）
  3. 半孔焊盘供电

## 板载资源

- BOOT 按键：接模组 IO0（GPIO0），按住上电可进入下载模式
- RESET 按键：接模组 EN 使能脚
- 半孔焊盘（castellated pads）：可直接焊接到用户自有 PCB，适合产品化

## 开发环境

- Arduino IDE（推荐选板：Arduino Nano ESP32）
- MicroPython
- ESP-IDF

## 与 Arduino Nano ESP32 的关系

引脚布局完全兼容，两者都是 ESP32-S3 + 16 MB Flash 平台，因此 Arduino Nano ESP32 的板定义、示例、第三方库可直接复用。差异主要在板级设计：WT9932S3-NANO 提供半孔焊盘、板载 BOOT/RESET 按键，尺寸更小。

> 注意：不要在文档中声称"官方 Nano ESP32 无 PSRAM 所以本板有优势"。Espressif 的 `nano_nora` 板定义配置为 16 MB flash + OPI PSRAM，两者内存档位相同。
