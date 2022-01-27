from django.contrib import admin

from .models import User, Referral, Item, Purchase


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    show_on_display = ("id", "name", "user_id", "username", "balance", "created_at")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    show_on_display = ("id", "referrer_id")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    show_on_display = ("id", "name", "price", "photo")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    show_full_result_count = ("id", "buyer", "item_id", "quantity", "amount", "receiver", "created_at", "successful", "shipping_address", "phone_number", "email")

