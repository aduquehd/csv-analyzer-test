# Models
from trueking_platform.apps.products.models import ProductComment

# Serializers
from trueking_platform.apps.users.serializers.users import SimpleUserSerializer


def comments_tree(product, is_active=True):
    # return []
    """
    List tree of comments of a product
    :param product: product, product related comment. e.g. UUID "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e"
    :param is_active: bool, comment is active. e.g. True
    :return: Json | List | List comments and sub-comments. e.g.
    [{
        "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
        "comment": "what is reference of phone?",
        "parent": None
        "children": [
          {
            "id": "8c8fff64-8886-4688-9a90-24f0d2d918f9",
            "comment": "Is a new phone Moto G Power plus",
            "parent": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "children": None
          }
        ]
      }]
    """
    comments_list = ProductComment.objects.filter(
        parent_comment=None,
        product=product,
        is_active=is_active
    ).prefetch_related(
        'created_by',
        'productcomment_set',
        'productcomment_set__created_by',
        'productcomment_set__productcomment_set',
        'productcomment_set__productcomment_set__created_by',
    ).order_by('created')

    comments_list_tree = []
    for comment in comments_list:
        comments_list_tree.append({
            'id': str(comment.id),
            'comment': comment.comment,
            'created_by': SimpleUserSerializer(instance=comment.created_by, many=False).data,
            'created': comment.created,
            'parent': comment.parent_comment_id,
            'children': comment_children(comment, is_active)
        })
    return comments_list_tree


def comment_children(comment, is_active=True):
    """
    Recursive list to consult the sub-comments of a comment
    :param is_active: bool, comment is active. e.g. True
    :param comment: UUID, comment id of product. e.g "8c8fff64-8886-4688-9a90-24f0d2d918f9"
    :return: Dict | List | List comments and sub-comments. e.g.
    [{
        "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
        "comment": "is a new?",
        "parent": "0811b2e0-531b-4468-a41b-22cc8eb27a30",
        "children": [{
            "id": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "comment": "yes",
            "parent": "57136fa2-7d90-4be5-bb21-bb17bdbfbc3e",
            "children": None
          }
        ]
      }]
    """
    children_list = []
    for comment_child in comment.productcomment_set.all():
        children_list.append({
            'id': str(comment_child.id),
            'created_by': SimpleUserSerializer(instance=comment_child.created_by, many=False).data,
            'created': comment_child.created,
            'comment': comment_child.comment,
            'parent': str(comment_child.parent_comment_id) if comment_child.parent_comment else None,
            'children': comment_children(comment_child, is_active)
        })

    if not children_list:
        return None

    return children_list
