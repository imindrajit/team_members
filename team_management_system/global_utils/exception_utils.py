class ExceptionUtils:
    @staticmethod
    def get_error_message(ex):
        error_msg = None
        try:
            error_msg = ex.message
        except Exception:
            error_msg = ex['message']
        if not error_msg and len(ex.args) == 2:
            error_msg = ex.args[-1]
        return error_msg