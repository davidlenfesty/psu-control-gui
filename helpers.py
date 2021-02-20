import universal_usbtmc
import os

if not os.environ.get("USBTMC_BACKEND"):
    os.environ["USBTMC_BACKEND"] = "linux_kernel"

def usbtmc_backend():
    return universal_usbtmc.import_backend(os.environ["USBTMC_BACKEND"])
