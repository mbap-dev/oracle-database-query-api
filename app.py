from flask import Flask, jsonify, request
import oracledb
import os

app = Flask(__name__)


oracledb.init_oracle_client(lib_dir="/usr/lib/oracle/instantclient")



dsn_tns = f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE_NAME')}"
usuario = os.getenv('ORACLE_USER')
senha = os.getenv('ORACLE_PASSWORD')


def conectar_oracle():
    try:
        conn = oracledb.connect(user=usuario, password=senha, dsn=dsn_tns, mode=oracledb.DEFAULT_AUTH)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return None

@app.route('/consulta', methods=['POST'])
def consulta_oracle():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({"erro": "Parâmetro 'query' é obrigatório"}), 400
    
    conn = conectar_oracle()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco Oracle"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        colunas = [col[0] for col in cursor.description]  # Pega os nomes das colunas
        dados = [dict(zip(colunas, linha)) for linha in resultado]
        
        return jsonify(dados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
