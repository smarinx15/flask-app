from flask import Flask, request, session, redirect, url_for
import numpy as np

app = Flask(__name__)
app.secret_key = 'clave_secreta_123'

def inicializar_matriz():
    if 'matriz_produccion' not in session:
        session['matriz_produccion'] = np.zeros((2, 2, 3)).tolist()

@app.route('/')
def inicio():
    inicializar_matriz()
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Registro de Azucar</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 50px; 
            background-color: #f5f5f5; 
        }
        .container { 
            background-color: white; 
            padding: 30px; 
            border-radius: 10px; 
            max-width: 500px; 
            margin: 0 auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333; 
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group { 
            margin: 20px 0; 
        }
        label { 
            display: block; 
            font-weight: bold; 
            margin-bottom: 8px;
            color: #555;
        }
        select, input { 
            width: 100%; 
            padding: 10px; 
            font-size: 16px; 
            border: 2px solid #ddd; 
            border-radius: 5px;
            box-sizing: border-box;
        }
        select:focus, input:focus {
            border-color: #007bff;
            outline: none;
        }
        button { 
            background-color: #007bff; 
            color: white; 
            padding: 12px 30px; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            margin: 20px 0;
        }
        button:hover { 
            background-color: #0056b3; 
        }
        .btn { 
            background-color: #28a745; 
            color: white; 
            padding: 10px 20px; 
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 5px;
            font-size: 14px;
        }
        .btn:hover { 
            background-color: #218838; 
        }
        .btn-danger {
            background-color: #dc3545;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .botones { 
            text-align: center; 
            margin-top: 30px; 
        }
        .mensaje { 
            background-color: #d4edda; 
            color: #155724; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0;
            border: 1px solid #c3e6cb;
        }
        .error { 
            background-color: #f8d7da; 
            color: #721c24; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 20px 0;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>REGISTRO DE AZUCAR - INGENIO MANUELITO</h1>
        
        <form method="POST" action="/registrar">
            <div class="form-group">
                <label>Planta:</label>
                <select name="planta" required>
                    <option value="">-- Seleccione una planta --</option>
                    <option value="1">1. Palmira</option>
                    <option value="2">2. Buga</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Turno:</label>
                <select name="turno" required>
                    <option value="">-- Seleccione un turno --</option>
                    <option value="1">1. Mañana</option>
                    <option value="2">2. Tarde</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Tipo de Azucar:</label>
                <select name="tipo" required>
                    <option value="">-- Seleccione el tipo --</option>
                    <option value="1">1. Cruda</option>
                    <option value="2">2. Blanca</option>
                    <option value="3">3. Organica</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Cantidad (toneladas):</label>
                <input type="number" name="cantidad" step="0.1" min="0" required placeholder="Ejemplo: 25.5">
            </div>
            
            <button type="submit">REGISTRAR PRODUCCION</button>
        </form>
        
        <div class="botones">
            <a href="/reporte" class="btn">Ver Reporte Completo</a>
            <a href="/limpiar" class="btn btn-danger" onclick="return confirm('¿Seguro que desea limpiar todos los datos?')">Limpiar Todo</a>
        </div>
    </div>
</body>
</html>
"""
    return html

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return redirect(url_for('inicio'))
    
    try:
        planta = int(request.form['planta']) - 1
        turno = int(request.form['turno']) - 1
        tipo = int(request.form['tipo']) - 1
        cantidad = float(request.form['cantidad'])
        
        matriz = np.array(session.get('matriz_produccion', np.zeros((2, 2, 3)).tolist()))
        matriz[planta][turno][tipo] += cantidad
        session['matriz_produccion'] = matriz.tolist()
        
        nombres_planta = ["Palmira", "Buga"]
        nombres_turno = ["Mañana", "Tarde"]
        nombres_tipo = ["Cruda", "Blanca", "Organica"]
        
        mensaje = f"REGISTRO EXITOSO: {nombres_planta[planta]} - {nombres_turno[turno]} - {nombres_tipo[tipo]} - {cantidad} toneladas"
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Registro de Azucar</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f5f5f5; }
        .container { background-color: white; padding: 30px; border-radius: 10px; max-width: 500px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; margin-bottom: 30px; }
        .form-group { margin: 20px 0; }
        label { display: block; font-weight: bold; margin-bottom: 8px; color: #555; }
        select, input { width: 100%; padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        select:focus, input:focus { border-color: #007bff; outline: none; }
        button { background-color: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; margin: 20px 0; }
        button:hover { background-color: #0056b3; }
        .btn { background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; font-size: 14px; }
        .btn:hover { background-color: #218838; }
        .btn-danger { background-color: #dc3545; }
        .btn-danger:hover { background-color: #c82333; }
        .botones { text-align: center; margin-top: 30px; }
        .mensaje { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; border: 1px solid #c3e6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>REGISTRO DE AZUCAR - INGENIO MANUELITO</h1>
        
        <div class="mensaje">✓ """ + mensaje + """</div>
        
        <form method="POST" action="/registrar">
            <div class="form-group">
                <label>Planta:</label>
                <select name="planta" required>
                    <option value="">-- Seleccione una planta --</option>
                    <option value="1">1. Palmira</option>
                    <option value="2">2. Buga</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Turno:</label>
                <select name="turno" required>
                    <option value="">-- Seleccione un turno --</option>
                    <option value="1">1. Mañana</option>
                    <option value="2">2. Tarde</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Tipo de Azucar:</label>
                <select name="tipo" required>
                    <option value="">-- Seleccione el tipo --</option>
                    <option value="1">1. Cruda</option>
                    <option value="2">2. Blanca</option>
                    <option value="3">3. Organica</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Cantidad (toneladas):</label>
                <input type="number" name="cantidad" step="0.1" min="0" required placeholder="Ejemplo: 25.5">
            </div>
            
            <button type="submit">REGISTRAR PRODUCCION</button>
        </form>
        
        <div class="botones">
            <a href="/reporte" class="btn">Ver Reporte Completo</a>
            <a href="/limpiar" class="btn btn-danger" onclick="return confirm('¿Seguro que desea limpiar todos los datos?')">Limpiar Todo</a>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1><a href='/'>Volver</a>"

@app.route('/reporte')
def reporte():
    try:
        matriz_produccion = np.array(session.get('matriz_produccion', np.zeros((2, 2, 3)).tolist()))
        
        total_dia = np.sum(matriz_produccion)
        por_planta = np.sum(matriz_produccion, axis=(1,2))
        por_tipo = np.sum(matriz_produccion, axis=(0, 1))
        por_turno = np.sum(matriz_produccion, axis=(0, 2))
        
        cana_necesaria = total_dia * 10
        costo_total = cana_necesaria * 180000
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Produccion</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; background-color: #f5f5f5; }}
        .container {{ background-color: white; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
        h2 {{ color: #555; border-bottom: 2px solid #007bff; padding-bottom: 5px; }}
        .total-grande {{ font-size: 28px; color: #007bff; font-weight: bold; text-align: center; margin: 20px 0; background-color: #e7f3ff; padding: 20px; border-radius: 8px; }}
        .seccion {{ background-color: #f8f9fa; padding: 20px; margin: 20px 0; border-radius: 8px; border-left: 4px solid #007bff; }}
        .btn {{ background-color: #007bff; color: white; padding: 12px 25px; border: none; border-radius: 5px; text-decoration: none; display: inline-block; margin: 15px 5px; }}
        .btn:hover {{ background-color: #0056b3; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #007bff; color: white; font-weight: bold; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .numero {{ font-weight: bold; color: #28a745; }}
        .centrado {{ text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>=== REPORTE FINAL DE PRODUCCION ===</h1>
        
        <div class="total-grande">
            PRODUCCION TOTAL DEL DIA: {total_dia:.1f} TONELADAS
        </div>
        
        <div class="seccion">
            <h2>PRODUCCION POR PLANTA</h2>
            <p>• <strong>Palmira:</strong> <span class="numero">{por_planta[0]:.1f} toneladas</span></p>
            <p>• <strong>Buga:</strong> <span class="numero">{por_planta[1]:.1f} toneladas</span></p>
        </div>
        
        <div class="seccion">
            <h2>PRODUCCION POR TIPO DE AZUCAR</h2>
            <p>• <strong>Azucar Cruda:</strong> <span class="numero">{por_tipo[0]:.1f} toneladas</span></p>
            <p>• <strong>Azucar Blanca:</strong> <span class="numero">{por_tipo[1]:.1f} toneladas</span></p>
            <p>• <strong>Azucar Organica:</strong> <span class="numero">{por_tipo[2]:.1f} toneladas</span></p>
        </div>
        
        <div class="seccion">
            <h2>PRODUCCION POR TURNO</h2>
            <p>• <strong>Turno Mañana:</strong> <span class="numero">{por_turno[0]:.1f} toneladas</span></p>
            <p>• <strong>Turno Tarde:</strong> <span class="numero">{por_turno[1]:.1f} toneladas</span></p>
        </div>
        
        <div class="seccion">
            <h2>RECURSOS Y COSTOS</h2>
            <p>• <strong>Caña de azucar necesaria:</strong> <span class="numero">{cana_necesaria:.1f} toneladas</span></p>
            <p>• <strong>Costo total estimado:</strong> <span class="numero">${costo_total:,.0f} COP</span></p>
        </div>
        
        <h2>MATRIZ COMPLETA DE PRODUCCION</h2>
        <table>
            <tr>
                <th>PLANTA</th>
                <th>TURNO</th>
                <th>CRUDA</th>
                <th>BLANCA</th>
                <th>ORGANICA</th>
                <th>TOTAL FILA</th>
            </tr>
            <tr>
                <td><strong>Palmira</strong></td>
                <td>Mañana</td>
                <td>{matriz_produccion[0][0][0]:.1f}</td>
                <td>{matriz_produccion[0][0][1]:.1f}</td>
                <td>{matriz_produccion[0][0][2]:.1f}</td>
                <td><strong>{np.sum(matriz_produccion[0][0]):.1f}</strong></td>
            </tr>
            <tr>
                <td><strong>Palmira</strong></td>
                <td>Tarde</td>
                <td>{matriz_produccion[0][1][0]:.1f}</td>
                <td>{matriz_produccion[0][1][1]:.1f}</td>
                <td>{matriz_produccion[0][1][2]:.1f}</td>
                <td><strong>{np.sum(matriz_produccion[0][1]):.1f}</strong></td>
            </tr>
            <tr>
                <td><strong>Buga</strong></td>
                <td>Mañana</td>
                <td>{matriz_produccion[1][0][0]:.1f}</td>
                <td>{matriz_produccion[1][0][1]:.1f}</td>
                <td>{matriz_produccion[1][0][2]:.1f}</td>
                <td><strong>{np.sum(matriz_produccion[1][0]):.1f}</strong></td>
            </tr>
            <tr>
                <td><strong>Buga</strong></td>
                <td>Tarde</td>
                <td>{matriz_produccion[1][1][0]:.1f}</td>
                <td>{matriz_produccion[1][1][1]:.1f}</td>
                <td>{matriz_produccion[1][1][2]:.1f}</td>
                <td><strong>{np.sum(matriz_produccion[1][1]):.1f}</strong></td>
            </tr>
            <tr style="background-color: #e3f2fd;">
                <td colspan="2"><strong>TOTALES</strong></td>
                <td><strong>{por_tipo[0]:.1f}</strong></td>
                <td><strong>{por_tipo[1]:.1f}</strong></td>
                <td><strong>{por_tipo[2]:.1f}</strong></td>
                <td><strong>{total_dia:.1f}</strong></td>
            </tr>
        </table>
        
        <div class="centrado">
            <a href="/" class="btn">Volver al Registro</a>
            <a href="/limpiar" class="btn" style="background-color: #dc3545;" onclick="return confirm('¿Seguro que desea limpiar todos los datos?')">Limpiar Todo</a>
        </div>
    </div>
</body>
</html>
"""
        return html
        
    except Exception as e:
        return f"<h1>Error al generar reporte: {e}</h1><a href='/'>Volver</a>"

@app.route('/limpiar')
def limpiar():
    session['matriz_produccion'] = np.zeros((2, 2, 3)).tolist()
    return redirect(url_for('inicio'))

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
