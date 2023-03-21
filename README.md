# TSV-to-SQL-Tool
TSV-to-SQL-Tool is a simple command line program that allows you to easily migrate data from TSV files to a MariaDB database.

## Program works in 2 modes:
- Add data from .TSV to SQL: 

  Just connect to database, choose your .TSV file and wait till records are added. Records that weren't added will be stored offline.
- Add fixed data: 

  When there is a data that had bad syntax or whetever it is stored offline as file. You can check what is wrong with it and fix it. Then use this option and programm will add all remaining data without errors.
