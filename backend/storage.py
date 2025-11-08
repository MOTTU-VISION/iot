import os
import json
import oracledb
import threading
from datetime import datetime
from dotenv import load_dotenv

# Lendo variáveis de ambiente
load_dotenv()

_lock = threading.Lock()

# Configuração da conexão Oracle
def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")  # Ex: "localhost:1521/XE"
    )

# ----------------------------
# REGISTROS DE CÂMERAS
# ----------------------------
def save_record(camera_id, records):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()

            for record in records:
                placa = record["placa"]

                # Verifica se já existe um registro dessa placa
                cur.execute("""
                    SELECT COUNT(*) FROM registros
                    WHERE placa = :placa
                """, {"placa": placa})
                exists = cur.fetchone()[0] > 0

                if exists:
                    # Atualiza o registro existente
                    cur.execute("""
                        UPDATE registros
                        SET camera_id = :camera_id,
                            timestamp = :timestamp,
                            bounding_box = :bbox,
                            label = :label
                        WHERE placa = :placa
                    """, {
                        "camera_id": camera_id,
                        "timestamp": record["timestamp"],
                        "bbox": json.dumps(record["bounding_box"]),
                        "label": record["label"],
                        "placa": placa
                    })
                else:
                    # Insere novo registro
                    cur.execute("""
                        INSERT INTO registros (camera_id, placa, timestamp, bounding_box, label)
                        VALUES (:camera_id, :placa, :timestamp, :bbox, :label)
                    """, {
                        "camera_id": camera_id,
                        "placa": placa,
                        "timestamp": record["timestamp"],
                        "bbox": json.dumps(record["bounding_box"]),
                        "label": record["label"]
                    })
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def load_records(camera_id):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                    SELECT placa, timestamp, bounding_box, label 
                    FROM registros WHERE camera_id = :id"""
                    , {"id": camera_id})
            rows = cur.fetchall()
            return [
                {
                    "camera_id": camera_id,
                    "placa": r[0],
                    "timestamp": r[1],
                    "bounding_box": json.loads(r[2]),
                    "label": r[3]
                }
                for r in rows
            ]
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def delete_record_by_plate(placa):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM registros WHERE placa = :p", {"p": placa})
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

# ----------------------------
# MOTO
# ----------------------------
def save_moto(camera_id, placa):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Verifica se já existe moto cadastrada com essa placa
            cur.execute("SELECT COUNT(*) FROM moto WHERE placa = :placa", {"placa": placa})
            exists = cur.fetchone()[0] > 0

            if exists:
                # Se já existe, apenas atualiza data_entrada e o nm_camera
                cur.execute("""
                    UPDATE moto
                    SET data_entrada = :data_entrada,
                        camera_nome = :camera_nome
                    WHERE placa = :placa
                """, {
                    "data_entrada": datetime.now(),
                    "camera_nome": camera_id,
                    "placa": placa
                })

            else:
                # Inserção padrão com valores default
                cur.execute("""
                    INSERT INTO moto (
                        id, placa, chassi, qr_code,
                        data_entrada, previsao_entrega, fotos,
                        zona_id, patio_id, status_id,
                        observacoes, valor_servico, modelo, camera_nome
                    )
                    VALUES (
                        moto_seq.NEXTVAL, :placa, :chassi, :qr_code,
                        :data_entrada, :previsao_entrega, :fotos,
                        :zona_id, :patio_id, :status_id,
                        :observacoes, :valor_servico, :modelo, :camera_nome
                    )
                """, {
                    "placa": placa,
                    "chassi": f"CH-{placa}",  # valor temporário padrão
                    "qr_code": None,
                    "data_entrada": datetime.now(),
                    "previsao_entrega": None,
                    "fotos": None,
                    "zona_id": 1,
                    "patio_id": 1,         # valor padrão (pátio principal)
                    "status_id": 1,        # status padrão (ex: aguardando)
                    "observacoes": None,
                    "valor_servico": 0.0,
                    "modelo": "SPORT-ESD",
                    "camera_nome": camera_id,
                })
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def get_all_known_plates():
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT placa FROM moto")
            plates = [r[0] for r in cur.fetchall()]
            return plates
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

# ----------------------------
# ALERTAS
# ----------------------------
def save_alert(alert):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM alertas WHERE placa = :placa", {"placa": alert["placa"]})
            exists = cur.fetchone()[0] > 0
            if not exists:
                cur.execute("""
                INSERT INTO alertas (camera_id, placa, timestamp, alert, severity) 
                VALUES (:1, :2, :3, :4, :5)
                """, (
                    alert["camera_id"],
                    alert["placa"],
                    alert["timestamp"],
                    alert["alert"],
                    alert["severity"]
                ))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def save_alerts(alerts):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            for alert in alerts:
                cur.execute("SELECT COUNT(*) FROM alertas WHERE placa = :placa", {"placa": alert["placa"]})
                exists = cur.fetchone()[0] > 0
                if not exists:
                    cur.execute("""
                        INSERT INTO alertas (camera_id, placa, timestamp, alert, severity)
                        VALUES (:1, :2, :3, :4, :5)
                    """, (
                        alert["camera_id"],
                        alert["placa"],
                        alert["timestamp"],
                        alert["alert"],
                        alert["severity"]
                    ))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def load_alerts():
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT camera_id, placa, timestamp, alert, severity FROM alertas")
            rows = cur.fetchall()
            return [
                {
                    "camera_id": r[0],
                    "placa": r[1],
                    "timestamp": r[2],
                    "alert": r[3],
                    "severity": r[4],
                }
                for r in rows
            ]
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def delete_alert(placa):
    with _lock:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM alertas WHERE placa = :p", {"p": placa})
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cur.close()
            conn.close()

def load_alert_by_plate():
    with _lock:
        return