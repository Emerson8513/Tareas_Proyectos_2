pkg load database

conn = pq_connect(setdbopts("dbname", "postgres", "host", "localhost", "port", "5432", "user", "postgres", "password", "kuto"));

N = pq_exec_params(conn,'select * from redes;')
