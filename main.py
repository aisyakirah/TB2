import mysql.connector
import logging
from http.client import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#a
class Buku:
    def __init__(self, judul, penulis, penerbit, tahun_terbit, konten, iktisar):
        self.judul = judul
        self.penulis = penulis
        self.penerbit = penerbit
        self.tahun_terbit = tahun_terbit
        self.konten = konten
        self.iktisar = iktisar

    def read(self, halaman_awal, halaman_akhir):
        if halaman_awal <= len(self.konten) and halaman_akhir <= len(self.konten):
            for i in range(halaman_awal, halaman_akhir + 1):
                print(f"Halaman {i}: {self.konten[i - 1]}")
        else:
            print("Nomor halaman tidak valid.")

    def __str__(self):
        return f"{self.judul} by {self.penulis}"
    
#c
class BukuDatabase:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor(dictionary=True)
    
    def get_buku_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM buku WHERE id = %s", (id,))
            result = self.cursor.fetchone()
            if result:
                return Buku(
                    judul=result['judul'], 
                    penulis=result['penulis'], 
                    penerbit=result['penerbit'], 
                    tahun_terbit=result['tahun_terbit'], 
                    konten=result['konten'].split('\n'), 
                    iktisar=result['iktisar']
                )
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

#d
def post_buku(self, buku):
        cnx = mysql.connector.connect(**self.db_config)
        cursor = cnx.cursor()

        query = "INSERT INTO buku (judul, penulis, konten, penerbit, tahun_terbit, iktisar) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            buku.judul,
            buku.penulis,
            buku.konten,
            buku.penerbit,
            buku.tahun_terbit,
            buku.iktisar
        ))

        cnx.commit()
        cursor.close()
        cnx.close()

#e
class BukuDatabase:
    def __init__(self, host, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor(dictionary=True)
            logger.info("Database connection established")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            raise HTTPException(f"Cannot connect to database: {err}")

    def get_buku_by_id(self, id):
        try:
            self.cursor.execute("SELECT * FROM buku WHERE id = %s", (id,))
            result = self.cursor.fetchone()
            if result:
                logger.info(f"Buku with ID {id} fetched successfully")
                return Buku(
                    judul=result['judul'], 
                    penulis=result['penulis'], 
                    penerbit=result['penerbit'], 
                    tahun_terbit=result['tahun_terbit'], 
                    konten=result['konten'].split('\n'), 
                    iktisar=result['iktisar']
                )
            else:
                logger.warning(f"No Buku found with ID {id}")
                return None
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
            return None

    def save_buku(self, buku):
        try:
            query = """
            INSERT INTO buku (judul, penulis, penerbit, tahun_terbit, konten, iktisar)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (buku.judul, buku.penulis, buku.penerbit, buku.tahun_terbit, '\n'.join(buku.konten), buku.iktisar))
            self.conn.commit()
            logger.info(f"Buku '{buku.judul}' by {buku.penulis} saved successfully")
        except mysql.connector.Error as err:
            logger.error(f"Error: {err}")
    
    def close(self):
        self.cursor.close()
        self.conn.close()
        logger.info("Database connection closed")