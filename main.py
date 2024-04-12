import machine
import time
import app

def main():
    run = True
    cause = machine.reset_cause()
    if cause == machine.SOFT_RESET:
        print("main() BOOT: soft reset")
        run = False
        # do nothing, drop to REPL
    elif cause == machine.DEEPSLEEP_RESET:
        print("main() BOOT: deep sleep reset")
    elif cause == machine.PWRON_RESET:
        print("main() BOOT: PWRON_RESET") # e.g. machine.PWRON_RESET
        time.sleep(10)
    elif cause == machine.WDT_RESET:
        print("main() BOOT: WDT_RESET")
    elif cause == machine.SOFT_RESET:
        print("main() BOOT: SOFT_RESET, not running App")
        run = False
    elif cause == machine.HARD_RESET:
        print("main() BOOT: HARD_RESET")
    else:
        pass
    if run:
        print("main() Running App")
        from app import App
        mainApp = App()
        mainApp.run()
    else:
        print("main() NOT Running App")


    print("main(): finished")
main()