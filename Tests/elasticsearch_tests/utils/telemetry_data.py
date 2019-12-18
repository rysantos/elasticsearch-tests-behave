"""
Defines the telemetryData class used to read, write, and delete a list of uuid's from an elastic serach index
"""
from elasticsearch_dsl import Text, Document, Search, Index
from typing import List


class TelemetryData(Document):
    """Facade for common Telemetry Data operations built on top of elastic search API"""
    uuid = Text()


def delete_uuids(uuids: List[str], index: str):
    """Delete all uuids in list from specified index

        Args:
            uuids: The list of uuids to delete from the index
            index: Name of the index from which to delete 
    """

    Search(index=index).query(
        "match", uuid=' '.join(uuids)).delete()


def upsert_index(index_name: str):
    """Create the index with the given name if it does not exists

        Args: 
            index_name: Name of the index to create
    """

    i = Index(index_name)
    i.save()


def get_uuids(uuids: List[str], index: str) -> List[str]:
    """Retrieves the specified uuids in the list from the elastic search cluster

        Args:
            uuids: uuids to retrieve from elastic search cluster
            index: Index in which to search for uuids

        Returns:
            A list of uuid strings found which match the search uuids 
    """
    lst = Search(index=index).query(
        "match", uuid=' '.join(uuids)).execute(ignore_cache=True)

    return [dbuuid.uuid for dbuuid in lst]
