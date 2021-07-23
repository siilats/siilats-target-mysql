# target-mysql

`target-mysql` is a Singer tap for MySQL based on the code from MSSQL target and ODBC.
I only have it tested for mariadb on mac
1. brew install mariadb
2. brew services list
3. brew start mariadb
4. recommend changing root password to root (empty pw is not supported well)
5. recommend testing your connection in pycharm
   if the connection doesn't start (mac):  
   ```
   more ~/Library/LaunchAgents/homebrew.mxcl.mariadb.plist 
   cd /usr/local/var/mysql
   ls -la
   tail -1000 *-MacBook-Pro.local.err
   ps axw|grep mysql
   sudo pkill mysql
   ```
6. Download  
   a. with brew: https://github.com/davidski/database_connections  
   ```
   brew install mariadb-connector-odbc --force
   vi /usr/local/etc/odbcinst.ini
   
   [MariaSQL]
   Driver = /usr/local/Cellar/mariadb-connector-odbc/3.1.13/lib/mariadb/libmaodbc.dylib
   
   ```
   b.  manual download
   * https://downloads.mariadb.org/connector-odbc/
   * https://downloads.mariadb.com/Connectors/odbc/connector-odbc-3.1.13/mariadb-connector-odbc-3.1.13-osx-x86_64.pkg
   * https://mariadb.com/kb/en/creating-a-data-source-with-mariadb-connectorodbc/#creating-a-data-source-with-mariadb-connectorodbc-on-mac-os-x
   * http://www.iodbc.org/dataspace/doc/iodbc/wiki/iodbcWiki/Downloads#Mac%20OS%20X
   * Dont download the obvious:
https://sourceforge.net/projects/iodbc/files/iodbc/3.52.15/iODBC-SDK-3.52.15-macOS11.dmg/download
   * But download from github the latest:
   * https://github.com/openlink/iODBC/blob/develop/README_MACOSX.md  
      `vi /Library/ODBC/odbc.ini`
     
        ```
        [ODBC Data Sources]  
        CData SSAS Sys = CData ODBC Driver for SQL Server Analysis Services   
        MariaDB-server = MariaDB ODBC 3.1 Driver
        ```
        then add
        ```
        [MariaDB-server]
        Description = MariaDB server
        Driver = /Library/MariaDB/MariaDB-Connector-ODBC/libmaodbc.dylib
        SERVER=localhost
        USER=root
        PASSWORD=root
        DATABASE=mysql
        PORT=3306
        ```
   * if everything works you should be able to run:  
     `/usr/local/iODBC/bin/iodbctest "DSN=MariaDB-server"`
   * ODBC config is a mess, there are several .ini files with confusing names, driver names have 
   sometimes Unicode in them sometimes not, there are several dylib files that are not
     in standard paths etc. Try these links
     * https://snowflakecommunity.force.com/s/article/How-to-configure-Excel-on-MacOS-to-use-Snowflake-using-ODBC-driver
     * https://github.com/openlink/iODBC/blob/develop/README_MACOSX.md
     * http://www.odbcmanager.net/
     * https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX
     * https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-MySQL
     * https://towardsdatascience.com/using-odbc-to-connect-any-database-directly-to-jupyter-notebook-19741b4b748
    
7. clone `target-mysql` to a local folder and 
   add this to meltano.yml (or install from github and edit target)
```
  - name: target-mysql
    namespace: target_mysql
    pip_url: ../autoidm-target-mssql
    executable: target-mssql
    config:
      host: localhost
      port: 3306
      database: test
      user: root
      password: root
```
8. run
`meltano add --custom loader target-mysql`
9. configure tap-posgres or another tap
10. run
`meltano elt tap-postgres target-mysql`


Build with the [Singer SDK](https://gitlab.com/meltano/singer-sdk).

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install target-mssql
```

## Configuration

### Accepted Config Options
```
host: Hostname (example: localhost)
port: example: 1433
database:
user:
password:
trusted_connection: yes # Will use windows authentication 
schema (Optional): will default to whatever the user's default schema is set to if this isn't set
batch_size (Optional): Will default to 10000
A full list of supported settings and capabilities for this
tap is available by running:
```

```bash
target-mysql --about
```

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `target-mssql` by itself or in a pipeline using [Meltano](www.meltano.com).

### Executing the Tap Directly

```bash
target-mssql --version
target-mssql --help
target-mssql --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_mssql/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `target-mssql` CLI interface directly using `poetry run`:

```bash
poetry run target-mssql --help
```

### Testing with [Meltano](meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-mssql
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-mssql --version
# OR run a test `elt` pipeline:
meltano etl target-mssql target-jsonl
```

### Singer SDK Dev Guide

See the [dev guide](../../docs/dev_guide.md) for more instructions on how to use the Singer SDK to 
develop your own taps and targets.
