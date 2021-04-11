# Mirror+
一个 MCDR 插件，用于镜像服管理。

## Features

- 颜色区分——将镜像服和主服务器输出区分
- 简单的配置——无需纠结于 RCON 等复杂配置
- 一键与生存服同步——无需进入服务器后台

## How it works?
Mirror+ 使用 `subprocess.Popen` 启动镜像服，以此来控制镜像服的标准输入输出流。就酱

## How to use?
1. 将插件文件扔到主服务器 `plugins` 文件夹，并重载插件；
2. 编辑配置文件；
3. 将镜像服务器所需文件复制到配置文件指定的工作文件夹中；
4. 在主服务器中使用指令启动镜像服。

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
        "start": 0,
        "stop": 0,
        "kill": 0,
        "restart": 0,
        "sync": 0,
        "reload": 0,
        "send": 0
    }
}
```

## Commands
- `!!mirror` 显示帮助消息
- `!!mirror start|stop|restart|sync` 开启 / 关闭 / 重启 / 同步镜像服
- `!!mirror send <command>` 向镜像服发送指令
- `!!mirror reload` 重载配置文件

## Attention!
请注意，**镜像服本身也是一个 Minecraft 服务端。**因此，你需要在工作文件夹建立一个完整的 Minecraft 服务端，并设置与主服务器不同的端口。

如果需要更便捷地切换到镜像服务器，请使用 [Velocity](https://velocitypowered.com/) 或者 [BungeeCord](https://www.spigotmc.org/wiki/about-bungeecord/)。

使用 Mirror+ 与生存服同步时，将同步**整个世界文件夹**，即镜像服的世界文件夹**直接删除**，并替换为当前主服务器的世界文件夹，并且**不会保留原备份**。  
这个过程中**不会进行任何确认提示**（暂时），请谨慎操作。如果需要同步部分区域，请与 [RegionFileUpdater](https://github.com/TISUnion/RegionFileUpdater) 配合使用。

## Compatibility
**在以下环境测试通过：**
```
System: Windows Server 2003 x64
Python version: 3.9
Main Server:
	Type: Fabric (Vanilla)
	MCDR: 1.3
Mirror Server:
	Type: Fabric (Vanlilla)
	MCDR: Not installed
```

