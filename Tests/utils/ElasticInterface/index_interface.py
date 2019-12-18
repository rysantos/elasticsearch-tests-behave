"""
Defines a class and functions used to interact with an Elastic search index
"""
from elasticsearch_dsl import Text, Document, Search, Index
import datetime

class IndexInterface():
    """Facade for Elastic operations built on top of elastic search API"""

    def __init__(self, _index: str, _timeRange = "30s"):
        """
        Args:
            index: The index requested.
            timeRange: Time Range to search the index. 
        """
        self.index = _index
        self.timeRange = _timeRange

    def get_logs(self):
        """Retrieves the logs from the elastic search cluster given the index

            Args:

            Returns:
                A list of logs found in the elastic search cluster 
        """
        s = Search(index=self.index).filter('range', **{'@timestamp': {'gte':'now-'+ self.timeRange,'lt':'now' }}).sort('-@timestamp')
        lst = self.construct_results(s)
        return lst

    def construct_results(self, query):
        """Pages through the search results and constructs a list of documents to return
            Args:
                query: The query to execute
            Returns:
                A list of documents in the respnse object
        """
        lst = list()
        response = query.execute(ignore_cache=True)
        count = 0
        totalHits = query.count().value
        offset = 10
        while count < totalHits:
            query = query[count:count+offset]
            tmp = query.execute(ignore_cache=True)
            for hit in tmp:
                lst.append(hit)
            count = len(lst)
        return lst

    def get_topTwoLogs(self):
        """Retrieves the top two logs from the elastic search cluster given the specified index

            Args:

            Returns:
                Two logs found in the elast search cluster 
        """
        temp = self.get_logs()
        lst = list()
        lst.append(temp[0])
        lst.append(temp[1])
        return lst
    
    def get_LatestLog(self):
        """Retrieves the latest log from the elastic search cluster

            Args:

            Returns:
                One logs found in the elast search cluster 
        """
        lst = self.get_logs()
        return lst[0]
