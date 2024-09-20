from flask import Flask, flash, render_template, request, url_for, redirect

# from flask_crud.crud import CrudRegistrable
from flask_crud.manage import CrudEntityStore, RenderDataHandler
from flask_crud.view import Btn, FormView, Opt
from models import ProductEntity

# from flask_mysqldb import MySQL
app = Flask(__name__)
app.config["SECRET_KEY"] = "mi_clave_secreta_unica_y_segura"

db = {
    ProductEntity.table_name: [
        {
            "id_product": 0,
            "name_product": "PAPEL HIGIENICO HADA X6",
            "price": "0.99",
            "category": "higiene",
            "fecha_expiracion":"2025-06-12",
        },
        {
            "id_product": 1,
            "name_product": "JABON PALMOLIVE HUMAN",
            "price": "3.99",
            "category": "higiene",
            "fecha_expiracion":"2025-06-12",
        },
        {
            "id_product": 2,
            "name_product": "ENCEBO",
            "price": "32.75",
            "category":"alimentos",
            "fecha_expiracion":"2025-06-12",
        },
    ]
}

endpoints_verbose = {
    "edit": {
        "text_submit": "Editar",
    },
    "delete": {
        "text_submit": "Eliminar",
    },
    "manage": {
        "text_submit": "Añadir",
    },
}

def changeTextSubmit(endpoint_name, form_view):
    form_view.main_btn.name_action = endpoints_verbose[endpoint_name]["text_submit"]

FormView._endpoint_change_listeners = [changeTextSubmit]

@app.route("/", methods=["GET"])
def landing():
    return "<h1>Landing page!</h1>"


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return "<h1>Dashboard!</h1>"


@app.route("/logout", methods=["GET"])
def logout():
    return "<h1>Dashboard!</h1>"

@app.route("/search", methods=["POST"])
def search():
    return request.form

view = CrudEntityStore.getView("product")      
# CrudEntityStore.registerView()
OptEdit = Opt(
    name_action= "Editar",
    isGetId= True,
    endpoint_name="edit",
    htmlclass="btn btn-warning btn-sm"
)
optDelete = Opt(
    name_action= "Eliminar",
    isPostId= True,
    endpoint_name="delete",
    htmlclass="btn btn-danger btn-sm"
)
view.table.opts["edit-product"] = OptEdit
view.table.opts["del-product"] =  optDelete

view.form.btns["search"] =  Btn(
        name_action="Buscar",
        isSubmit=True,
        endpoint_name="search",
        htmlclass="btn btn-light",
    )
view.form.btns["hi"] =  Btn(
        name_action="Hi!",
        isSimple=True,
        endpoint_name="dashboard",
        htmlclass="btn btn-success",
    )

@app.route("/manage-<entity_name>", methods=["GET", "POST"])
def manager(entity_name):
    entity = CrudEntityStore.getEntity(entity_name)
    if request.method == "POST":
        categories = request.form.getlist('category')               
        data = dict(request.form)
        data['category'] = categories
        print(f"------- DATOS AGREGADOSS: dataform={data}")
        state, msg = view.form.anyEqual(request.form)
        print(f"state: {state}, msg: {msg}")
        if state:
            flash("Falta llenar campos obligatorios: "+msg, "warning")
            return redirect(url_for("manager", entity_name=entity_name))
        else:
            flash("Registro satisfactorio.", "success")
        rows = db.get(entity.table_name)
        data[entity.id_name] = len(rows)
        print(db.get(entity.table_name))
        db.get(entity.table_name).append(data)
        print(db.get(entity.table_name))
    RenderDataHandler.onFormData(None, "manage")
    # RenderDataHandler.onTableData(entity.all())
    RenderDataHandler.onTableData(db.get(entity.table_name))
    return render_template(
        "form_table.html", template_data=RenderDataHandler.toTemplateData()
    )


@app.route("/edit-<entity_name>/<int:id>", methods=["GET", "POST"])
def edit(entity_name, id):
    entity = CrudEntityStore.getEntity(entity_name)
    print(f"------- DATOS TO CHANGES: id={id} dataform={dict(request.form)}")
    if request.method == "POST":
        products = db.get(entity.table_name)
        data = dict(request.form)
        print(f"------- DATOS CAMBIADOS: id={id} dataform={data}")
        data[entity.id_name] = id
        products[id] = data
        print(db.get(entity.table_name))
        return redirect(url_for("manager", entity_name=entity_name))
    # RenderDataHandler.onTableData(entity.all())
    RenderDataHandler.onFormData(db.get(entity.table_name)[id], "edit")
    RenderDataHandler.onTableData(db.get(entity.table_name))
    return render_template(
        "form_table.html", template_data=RenderDataHandler.toTemplateData()
    )


@app.route("/delete-<entity_name>/<int:id>", methods=["POST"])
def delete(entity_name, id):
    # if request.method == "GET":
    # return"Holaaa "+str(id)
    print(f"ELIMINANDO {entity_name} con ID: {id}")
    entity = CrudEntityStore.getEntity(entity_name)
    products = db.get(entity.table_name)
    datos = products[id]
    products.pop(id)
    print(f"------- DATOS ELIMINADOS: id={id} dataform={datos}")
    print(db.get(entity.table_name))
    RenderDataHandler.onTableData(db.get(entity.table_name))
    return redirect(url_for("manager", entity_name=entity_name))

# if __name__ == "__main__":
app.run(debug=True)
