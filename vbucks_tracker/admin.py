from django.contrib import admin
from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund

class RealMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'currency', 'vbucks_earned', 'date')
    list_filter = ('category', 'currency', 'date')
    search_fields = ('user__username', 'source_name')
    date_hierarchy = 'date'
    ordering = ('-date',)

class VbucksEarningAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'date', 'earning_name')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'earning_name')
    date_hierarchy = 'date'

class VbucksSpendingAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'category', 'vbucks_spent', 'date', 'refunded')
    list_filter = ('category', 'refunded', 'date')
    search_fields = ('user__username', 'item_name')
    date_hierarchy = 'date'
    list_editable = ('refunded',)

class RefundAdmin(admin.ModelAdmin):
    list_display = ('user', 'original_purchase', 'vbucks_returned', 'refund_date', 'reason')
    list_filter = ('reason', 'refund_date')
    search_fields = ('user__username', 'original_purchase__item_name')
    raw_id_fields = ('original_purchase',)

admin.site.register(RealMoneyTransaction, RealMoneyTransactionAdmin)
admin.site.register(VbucksEarning, VbucksEarningAdmin)
admin.site.register(VbucksSpending, VbucksSpendingAdmin)
admin.site.register(Refund, RefundAdmin)