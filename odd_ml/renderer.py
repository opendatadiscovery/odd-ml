from functools import partial

from IPython.display import IFrame


class IFrameRenderer:
    def __init__(self, platform_url: str, width: int = 1024, height: int = 768):
        self.embedded_url = f"{platform_url}/embedded"
        self.__draw = partial(IFrame, width=width, height=height)

    def show_overview(self, data_entity_id: int):
        return self.__draw(
            src=f"{self.embedded_url}/dataentities/{data_entity_id}/overview",
        )

    def show_structure(self, data_entity_id: int, structure_version_id: int):
        return self.__draw(
            src=f"{self.embedded_url}/dataentities/{data_entity_id}/structure/{structure_version_id}",
        )

    def show_lineage(self, data_entity_id: int):
        return self.__draw(
            src=f"{self.embedded_url}/dataentities/{data_entity_id}/lineage",
        )

    def show_search_result(self, search_id: int):
        return self.__draw(src=f"{self.embedded_url}/search/{search_id}")
