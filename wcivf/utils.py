class NoOpOutputWrapper:
    """
    Used in place of django.core.management.base.OutputWrapper
    to support quiet mode in mgmt commands.
    """

    def write(self, *args):
        pass
