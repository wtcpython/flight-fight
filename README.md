# 飞机大战 (Flight-Fight)

飞机大战，一个经典小游戏

## 游戏介绍

### 角色移动

使用 **↑ ↓ ← →** 移动我方飞机

### 角色技能

**"e"** 技能：扣除飞机 **当前血量的30%**，使子弹造成的伤害增加 **3倍**，**随机** 回复一定能量，持续 **7s**，时间间隔cd 为 **10s**

**"空格"** 技能：如果当前持有一定量的炸弹，将会消耗一个炸弹，对 **屏幕下方 $\frac{2}{3}$ 区域** 的全体敌人造成一定伤害，并根据敌人的数量（至多10个）**按一定比例** 回复生命值，回复后的血量 **不超过生命值上限**

**"f"** 技能：聚怪，**消耗35能量**，将全屏的敌机向屏幕中上方吸附，对大型战机无效

**"q"** 技能：当能量充满的时候，消耗所有能量，子弹由 **单发** 升级为 **3发**，持续 **14s**，该技能具有 **充能动画**

### 其他特性

    1. 当成功击杀大型战机时，有一定概率获得一个炸弹，或者回复10点能量

* V 0.5 版本修改：追加随机效果：有 **一定概率失去** 一个炸弹，有 **一定概率失去** 10点能量

### 如何从源代码构建

    1. python >= 3.10
    2. pygame-ce >= 2.4 (使用 pygame-ce 而不是 pygame)
    3. Windows, MacOS 或 Linux 等任意受支持的桌面操作系统
