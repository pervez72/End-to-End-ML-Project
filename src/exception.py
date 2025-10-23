import sys
import logging  # custom logging module import (তুমি src/logger.py এ log configuration রাখবে)

# এই function টি detailed error message তৈরি করে
def error_message_detail(error, error_detail: sys):
    # exc_info() থেকে traceback object পাওয়া যায় (type, value, traceback)
    _, _, exc_tb = error_detail.exc_info()

    # traceback থেকে error ঘটার file name নেওয়া
    file_name = exc_tb.tb_frame.f_code.co_filename

    # formatted error message তৈরি করা
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name,               # যেখানে error ঘটেছে
        exc_tb.tb_lineno,        # কোন line এ ঘটেছে
        str(error)               # আসল error message
    )

    return error_message


# Custom exception class তৈরি করা
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        # parent Exception class কে initialize করা
        super().__init__(error_message)

        # detailed error message তৈরি ও save করা
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    # যখন exception print করা হয়, তখন এই function call হয়
    def __str__(self):
        return self.error_message

