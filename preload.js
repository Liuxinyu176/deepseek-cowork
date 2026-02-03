const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    saveFile: (filename, content) => ipcRenderer.invoke('save-file', { filename, content }),
    // 这里可以暴露更多 Node.js 能力给前端，例如读取特定目录
});
