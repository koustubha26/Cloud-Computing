import logging
import sys
import fileinput
from unittest.mock import patch
from helpers import functions
from helpers import constants
from helpers import config
from helpers import admin
from helpers import server

def run():
    try:
        __data = ""
        __args = functions.parseArguements()
        logging.basicConfig(
            filename='aggiestack-log.txt',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        hw_dict = functions.getData("hw")
        fl_dict = functions.getData("fl")
        im_dict = functions.getData("im")
        rk_dict = functions.getData("rk")
        vm_dict = functions.getData("vm")
        if(__args.cmd == "config"):
            if(__args.hardware):
                config.preprocessHardwareFile(
                    __args.hardware,
                    constants.RK_FILE_NAME, constants.HW_FILE_NAME
                )
                config.readConfigFile(
                    constants.HW_FILE_NAME, constants.HW_FILE_FORMAT, hw_dict
                )
                config.readConfigFile(
                    constants.RK_FILE_NAME, constants.RK_FILE_FORMAT, rk_dict
                )
                config.postprocessRackData(rk_dict)
            if(__args.images):
                config.readConfigFile(
                    __args.images, constants.IM_FILE_FORMAT, im_dict
                )
            if(__args.flavors):
                config.readConfigFile(
                    __args.flavors, constants.FL_FILE_FORMAT, fl_dict
                )
        if(__args.cmd == "show"):
            if(__args.element == "hardware"):
                __data += functions.displayData(
                    hw_dict, 'machine', constants.HW_FILE_FORMAT
                )
            if(__args.element == "images"):
                __data = functions.displayData(
                    im_dict, __args.element, constants.IM_FILE_FORMAT
                )
            if(__args.element == "flavors"):
                __data = functions.displayData(
                    fl_dict, __args.element, constants.FL_FILE_FORMAT
                )
            if(__args.element == "all"):
                __data = functions.displayData(
                    rk_dict, 'rack', constants.RK_FILE_FORMAT
                ) + "\n\n"
                __data += functions.displayData(
                    hw_dict, 'machine', constants.HW_FILE_FORMAT
                ) + "\n\n"
                __data += functions.displayData(
                    im_dict, "images", constants.IM_FILE_FORMAT
                ) + "\n\n"
                __data += functions.displayData(
                    fl_dict, "flavors", constants.FL_FILE_FORMAT
                ) + "\n"
        if(__args.cmd == "admin"):
            if(__args.action == "show"):
                if(__args.element == "hardware"):
                    __data += functions.displayData(
                        hw_dict, 'machine', constants.HW_FILE_FORMAT
                    )
                if(__args.element == "instances"):
                    __data += functions.displayData(
                        vm_dict, 'instance', constants.VM_FILE_FORMAT
                    )
                if(__args.element == "imagecaches"):
                    constants.RK_FILE_FORMAT.append("images")
                    __data += functions.displayData(
                        rk_dict, 'rack', constants.RK_FILE_FORMAT
                    )
            if(__args.action == "add"):
                admin.addMachine(hw_dict, __args)
            if(__args.action == "evacuate"):
                admin.evacuateRack(
                    __args.rack, rk_dict,
                    hw_dict, vm_dict, im_dict, fl_dict
                )
            if(__args.action == "remove"):
                admin.removeMachine(hw_dict, vm_dict, __args.machine)
            if(__args.action == "can_host"):
                if (not hw_dict or not fl_dict):
                    raise AssertionError(
                        'hardware or flavor information not available.'
                    )
                try:
                    __data = admin.canSpawn(
                        hw_dict[__args.machine], fl_dict[__args.flavor]
                    )
                except KeyError as __err:
                    raise __err
        if(__args.cmd == "server"):
            if(__args.action == "create"):
                server.createInstance(
                    rk_dict, hw_dict, fl_dict, im_dict, vm_dict, __args
                )
            if(__args.action == "delete"):
                server.deleteInstance(hw_dict, fl_dict, vm_dict, __args.name)
            if(__args.action == "list"):
                __data = functions.displayData(
                    vm_dict, 'instance', constants.VM_FILE_FORMAT
                )
        functions.storeData(hw_dict, "hw")
        functions.storeData(fl_dict, "fl")
        functions.storeData(im_dict, "im")
        functions.storeData(rk_dict, "rk")
        functions.storeData(vm_dict, "vm")
        print(__data)
        logging.debug("SUCCESS")
    except Exception as __err:
        exc_type, exc_obj, tb = sys.exc_info()
        while(1):
            if not tb.tb_next:
                break
            tb = tb.tb_next
        filename = tb.tb_frame.f_code.co_filename
        linenumber = tb.tb_lineno
        logging.debug(
            "FAILURE - At line %s in %s - %s: %s" % (
                linenumber, filename,
                type(__err).__name__, __err
            )
        )
        print(
            "FAILURE - At line %s in %s - %s: %s" % (
                linenumber, filename,
                type(__err).__name__, __err
            )
        )


if __name__ == "__main__":
    # execute only if run as a script
    try:
        for line in fileinput.input():
            __input = [sys.argv[0]] + line.split()[1::]
            with patch.object(sys, 'argv', __input):
                run()
    except (FileNotFoundError, PermissionError):
        run()
