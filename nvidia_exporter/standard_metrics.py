from pynvml import *
from prometheus_client import Gauge

from .metric import Metric


def register_standard_metrics():
    Gauge('nvidia_device_count', 'Number of compute devices in the system')\
        .set_function(lambda: int(nvmlDeviceGetCount()))

    metrics = [
        Metric('gpu_temp_degC',
               'GPU Temperature (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperature(h, NVML_TEMPERATURE_GPU)),
        Metric('mem_total_bytes',
               'Total installed FB memory (in  bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).total),
        Metric('mem_free_bytes',
               'Unallocated FB memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).free),
        Metric('mem_used_bytes',
               'Allocated FB memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).used),
        Metric('shutdown_temp_degC',
               'Shutdown temperature threshold (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperatureThreshold(h, 0)),
        Metric('slowdown_temp_degC',
               'Slowdown temperature threshold (in degrees Celsius)',
               lambda h: nvmlDeviceGetTemperatureThreshold(h, 1)),
        Metric('process_count',
               'Number of running compute processes',
               lambda h: len(nvmlDeviceGetComputeRunningProcesses(h))),
        Metric('gpu_util',
               'Percent of time over the past sample period during which one or more kernels was executing on the GPU',
               lambda h: nvmlDeviceGetUtilizationRates(h).gpu),
        Metric('mem_util',
               'Percent of time over the past sample period during which global (device) memory was being read or written',
               lambda h: nvmlDeviceGetUtilizationRates(h).memory),

	Metric('cpu_util',
               'Percent of time over the past sample period during which one or more kernels was executing on the CPU',
               lambda h: nvmlDeviceGetUtilizationRates(h).memory),
	Metric('mem_total_bytes',
               'Total installed FB memory (in  bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).total),
        Metric('mem_free_bytes',
               'Unallocated memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).free),
        Metric('mem_used_bytes',
               'Allocated memory (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).used),
	Metric('storage_total_bytes',
               'Total installed storage (in  bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).total),
        Metric('storage_free_bytes',
               'Unallocated storage (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).free),
        Metric('storage_used_bytes',
               'Allocated storage (in bytes)',
               lambda h: nvmlDeviceGetMemoryInfo(h).used),
	Metric('network_in',
		'Total Bytes Received Across Network Interfaces (in bytes)',
		lambda h: nvmlDeviceGetMemoryInfo(h).used),
	Metric('network_out',
		'Total Bytes Transfered Across Network Interfaces (in bytes)',
		lambda h: nvmlDeviceGetMemoryInfo(h).used)
	]

    device_count = int(nvmlDeviceGetCount())
    for device_index in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(device_index)
        name = nvmlDeviceGetName(handle)

        for metric in metrics:
            metric.metric_for(name, device_index, handle)
