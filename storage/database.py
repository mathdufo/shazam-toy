from collections import defaultdict
import sqlite3

from common.settings import DEFAULT_DB_PATH

class database:
    def __init__(self, path=DEFAULT_DB_PATH):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        if not self._table_exist("audio_hashes"):
            self._create_table("audio_hashes", "hash TEXT, timestamp REAL, id TEXT")

        if not self._table_exist("audio_info"):
            self._create_table("audio_info", "id TEXT, info TEXT")

        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_audio_hashes ON audio_hashes (hash)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_audio_info ON audio_info (id)")

    def insert(self, hashes, timestamps, id, info):
        ids = [id for i in hashes]

        sql = "INSERT INTO audio_hashes (hash, timestamp, id) VALUES (?,?,?)"
        self.cursor.executemany(sql, zip(hashes, timestamps, ids))
        
        sql = "INSERT INTO audio_info (id, info) VALUES (?,?)"
        self.cursor.execute(sql, (id, info))

        self.connection.commit()
    
    def search_info(self, ids):
        sql = f"SELECT info FROM audio_info WHERE id IN ({','.join(['?']*len(ids))})"
        self.cursor.execute(sql, ids)

        return self.cursor.fetchall()     

    def search_hashes(self, hashes, timestamps):
        sql = f"SELECT hash, timestamp, id FROM audio_hashes WHERE hash IN ({','.join(['?']*len(hashes))})"
        self.cursor.execute(sql, hashes)

        hashes_offsets_map = {}
        for hash, timestamp in list(zip(hashes, timestamps)):
            hashes_offsets_map[hash] = timestamp

        results = defaultdict(list)
        for hash, timestamp, id in self.cursor:
            results[id].append(timestamp - hashes_offsets_map[hash])

        return results

    def _table_exist(self, table_name):
        sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        tables = self.cursor.execute(sql).fetchall()

        return len(tables) > 0
    
    def _create_table(self, name, attributes):
        sql = f"CREATE TABLE IF NOT EXISTS {name} ({attributes});"
        self.cursor.execute(sql)
        self.connection.commit()