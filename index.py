import random
from faker import Faker
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta

fake = Faker()

config = {
  'user': '',
  'password': '',
  'host': '',
  'database': ''
}


try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS exemplo (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), data DATE)")


    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 12, 31)


    for i in range(10):
        data = start_date + timedelta(days=random.randint(0, 364))
        nome = fake.name()
        query = "INSERT INTO exemplo (data, nome) VALUES (%s, %s)"
        values = (data, nome)
        cursor.execute(query, values)
        cnx.commit()

    query = """
    SELECT MAX(data) AS last_date_of_month, nome
    FROM exemplo
    WHERE data <= LAST_DAY(data)
    GROUP BY YEAR(data), MONTH(data);
    """

    cursor.execute(query)

    for (last_date_of_month, name_column) in cursor:
        print(f"Última data de {name_column} no mês: {last_date_of_month}")

    
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erro: Nome de usuário ou senha incorretos")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Erro: Banco de dados não existe")
    else:
        print(err)


