import notpywinsparkle
import os
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
    update_url = "https://raw.githubusercontent.com/K1K3-08/Format-Tool/refs/heads/main/sparklecast.xml"
    notpywinsparkle.win_sparkle_set_appcast_url(update_url)
    notpywinsparkle.win_sparkle_set_app_details("KikeH", "Format-Tool", "0.2.0")

    if os.path.isfile('eddsa_pub.pem'):
        with open('eddsa_pub.pem', 'r') as file:
            pub_key = file.read()
        notpywinsparkle.win_sparkle_set_eddsa_public_key(pub_key)

    # initialize
    notpywinsparkle.win_sparkle_init()

    # check for updates
    #notpywinsparkle.win_sparkle_check_update_with_ui()

    # alternatively you could check for updates in the 
    # background silently
    notpywinsparkle.win_sparkle_check_update_without_ui()

    # dont do it this way, just an example to keep the thread running
    while True:
        time.sleep(1)
