import notpywinsparkle
import time
import sys

def no_update_found():
    """ when no update has been found, close the updater"""
    print("No update found")
    print("Setting flag to shutdown PassagesUpdater")


def found_update():
    """ log that an update was found """
    print("New Update Available")


def encountered_error():
    print("An error occurred")


def update_cancelled():
    """ when the update was cancelled, close the updater"""
    print("Update was cancelled")
    print("Setting flag to shutdown PassagesUpdater")


def shutdown():
    """ The installer is being launched signal the updater to shutdown """
    sys.exit(0)
    # actually shutdown the app here
    print("Safe to shutdown before installing")


def sparkle():

    # register callbacks
    notpywinsparkle.win_sparkle_set_did_find_update_callback(found_update)
    notpywinsparkle.win_sparkle_set_error_callback(encountered_error)
    notpywinsparkle.win_sparkle_set_update_cancelled_callback(update_cancelled)
    notpywinsparkle.win_sparkle_set_did_not_find_update_callback(no_update_found)
    notpywinsparkle.win_sparkle_set_shutdown_request_callback(shutdown)

    # set application details
    update_url = "https://k1k3-08.github.io/Format-Tool/sparklecast.xml"
    notpywinsparkle.win_sparkle_set_appcast_url(update_url)
    APP_VERSION = "0.3.1"  # or read from a file or constant
    notpywinsparkle.win_sparkle_set_app_details("KikeH", "Format-Tool", APP_VERSION)

    
    notpywinsparkle.win_sparkle_set_eddsa_public_key("xwpakLMxVqP+juQ/MUmebiQPPuFwLTohmE6WIQBpOb8=")

    # initialize
    notpywinsparkle.win_sparkle_set_automatic_check_for_updates(True)
    notpywinsparkle.win_sparkle_init()

    # check for updates
    notpywinsparkle.win_sparkle_check_update_without_ui()

    # alternatively you could check for updates in the 
    # background silently
    #notpywinsparkle.win_sparkle_check_update_without_ui()

    # dont do it this way, just an example to keep the thread running
    while True:
        time.sleep(1)