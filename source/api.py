import csv
import os

from flask import Blueprint, Response, current_app, g, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_csv_path() -> str:
    return os.path.join(current_app.instance_path, "products.csv")


@api_bp.before_request
def load_data() -> None:
    file_path = _get_csv_path()

    if os.path.exists(file_path):
        file_opened = open(file_path, "r+", encoding="utf-8")
        g.file_opened = file_opened
        g.csv_reader = csv.DictReader(file_opened)


@api_bp.teardown_request
def clear_files(error) -> None:
    file_opened = g.pop("file_opened", None)
    g.pop("cvs_reader", None)

    if file_opened is not None:
        file_opened.close()


@api_bp.route("/products", methods=("GET",))
def get_products() -> Response:
    if "csv_reader" not in g or g.csv_reader is None:
        return jsonify({"error": "El archivo de productos no está disponible"}), 404
    products = list(g.csv_reader)
    return jsonify(products), 200


@api_bp.route("/products", methods=("POST",))
def create_product() -> Response:
    data = request.get_json()
    if not data or not all(
        k in data for k in ("product_id", "product_name", "quantity", "price")
    ):
        return (
            jsonify(
                {
                    "error": "Faltan datos obligatorios (product_id, product_name, quantity, price)"
                }
            ),
            400,
        )

    file_path = _get_csv_path()

    # Verificamos si el producto ya existe para evitar duplicados de ID
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["product_id"] == str(data["product_id"]):
                    return jsonify({"error": "El product_id ya existe"}), 409

    # Agregamos el nuevo registro al final del archivo CSV
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["product_id", "product_name", "quantity", "price"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(
            {
                "product_id": str(data["product_id"]),
                "product_name": data["product_name"],
                "quantity": str(data["quantity"]),
                "price": str(data["price"]),
            }
        )

    return jsonify({"message": "Producto creado exitosamente", "product": data}), 201


# --- 3. PUT: Actualizar un producto existente ---
@api_bp.route("/products/<string:product_id>", methods=("PUT",))
def update_product(product_id: str) -> Response:
    data = request.get_json()
    file_path = _get_csv_path()

    if not os.path.exists(file_path):
        return jsonify({"error": "El archivo de productos no existe"}), 404

    rows = []
    updated = False

    # Leemos todos los registros, modificamos el coincidente
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["product_id"] == product_id:
                row["product_name"] = data.get("product_name", row["product_name"])
                row["quantity"] = str(data.get("quantity", row["quantity"]))
                row["price"] = str(data.get("price", row["price"]))
                updated = True
            rows.append(row)

    if not updated:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Reescribimos el archivo CSV con la información actualizada
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({"message": "Producto actualizado exitosamente"})


# --- 4. DELETE: Eliminar un producto ---
@api_bp.route("/products/<string:product_id>", methods=("DELETE",))
def delete_product(product_id: str) -> Response:
    file_path = _get_csv_path()

    if not os.path.exists(file_path):
        return jsonify({"error": "El archivo de productos no existe"}), 404

    rows = []
    deleted = False

    # Filtramos la lista omitiendo el ID que queremos borrar
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["product_id"] == product_id:
                deleted = True
                continue
            rows.append(row)

    if not deleted:
        return jsonify({"error": "Producto no encontrado"}), 404

    # Reescribimos el archivo CSV sin el registro eliminado
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return jsonify({"message": "Producto eliminado exitosamente"})
