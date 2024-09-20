from flask_crud.manage import CrudRegistrable


class ProductEntity(CrudRegistrable):
    table_name = "products"
    id_name = "id_product"
    entity_name = "product"
    enums = {
        "category":["lacteo","embutido","hogar", "alimentos", "higiene"],
    }
    requireds = ["category"]
    # enumsmuliple = ["category"]

    def __init__(self, name_product="", price=9.76, fecha_expiracion="2024-05-12", category="SELECCIONE:") -> None:
        self.name_product = name_product
        self.price = price
        self.category = category
        self.fecha_expiracion = fecha_expiracion
