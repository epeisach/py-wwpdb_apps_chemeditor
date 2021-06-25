import sys

from wwpdb.apps.chemeditor.webapp.Utils import setupLog
from wwpdb.utils.db.MyConnectionBase import MyConnectionBase

class DaInternalCombineDb(object):
    def __init__(self, siteId=None, verbose=False, log=sys.stderr):
        self._mydb = None
        self._siteId = siteId
        self._open()
        self.logger = setupLog(verbose, log)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._close()

    def __del__(self):
        self._close()

    def _open(self):
        """Open db connection

        Returns:
            DaInternalCombineDb: instance of this class
        """
        self._mydb = MyConnectionBase(siteId=self._siteId)
        self._mydb.setResource(resourceName="DA_INTERNAL_COMBINE")

        ok = self._mydb.openConnection()

        if not ok:
            self.logger.error("Could not open resource connection to DA_INTERNAL_COMBINE")
            self._mydb = None
            return False

        return True

    def _close(self):
        if self._mydb:
            self._mydb.closeConnection()
            self._mydb = None
    
    def getEntriesWithLigand(self, ccId):
        """Get entries in pdbx_entity_nonpoly table that
        have a given ligand.

        Args:
            ccId (str): ligand id

        Returns:
            list: list containing entries (dep ids) containing the ligid
        """
        query = "select Structure_ID from pdbx_entity_nonpoly where comp_id = %s"
        
        self.logger.debug("querying entries with ligand %s", ccId)

        cursor = self._mydb.getCursor()
        cursor.execute(query, (ccId,))

        rows = cursor.fetchall()

        self.logger.info("got %s entries with ligand %s", len(rows), ccId)

        depIds = []
        for r in rows:
            depIds.append(r[0])

        return depIds

if __name__ == '__main__':
    with DaInternalCombineDb() as db:
        db.getEntriesWithLigand('AAA')