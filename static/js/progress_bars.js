const memoryBar = document.getElementById("memoryBar");
const memoryLabel = document.getElementById("memoryLabel");
const diskCBar = document.getElementById("diskCBar");
const diskCLabel = document.getElementById("diskCLabel");
const diskDBar = document.getElementById("diskDBar");
const diskDLabel = document.getElementById("diskDLabel");

function paintProgreessBar(bar, percentUsed) {
    if (percentUsed < 10) {
            bar.style.backgroundColor = "#6BC1FF";
        } else if (percentUsed >= 10 && percentUsed < 20) {
            bar.style.backgroundColor = "#6BFFE3";
        } else if (percentUsed >= 20 && percentUsed < 30) {
            bar.style.backgroundColor = "#6BFF9C";
        } else if (percentUsed >= 30 && percentUsed < 40) {
            bar.style.backgroundColor = "#7EFF6B";
        } else if (percentUsed >= 40 && percentUsed < 50) {
            bar.style.backgroundColor = "#D1FF6B";
        } else if (percentUsed >= 50 && percentUsed < 60) {
            bar.style.backgroundColor = "#FFF86B";
        } else if (percentUsed >= 60 && percentUsed < 70) {
            bar.style.backgroundColor = "#FFE36B";
        } else if (percentUsed >= 70 && percentUsed < 80) {
            bar.style.backgroundColor = "#FFC46B";
        } else if (percentUsed >= 80 && percentUsed < 90) {
            bar.style.backgroundColor = "#FFA06E";
        } else {
            bar.style.backgroundColor = "#FF6E6E";
        }
}

function updateMemoryProgressBar() {
    fetch('/memory-usage')
    .then(response => response.json())
    .then(data => {
        const totalMemory = data.total_memory;
        const usedMemory = data.memory_usage;
        const percentUsedMemory = data.memory_percent;
        memoryBar.style.width = percentUsedMemory + "%";
        paintProgreessBar(memoryBar, percentUsedMemory);
    });
}

function updateDiskCProgressBar() {
    fetch('/disk-c')
    .then(response => response.json())
    .then(data => {
        const totalSpace = data.total_size;
        const freeSpace = data.free_size;
        const percentageFree = 100 - Math.round((freeSpace / totalSpace) * 100);
        diskCBar.style.width = percentageFree + "%";
        paintProgreessBar(diskCBar, percentageFree);
    });
}

function updateDiskDProgressBar() {
    fetch('/disk-d')
    .then(response => response.json())
    .then(data => {
        const totalSpace = data.total_size;
        const freeSpace = data.free_size;
        const percentageFree = 100 - Math.round((freeSpace / totalSpace) * 100);
        diskDBar.style.width = percentageFree + "%";
        paintProgreessBar(diskDBar, percentageFree);
    });
}

function updateCpuPercent() {
    fetch('/cpu_percent')
    .then(response => response.json())
    .then(data => {
        // Обновление значений процентного использования CPU и ширины прогресс-баров
        for (let i = 0; i < data.cpu_percent.length; i++) {
            document.getElementById('cpuPercent' + (i + 1)).textContent = data.cpu_percent[i] + '%';
            document.getElementById('cpuBar' + (i + 1)).style.width = data.cpu_percent[i] + '%';
            paintProgreessBar(document.getElementById('cpuBar' + (i + 1)), data.cpu_percent[i]);
        }
    })
    .catch(error => console.error('Ошибка при получении значений процентного использования CPU:', error));
}

updateMemoryProgressBar();
updateDiskCProgressBar();
updateDiskDProgressBar();
updateCpuPercent();

setInterval(updateMemoryProgressBar, 1000);
setInterval(updateDiskCProgressBar, 10000);
setInterval(updateDiskDProgressBar, 10000);
setInterval(updateCpuPercent, 500);