"""MSSQL target class."""
from pathlib import Path
from typing import List
from .singer_sdk.target import Target
from .streams import MSSQLStream
import pyodbc 

#STREAM_TYPES = [
#  MSSQLStream,
#]  
class TargetMSSQL(Target):
  """MSSQL tap class."""
  name = "target-mssql"

  def __init__(self, config, *args, **kwargs):
    super().__init__(config, *args, **kwargs)
    assert self.config["host"]
    # print(pyodbc.drivers()) #https://towardsdatascience.com/using-odbc-to-connect-any-database-directly-to-jupyter-notebook-19741b4b748
    driver = self.config.get("driver", "{MariaSQL}")
    server = self.config["host"]
    port = str(self.config.get("port", 3306))
    if (self.config.get("trusted_connection")=="yes"):
        self.conn = pyodbc.connect( driver=driver,
                                    server=server,
                                    trusted_connection=self.config.get("trusted_connection"),
                                    database=self.config.get("database"),
                                    )
    else:
        self.conn = pyodbc.connect( driver=driver,
                                    server=server,
                                    port=port,
                                    uid=self.config.get("user"),
                                    pwd=self.config.get("password"),
                                    database=self.config.get("database"),
                                    )
    self.conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    self.conn.setencoding(encoding='utf-8', ctype=pyodbc.SQL_CHAR)
    self.conn.setencoding(encoding='utf-8')

  #TODO not a fan of streams not being required by the BaseTarget class here, as it's referenced in the class
  def streams(self):
    return self.streamslist 
    #return [stream_class(target=self) for stream_class in STREAM_TYPES]
  
  #TODO this is a silly way to do this
  def streamclass(self, *args, **kwargs):
    schema=self.config.get("schema")
    batch_size=self.config.get("batch_size")
    return MSSQLStream(conn=self.conn, schema_name=schema, batch_size=batch_size,*args, **kwargs)
# CLI Execution:

cli = TargetMSSQL.cli()
