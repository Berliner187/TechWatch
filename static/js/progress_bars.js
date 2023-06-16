const memoryBar = document.getElementById("memoryBar");
const memoryLabel = document.getElementById("memoryLabel");
const diskCBar = document.getElementById("diskCBar");
const diskCLabel = document.getElementById("diskCLabel");
const diskDBar = document.getElementById("diskDBar");
const diskDLabel = document.getElementById("diskDLabel");

function paintProgreessBar(progressBar, percentageFree) {
    if (percentageFree >= 90) {
        progressBar.classList.add('danger');
        progressBar.classList.remove('warning');
      } else if (percentageFree >= 80) {
        progressBar.classList.add('warning');
        progressBar.classList.remove('danger');
      } else {
        progressBar.classList.remove('warning');
        progressBar.classList.remove('danger');
      }
      if (percentageFree < 20) {
        progressBar.style.backgroundColor = "#6BFFE3";
      } else if (percentageFree < 30) {
        progressBar.style.backgroundColor = "#6BFF9C";
      } else if (percentageFree < 40) {
        progressBar.style.backgroundColor = "#7EFF6B";
      } else if (percentageFree < 50) {
        progressBar.style.backgroundColor = "#D1FF6B";
      } else if (percentageFree < 60) {
        progressBar.style.backgroundColor = "#FFF86B";
      } else if (percentageFree < 70) {
        progressBar.style.backgroundColor = "#FFE36B";
      } else if (percentageFree < 80) {
        progressBar.style.backgroundColor = "#FFC46B";
      } else if (percentageFree < 90) {
        progressBar.style.backgroundColor = "#FFA06E";
      } else {
        progressBar.style.backgroundColor = "#FF6E6E";
      }
}


function updateMemoryProgressBar() {
    fetch('/memory-usage')
    .then(response => response.json())
    .then(data => {
        const percentUsedMemory = data.memory_percent;
        memoryBar.style.width = percentUsedMemory + "%";
        paintProgreessBar(memoryBar, percentUsedMemory);
    });
}

function updateDisksProgressBar() {
    fetch('/disks-info')
        .then(response => response.json())
        .then(data => {

            for (let i = 0; i < data.length; i++) {
                const diskData = data[i];
                const diskBar = document.getElementById(`disk_${i}`);
                const totalSpace = diskData.total_size;
                const freeSpace = diskData.free_size;
                const percentageFree = 100 - Math.round((freeSpace / totalSpace) * 100);
                diskBar.style.width = percentageFree + "%";
                paintProgreessBar(diskBar, percentageFree);
            }
        })

    .catch(error => console.error('Error fetching disks info', error));
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

setTimeout(updateCpuPercent(), 2000);
setTimeout(updateMemoryProgressBar(), 2000);
setTimeout(updateDisksProgressBar(), 2000);

setInterval(updateCpuPercent, 500);
setInterval(updateMemoryProgressBar, 1000);
setInterval(updateDisksProgressBar, 10000);