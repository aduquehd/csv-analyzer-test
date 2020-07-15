# Models
from trueking_platform.apps.products.models import ProductCategory


def categories_tree(is_active=True):
    # return []
    """
    List tree of categories and subcategories of a product
    :param is_active: bool, category is active. e.g. True
    :return: Json | List | List categories and sub-categories. e.g.
    [{
        "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
        "slug": "Electronicos-0",
        "attributes": {
          "data-id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e"
        },
        "name": "Electronicos",
        "parent": "0811b2e0-531b-4468-a41b-22cc8eb27a30",
        "children": [
          {
            "id": "8c8fff64-8886-4688-9a90-24f0d2d918f9",
            "slug": "Ropa-0",
            "attributes": {
              "data-id": "8c8fff64-8886-4688-9a90-24f0d2d918f9"
            },
            "name": "Ropa",
            "parent": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "children": None
          }
        ]
      }]
    """
    categories_list = ProductCategory.objects.filter(
        parent_category=None,
        is_active=is_active
    ).prefetch_related(
        'productcategory_set',
        'productcategory_set__productcategory_set',
        'productcategory_set__productcategory_set__productcategory_set',
        'productcategory_set__productcategory_set__productcategory_set__productcategory_set',
    ).order_by('created')

    categories_list_tree = []
    for category in categories_list:
        categories_list_tree.append({
            'id': str(category.id),
            'slug': str(category.slug),
            'name': category.name,
            'parent': category.parent_category_id,
            'children': category_children(category, is_active)
        })
    return categories_list_tree


def category_children(category, is_active=True):
    """
    Recursive list to consult the sub-categories of a category
    :param is_active: bool, category is active. e.g. True
    :param category: UUID, category id of product. e.g "8c8fff64-8886-4688-9a90-24f0d2d918f9"
    :return: Dict | List | List categories and sub-categories. e.g.
    [{
        "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
        "slug": "Electronicos-0",
        "attributes": {
          "data-id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e"
        },
        "name": "Electronicos",
        "parent": "0811b2e0-531b-4468-a41b-22cc8eb27a30",
        "children": [{
            "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "slug": "Ropa-0",
            "attributes": {
              "data-id": "8c8fff64-8886-4688-9a90-24f0d2d918f9"
            },
            "name": "Ropa",
            "parent": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "children": None
          }
        ]
      }]
    """
    children_list = []
    for category_child in category.productcategory_set.all():
        children_list.append({
            'id': str(category_child.id),
            'slug': str(category_child.slug),
            'name': category_child.name,
            'parent': str(category_child.parent_category_id) if category_child.parent_category else None,
            'children': category_children(category_child, is_active)
        })

    if not children_list:
        return None

    return children_list


def category_parents(category):
    """
    Get list parents of category
    :param category: Object category,  product. e.g <8c8fff64-8886-4688-9a90-24f0d2d918f9>
    :return: Dict | List | List categories and sub-categories. e.g.
        [
            {
                "id": "c0136516-ff72-441a-9835-1ecb37357c41",
                "name": "Sombreros y Gorros"
            },
            {
                "id": "ff2cbe7e-a817-41d5-9363-6175bb757505",
                "name": "Accesorios"
            },
            {
                "id": "7b68e61c-516a-45b4-8eda-654f3af39e03",
                "name": "ROPA MUJER"
            }
        ]
    """

    if not category.parent_category:
        return []

    parent_list = []
    while category.parent_category:
        parent_list.append({
            'id': str(category.id),
            'name': category.name,
        }
        )

        category = category.parent_category

    parent_list.append({
        'id': str(category.id),
        'name': category.name,
    }
    )

    return parent_list
