from functools import partial

from IPython.display import IFrame


class IFrameRenderer:
    """
    Renders ODD UI to JupiterNotebook through IFrame.

    Example:
        renderer = IFrameRenderer('http://localhost:8080')
    """

    def __init__(self, platform_url: str, width: int = 1024, height: int = 768):
        """IFrame initialization

        Args:
            platform_url (str): ODD platform url
            width (int, optional): IFrame width. Defaults to 1024.
            height (int, optional): IFrame height. Defaults to 768.
        """
        self.__url = f"{platform_url}/embedded"
        self.__draw = partial(IFrame, width=width, height=height)

    def show_overview(self, data_entity_id: int):
        """Show overview page for DataEntity

        Args:
            data_entity_id (int): id of DataEntity

        Returns:
            IFrame: html markup for overview page
        """
        return self.__draw(
            src=f"{self.__url}/dataentities/{data_entity_id}/overview",
        )

    def show_structure(self, data_entity_id: int, structure_version_id: int):
        """Show structure of data entity

        Args:
            data_entity_id (int): DataEntity id
            structure_version_id (int): version id

        Returns:
            IFrame: html markup for overview page
        """
        return self.__draw(
            src=f"{self.__url}/dataentities/{data_entity_id}/structure/{structure_version_id}",
        )

    def show_lineage(self, data_entity_id: int):
        """Show lineage page for DataEntity

        Args:
            data_entity_id (int): DataEntity id

        Returns:
            IFrame: html markup for overview page
        """
        return self.__draw(
            src=f"{self.__url}/dataentities/{data_entity_id}/lineage",
        )

    def show_search_result(self, search_id: int):
        """Show search page

        Args:
            search_id (int): search id

        Returns:
            IFrame: html markup for overview page
        """
        return self.__draw(src=f"{self.__url}/search/{search_id}")
