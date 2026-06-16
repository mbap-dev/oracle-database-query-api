from flask import Flask, jsonify, request
import oracledb
import os

app = Flask(__name__)

oracledb.init_oracle_client(lib_dir="/usr/lib/oracle/instantclient")

def conectar_oracle(dsn_tns=None, usuario=None, senha=None):
    dsn_tns = dsn_tns or f"{os.getenv('ORACLE_HOST')}:{os.getenv('ORACLE_PORT')}/{os.getenv('ORACLE_SERVICE_NAME')}"
    usuario = usuario or os.getenv('ORACLE_USER')
    senha = senha or os.getenv('ORACLE_PASSWORD')
    
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
    dsn_tns = data.get('dsn_tns')
    usuario = data.get('usuario')
    senha = data.get('senha')
    
    if not query:
        return jsonify({"erro": "Parâmetro 'query' é obrigatório"}), 400
    
    conn = conectar_oracle(dsn_tns, usuario, senha)
    
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

@app.route('/procedure', methods=['POST'])
def executar_procedure():
    data = request.get_json()
    nome = data.get('procedure')
    parametros = data.get('parametros', [])
    out_params = data.get('out_params', [])
    dsn_tns = data.get('dsn_tns')
    usuario = data.get('usuario')
    senha = data.get('senha')

    if not nome:
        return jsonify({"erro": "Parâmetro 'procedure' é obrigatório"}), 400

    if not isinstance(parametros, list):
        return jsonify({"erro": "Parâmetro 'parametros' deve ser uma lista"}), 400

    if not isinstance(out_params, list):
        return jsonify({"erro": "Parâmetro 'out_params' deve ser uma lista"}), 400

    conn = conectar_oracle(dsn_tns, usuario, senha)

    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco Oracle"}), 500

    cursor = conn.cursor()
    try:
        # Mapeia os tipos suportados para parâmetros de saída (OUT)
        tipos = {
            "number": oracledb.NUMBER,
            "string": oracledb.STRING,
            "cursor": oracledb.CURSOR,
            "date": oracledb.DATETIME,
        }

        # Monta a lista de argumentos: entradas + variáveis de saída
        args = list(parametros)
        out_vars = []
        for op in out_params:
            tipo = tipos.get(str(op.get("tipo", "string")).lower(), oracledb.STRING)
            var = cursor.var(tipo)
            out_vars.append((op.get("nome"), tipo, var))
            args.append(var)

        cursor.callproc(nome, args)
        conn.commit()

        # Coleta os valores de saída
        saida = {}
        for idx, (nome_out, tipo, var) in enumerate(out_vars):
            chave = nome_out or f"out_{idx}"
            valor = var.getvalue()
            if tipo == oracledb.CURSOR and valor is not None:
                colunas = [col[0] for col in valor.description]
                saida[chave] = [dict(zip(colunas, linha)) for linha in valor.fetchall()]
            else:
                saida[chave] = valor

        return jsonify({"resultado": saida}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)