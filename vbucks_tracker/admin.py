from django.contrib import admin
from django.utils.html import format_html
from .models import RealMoneyTransaction, VbucksEarning, VbucksSpending, Refund


class RealMoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_summary', 'amount_with_currency', 'vbucks_earned', 'date')
    list_filter = ('category', 'currency', 'date')
    search_fields = ('user__username', 'source_name')
    ordering = ('-date',)
    fieldsets = (
        ('Transaction', {'fields': ('user', 'category', 'source_name')}),
        ('Financials', {'fields': ('amount', 'currency', 'vbucks_earned'), 'classes': ('collapse',)}),
        ('Metadata', {'fields': ('date', 'notes')})
    )

    def transaction_summary(self, obj):
        return f"{obj.get_category_display()}: {obj.source_name}"

    def amount_with_currency(self, obj):
        return f"{obj.amount} {obj.currency}"

    transaction_summary.short_description = "Transaction"
    amount_with_currency.short_description = "Amount"


class VbucksEarningAdmin(admin.ModelAdmin):
    list_display = ('user', 'earning_type', 'amount', 'date', 'earning_name')
    list_filter = ('type', 'date')
    search_fields = ('user__username', 'earning_name')
    list_editable = ('amount',)

    def earning_type(self, obj):
        return obj.get_type_display()

    earning_type.short_description = "Type"


class VbucksSpendingAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'category', 'vbucks_spent', 'date', 'refunded')
    list_filter = ('category', 'refunded', 'date')
    search_fields = ('user__username', 'item_name')
    list_editable = ('vbucks_spent', 'refunded')


class RefundAdmin(admin.ModelAdmin):
    list_display = ('user', 'purchase_link', 'vbucks_returned', 'refund_date', 'reason')
    list_filter = ('reason', 'refund_date')
    search_fields = ('user__username', 'original_purchase__item_name')
    raw_id_fields = ('original_purchase',)

    def purchase_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            f'/admin/vbucks_tracker/vbucksspending/{obj.original_purchase.id}/change/',
            obj.original_purchase.item_name
        )

    purchase_link.short_description = "Original Purchase"


admin.site.register(RealMoneyTransaction, RealMoneyTransactionAdmin)
admin.site.register(VbucksEarning, VbucksEarningAdmin)
admin.site.register(VbucksSpending, VbucksSpendingAdmin)
admin.site.register(Refund, RefundAdmin)