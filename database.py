import psycopg2

def koneksi():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="db_mahasiswa",
        user="postgres",
        password="postgres"
    )