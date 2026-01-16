const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false, // Security best practice
            contextIsolation: true  // Security best practice
        }
    });

    mainWindow.loadFile('index.html');
    
    // 打开开发工具
    // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});

// 示例：处理来自渲染进程的文件保存请求
ipcMain.handle('save-file', async (event, { filename, content }) => {
    const fs = require('fs');
    const filePath = path.join(app.getPath('downloads'), filename);
    
    try {
        fs.writeFileSync(filePath, content);
        return { success: true, path: filePath };
    } catch (error) {
        return { success: false, error: error.message };
    }
});
