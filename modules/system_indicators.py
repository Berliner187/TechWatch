import psutil
import platform


class SystemIndicators:
    @staticmethod
    def os_info():
        return f"{platform.system()} {platform.release()}"

    @staticmethod
    def cpu_info():
        return psutil.cpu_percent(interval=1, percpu=True)

    @staticmethod
    def memory_info():
        memory = psutil.virtual_memory()
        memory_use = round(memory.used / 1024 / 1024 / 1024, 2)
        memory_total = round(memory.total / (1024 ** 3), 2)

        memory_indicators_dict = {
            "total_memory": memory_total,
            "memory_usage": memory_use,
            "memory_percent": memory.percent
        }

        return memory_indicators_dict

    @staticmethod
    def disks_info():
        """
            Информация о дисках
            disk_title - краткая информация о диске
            :return: {total_size, free_size, occupied, used_percent, disk_title}
            """

        def get_conversion(total_size, free_size):
            """
                Конверсия из байтов в гигабайты
            """
            _size_gb = total_size / 1024 / 1024 / 1024
            _free_gb = free_size / 1024 / 1024 / 1024
            _occupied_gb = _size_gb - _free_gb
            return _size_gb, _free_gb, _occupied_gb

        disk_partitions = psutil.disk_partitions()
        disks_array = []
        disks_indicators_dict = {}
        for partition in disk_partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            used_percent = usage.percent

            size_gb, free_gb, occupied_gb = get_conversion(usage.total, usage.free)
            disks_indicators_dict['total_size'] = size_gb
            disks_indicators_dict['free_size'] = free_gb
            disks_indicators_dict['occupied'] = occupied_gb
            disks_indicators_dict['used_percent'] = used_percent

            disk_title = f"{partition.device} {occupied_gb:.2f} GB/{size_gb:.2f} GB ({used_percent}%)"
            disks_indicators_dict['disk_title'] = disk_title

            disks_array.append(disks_indicators_dict)
            disks_indicators_dict = {}

        return disks_array

    def get_system_indicators(self):
        return {
            "info_os": self.os_info(),
            "info_cpu": self.cpu_info(),
            "info_memory": self.memory_info(),
            "info_disks": self.disks_info(),
        }
