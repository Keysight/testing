# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# generated using file ./gen/model/dent/system/os/memory.yaml
#
# DONOT EDIT - generated by diligent bots

from dent_os_testbed.discovery.Module import Module
from dent_os_testbed.lib.os.memory_usage import MemoryUsage


class MemoryUsageMod(Module):
    """"""

    def set_memory_usage(self, src, dst):

        for i, memory_usage in enumerate([src]):
            if "mem_total" in memory_usage:
                dst.mem_total = memory_usage.get("mem_total")
            if "mem_free" in memory_usage:
                dst.mem_free = memory_usage.get("mem_free")
            if "mem_available" in memory_usage:
                dst.mem_available = memory_usage.get("mem_available")
            if "buffers" in memory_usage:
                dst.buffers = memory_usage.get("buffers")
            if "cached" in memory_usage:
                dst.cached = memory_usage.get("cached")
            if "swap_cached" in memory_usage:
                dst.swap_cached = memory_usage.get("swap_cached")
            if "active" in memory_usage:
                dst.active = memory_usage.get("active")
            if "inactive" in memory_usage:
                dst.inactive = memory_usage.get("inactive")

    async def discover(self):
        # need to get device instance to get the data from
        #
        for i, dut in enumerate(self.report.duts):
            if not dut.device_id:
                continue
            dev = self.ctx.devices_dict[dut.device_id]
            if dev.os == "ixnetwork" or not await dev.is_connected():
                print("Device not connected skipping memory_usage discovery")
                continue
            print("Running memory_usage Discovery on " + dev.host_name)
            out = await MemoryUsage.show(
                input_data=[{dev.host_name: [{"dut_discovery": True}]}],
                device_obj={dev.host_name: dev},
                parse_output=True,
            )
            if out[0][dev.host_name]["rc"] != 0:
                print(out)
                print("Failed to get memory_usage")
                continue
            if "parsed_output" not in out[0][dev.host_name]:
                print("Failed to get parsed_output memory_usage")
                print(out)
                continue
            self.set_memory_usage(
                out[0][dev.host_name]["parsed_output"], self.report.duts[i].system.os.memory
            )
            print(
                "Finished memory_usage Discovery on {} with {} entries".format(
                    dev.host_name, len(self.report.duts[i].system.os.memory)
                )
            )