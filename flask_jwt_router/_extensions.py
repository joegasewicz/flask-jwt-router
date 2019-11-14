class _Extensions:
    """
    :param secret_key: Defaults to `DEFAULT_SECRET_KEY`
    :param entity_key: The name of the model's entity attribute
    :param whitelist_routes: List of tuple pairs of verb & url path
    :param api_name: the api name prefix e.g `/api/v1`
    :param ignored_routes: Opt our routes from api name prefixing
    """
    def __init__(self,
                 secret_key=None,
                 entity_key="id",
                 whitelist_routes=None,
                 api_name=None,
                 ignored_routes=None
                 ):

        self.secret_key = secret_key
        self.entity_key = entity_key
        self.whitelist_routes = whitelist_routes
        self.api_name = api_name
        self.ignored_routes = ignored_routes

