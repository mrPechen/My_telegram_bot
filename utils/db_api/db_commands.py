from django_admin.user.models import *
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, full_name, username):
    try:
        return User(user_id=int(user_id), name=full_name, username=username, balance='0').save()
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def add_user_referral(user_id, full_name, username, referrer_id):
    user = User(user_id=int(user_id), name=full_name, username=username, balance='0')
    command1 = user.save()
    id = Referral(id=user, referrer_id=int(referrer_id)).id
    referral = Referral(id=id, referrer_id=int(referrer_id))
    command2 = referral.save()
    try:
        return command1, command2
    except Exception:
        return select_user(int(user_id))


@sync_to_async
def get_item(item_id):
    return Item.objects.get(id=item_id)


@sync_to_async
def search_item(search_query: str = None):
    if search_query:
        result = Item.objects.filter(name__istartswith=search_query)
    else:
        result = Item.objects.all()
    return result


@sync_to_async
def check_referrals(user_id):
    user = User.objects.get(user_id=user_id).id
    referrer_id = Referral.objects.filter(referrer_id__exact=user).all()

    return referrer_id


@sync_to_async
def check_balance(user_id):
    return User.objects.get(user_id=user_id).balance


@sync_to_async
def add_referral_money(referrer_id):
    balance = User.objects.get(id=referrer_id).balance
    a = balance+10
    User.objects.filter(id=referrer_id).update(balance=a)


@sync_to_async
def get_id(user_id):
    return User.objects.get(user_id=user_id).user_id


@sync_to_async
def save_purchase(user_id, phone_number, shipping_address, item, amount, quantity, receiver):
    user = User.objects.get(user_id=user_id)
    item_name = Item.objects.get(name=item)
    save_all = Purchase(buyer=user, item_id=item_name, amount=amount, quantity=quantity,
                        shipping_address=shipping_address, phone_number=phone_number,
                        receiver=receiver).save()
    return save_all
