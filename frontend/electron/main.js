import { app, BrowserWindow, ipcMain, screen } from 'electron'
import { join } from 'path'
import { fileURLToPath } from 'url'

const __dirname = fileURLToPath(new URL('.', import.meta.url))

// 一体机应用配置
const KIOSK_CONFIG = {
  fullscreen: true,          // 全屏模式
  kiosk: true,              // 一体机模式
  autoHideMenuBar: true,    // 隐藏菜单栏
  frame: false,             // 无边框
  resizable: false,         // 不可调整大小
  minimizable: false,       // 不可最小化
  maximizable: false        // 不可最大化
}

// 开发环境配置
const DEV_CONFIG = {
  fullscreen: false,
  kiosk: false,
  autoHideMenuBar: false,
  frame: true,
  resizable: true,
  minimizable: true,
  maximizable: true
}

let mainWindow

function createWindow() {
  // 获取主显示器信息
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize

  // 根据环境选择配置
  const isDev = process.env.NODE_ENV === 'development'
  const windowConfig = isDev ? DEV_CONFIG : KIOSK_CONFIG

  // 创建浏览器窗口
  mainWindow = new BrowserWindow({
    width: isDev ? 1200 : width,
    height: isDev ? 800 : height,
    x: 0,
    y: 0,
    ...windowConfig,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: join(__dirname, 'preload.js'),
      webSecurity: !isDev // 开发环境禁用web安全
    },
    icon: join(__dirname, '../assets/icon.png'), // 应用图标
    title: '不动产自助查询一体机',
    backgroundColor: '#ffffff',
    show: false // 先隐藏，等加载完成后显示
  })

  // 加载应用
  if (isDev) {
    // 开发模式：加载开发服务器
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    // 生产模式：加载构建后的文件
    mainWindow.loadFile(join(__dirname, '../dist/index.html'))
  }

  // 窗口准备好后显示
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
    
    // 生产环境下启用一体机模式
    if (!isDev) {
      mainWindow.setKiosk(true)
      mainWindow.setFullScreen(true)
    }
  })

  // 处理窗口关闭
  mainWindow.on('closed', () => {
    mainWindow = null
  })

  // 防止新窗口打开
  mainWindow.webContents.setWindowOpenHandler(() => {
    return { action: 'deny' }
  })

  // 一体机安全设置：禁用右键菜单
  if (!isDev) {
    mainWindow.webContents.on('context-menu', (e) => {
      e.preventDefault()
    })
  }
}

// 应用事件处理
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// IPC通信处理
ipcMain.handle('get-app-version', () => {
  return app.getVersion()
})

ipcMain.handle('get-system-info', () => {
  return {
    platform: process.platform,
    arch: process.arch,
    version: process.version,
    electronVersion: process.versions.electron
  }
})

// 设备相关IPC
ipcMain.handle('check-device-status', async () => {
  // TODO: 检查硬件设备状态
  return {
    camera: 'online',
    idCardReader: 'online',
    printer: 'online',
    stampMachine: 'online'
  }
})

// 打印功能
ipcMain.handle('print-document', async (event, data) => {
  // TODO: 调用打印功能
  return { success: true, message: '打印成功' }
})

// 一体机专用：禁用快捷键
if (process.env.NODE_ENV !== 'development') {
  app.on('browser-window-created', (_, window) => {
    window.webContents.on('before-input-event', (event, input) => {
      // 禁用F12、Ctrl+Shift+I等开发者工具快捷键
      if (input.key === 'F12' || 
          (input.control && input.shift && input.key === 'I') ||
          (input.control && input.shift && input.key === 'J') ||
          (input.control && input.key === 'U')) {
        event.preventDefault()
      }
    })
  })
} 