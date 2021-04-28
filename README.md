# Mirror+

一个 MCDR 插件，用于镜像服管理。
在使用之前，请务必仔细阅读这份 README，否则后果自负。


## WTH is a Mirror?

~~镜像服是一个独立于主服务器的服务器，用于测试与研制机器、建筑等。~~


## Why Mirror+?

- 尾随功能——在主服务器启动后自动启动镜像服
- 设置权限——预防小天才误操作的最有效方式
- 颜色区分——将镜像服和主服务器输出区分，易分辨
- 简单配置——无需纠结于 RCON 等复杂选项，快速开始
- 传输指令——在主服务器向镜像服输入指令，支持 MCDR 指令
- 快速同步——无需进入服务器后台，使用命令与生存服同步


## How it works?

Mirror+ 使用 `subprocess.Popen` 启动镜像服，以此来控制镜像服的标准输入输出流。就酱  
啥，这句话听着耳熟？不存在的，你肯定记错了 :P


## How to use?

1. 将插件文件移动到主服务器 MCDR 的 `plugins` 文件夹  
2. 根据需求编辑配置文件  
3. 将镜像服务端移动到配置文件指定的工作文件夹中，比如 `/mirror`  
4. 重载插件，并在主服务器中使用指令启动镜像服  


## Config File

```json5
{
    "work_folder": "mirror", // 工作文件夹
    "world_name": [
        "world" // 要同步的世界文件夹
    ],
    "start_command": "java -Xmx4G -jar server.jar", // 镜像服启动命令
    "start_after_main": true, // 是否跟随主服务器启动
    "minimum_permission_level": { // 指令权限
        "start": 0, // 指令对应的 MCDR 权限级别
        "stop": 0,
        "kill": 0,
        "restart": 0,
        "sync": 0,
        "reload": 0,
        "send": 0,
        "status": 0
    }
}
```


## Commands

- `!!mirror` 显示帮助消息和控制面板
- `!!mirror start|stop|restart|sync` 开启 / 关闭 / 重启 / 同步镜像服
- `!!mirror status` 查看当前状态
- `!!mirror send <command>` 向镜像服发送指令
- `!!mirror reload` 重载配置文件


## Attention!

请注意， **镜像服本身也是一个 Minecraft 服务端。** 因此，你需要在工作文件夹建立一个完整的 Minecraft 服务端，并设置与主服务器不同的端口。然后，使用设定的镜像服端口连接到镜像服。

如果需要更便捷地切换到镜像服务器，请使用 [Velocity](https://velocitypowered.com/) 或者 [BungeeCord](https://www.spigotmc.org/wiki/about-bungeecord/)。

使用 Mirror+ 与生存服同步时，将同步**整个世界文件夹**，在此之前会将镜像服的世界文件夹**直接删除**，并且**不会保留原备份**。  
这个过程中**不会进行任何确认提示**（暂时），请谨慎操作。如果仅需要同步部分区域，请与 [RegionFileUpdater](https://github.com/TISUnion/RegionFileUpdater) 配合使用。

与生存服同步时，Mirror+ 向生存服发送 `/save-all flush` 命令，但在发布下个版本前，**不会检测是否保存完毕，而是等待一段时间。**等待时间可以在配置文件中设置——请确保这个值与你的服务器性能匹配。

不建议在镜像服上启用 RCON 功能——这可能导致创造服无法正常关闭，必须杀死其进程。详见 [MC-154617](https://bugs.mojang.com/browse/MC-154617)


## Compatibility

Mirror+ 在以下环境测试通过。

```
System: Windows Server 2003, ArchLinux 2020.04.01
Python version: 3.7, 3.8, 3.9
Main Server:
	Type: Fabric, Vanilla
	MCDR: 1.4.1, None
Mirror Server:
	Type: Fabric, Vanilla
	MCDR: 1.4.1, 1.3, None
```


## Bug Report

如果 Mirror+ 在你的服务器出现了问题，请向我报告。最简单的方式是提交一个 Issue。
一般只为最后一个发布版本提供支持。
