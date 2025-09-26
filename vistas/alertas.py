import os, json
from io import BytesIO
from flask import Blueprint, request, jsonify, abort, send_file
from extensions import db
from modelos import Alerta
import pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

bp = Blueprint("alerting", __name__)
ADMIN_SECRET = os.getenv("ADMIN_SECRET","alertas-admin-secret")

@bp.route("/admin/init", methods=["POST"])
def admin_init():
    if request.headers.get("X-Admin-Secret") != ADMIN_SECRET: abort(401)
    db.create_all(); return {"ok": True}

@bp.route("/notificar", methods=["POST"])
def notificar():
    j = request.get_json(force=True)
    a = Alerta(titulo=j.get("titulo",""), detalle_json=json.dumps(j.get("detalle",{})))
    db.session.add(a); db.session.commit()
    return {"ok": True, "id": a.id}

@bp.route("/alertas")
def listar():
    rows = Alerta.query.order_by(Alerta.ts_utc.desc()).limit(200).all()
    return jsonify([{"ts":r.ts_utc.isoformat(),"titulo":r.titulo,
                    "detalle":json.loads(r.detalle_json or "{}")} for r in rows])

@bp.route("/charts/alertas_por_regla.png")
def chart_reglas():
    rows = Alerta.query.all()
    if not rows: abort(404)
    rec=[]
    for r in rows:
        rec.append({"ts": r.ts_utc, "regla": r.titulo})
    df = pd.DataFrame(rec)
    if df.empty: abort(404)
    s = df.groupby("regla").size().sort_values(ascending=False)
    plt.figure(figsize=(6,3)); s.plot(kind="bar"); plt.title("Alertas por regla")
    plt.xlabel("Regla"); plt.ylabel("Total")
    buf = BytesIO(); plt.tight_layout(); plt.savefig(buf, format="png"); buf.seek(0)
    return send_file(buf, mimetype="image/png")

@bp.route("/")
def health(): return {"ok": True}
