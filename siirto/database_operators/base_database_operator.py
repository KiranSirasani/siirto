from siirto.shared.enums import LoadType
from siirto.base import Base
from typing import List


class BaseDataBaseOperator(Base):
    """
    Abstract base class for all database operators.
    To derive this class, you are expected to override the constructor as well
    as the 'execute' method.

    Operators derived from this class should perform following steps:
    1. implement the execute method
        a. implement the full load
        b. implement the CDC
        c. handle the fail-overs
        d. persist the state

    :param connection_string: connection string for the database
    :type connection_string: str
    :param load_type: type of load to run for the job. LoadType.Full_Load,
        LoadType.CDC or LoadType.Full_Load_And_CDC
    :type connection_string: LoadType
    :param table_names: tables which needs to be considered
    :type table_names: List[str]
    :param full_load_plugin_name: name of full load plugin to be used in execute
    :type full_load_plugin_name: str
    :param cdc_plugin_name: name of cdc plugin to be used in execute
    :type cdc_plugin_name: str
    :param output_location: output location for the full load and cdc
    :type output_location: str
    """

    # operator type for the operator
    operator_type = None
    # operator name, which will go in configuration
    operator_name = None

    def __init__(self,
                 connection_string: str,
                 load_type: LoadType = LoadType.Full_Load_And_CDC,
                 table_names: List[str] = [],
                 full_load_plugin_name: str = None,
                 cdc_plugin_name: str = None,
                 output_location: str = None,
                 *args,
                 **kwargs):
        self.connection_string = connection_string
        self.load_type = load_type
        self.full_load_plugin_name = full_load_plugin_name
        self.cdc_plugin_name = cdc_plugin_name
        self.table_names = table_names or []
        self.output_location = output_location
        super().__init__(*args, **kwargs)
        self._validate_and_sanitize_input_parameters()

    def _validate_and_sanitize_input_parameters(self) -> None:
        """
        Validates the input parameters.
        Only validate connection string and load type.
        input and output plugins will be validated in corresponding operator
        """
        if len(self.connection_string.strip()) == 0:
            raise ValueError("Empty value provided for connection string")
        if len(self.output_location.strip()) == 0:
            raise ValueError("Empty value provided for output location")
        if (self.load_type is not None and type(self.load_type) is not LoadType) \
                or self.load_type is None:
            raise ValueError(f"Incorrect value provided for load type {self.load_type}")
        if not isinstance(self.table_names, list):
            raise ValueError(f"Table names `{self.table_names}` should be list or None")

    def execute(self):
        """
        This is the main method to derive when implementing an operator.
        """
        raise NotImplementedError()